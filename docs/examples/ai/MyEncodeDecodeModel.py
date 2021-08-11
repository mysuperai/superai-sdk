import datetime
from urllib.request import urlopen

import cv2
import numpy as np
import superai_schema.universal_schema.task_schema_functions as df
from superai.meta_ai import BaseModel
from superai.utils import log
from tensorflow import keras
from tensorflow.keras import layers


class MyEncodeDecodeModel(BaseModel):
    model = None

    def __init__(self, *args, **kwargs):
        super(MyEncodeDecodeModel, self).__init__(*args, **kwargs)
        if self.logger_dir is None:
            self.logger_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def load_weights(self, weights_path):
        self.model = self.define_model()
        self.model.load_weights(weights_path)

    def predict(self, input):
        log.info("Predict Input: ", input)
        input = self.preprocess(input)
        pred = self.model.predict(input)
        return self.postprocess(pred)

    def preprocess(self, input, preprocess_params=None):
        image_url = input["image_url"]
        req = urlopen(image_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
        input = np.reshape(img, (1, 28 * 28))
        return input

    def postprocess(self, pred, postprocess_params=None):
        input = np.argmax(pred[0])
        return [
            {
                "prediction": {
                    "mnist_class": df.exclusive_choice(
                        choices=list(map(str, range(10))),
                        selection=int(input),
                    )
                },
                "score": float(pred[0][int(input)]),
            }
        ]

    def train(
        self,
        model_save_path,
        encoder_trainable=True,
        decoder_trainable=True,
        hyperparameters=None,
        model_parameters=None,
        **kwargs,
    ):
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

        # Preprocess the data (these are NumPy arrays)
        x_train = x_train.reshape(60000, 784).astype("float32") / 255
        x_test = x_test.reshape(10000, 784).astype("float32") / 255

        y_train = y_train.astype("float32")
        y_test = y_test.astype("float32")

        # Reserve 10,000 samples for validation
        x_val = x_train[-10000:]
        y_val = y_train[-10000:]
        x_train = x_train[:-10000]
        y_train = y_train[:-10000]

        self.model = self.define_model(encoder_trainable, decoder_trainable)

        self.model.compile(
            optimizer=keras.optimizers.RMSprop(learning_rate=hyperparameters.learning_rate),
            loss=keras.losses.SparseCategoricalCrossentropy(),
            metrics=[keras.metrics.SparseCategoricalAccuracy()],
        )

        tensorboard_callback = keras.callbacks.TensorBoard(log_dir=self.logger_dir, histogram_freq=1)
        # Adapted from https://www.tensorflow.org/tutorials/keras/save_and_load to support encoder decoder structure
        cp_callback = keras.callbacks.ModelCheckpoint(
            filepath=model_save_path,
            save_weights_only=True,
            verbose=1,
        )
        log.info("Fit model on training data")
        history = self.model.fit(
            x_train,
            y_train,
            batch_size=hyperparameters.batch_size,
            epochs=hyperparameters.epochs,
            # We pass some validation for
            # monitoring validation loss and metrics
            # at the end of each epoch
            validation_data=(x_val, y_val),
            callbacks=[tensorboard_callback, cp_callback],
        )

        # Picked from https://www.tensorflow.org/guide/keras/save_and_serialize
        # self.model.save(model_save_path)

        # we could also store the model config in a json format in the save path
        # json_config = self.model.to_json()
        # with open(os.path.join(model_save_path, "model_config.json"), "w") as json_writer:
        #     json.dump(json_config, json_writer)

    def define_model(self, train_encoder=True, train_decoder=True):
        inputs = keras.Input(shape=(784,), name="digits")
        encoder = self._encoder(trainable=train_encoder)(inputs)
        decoder = self._decoder(trainable=train_decoder)(encoder)
        self.model = keras.Model(inputs=inputs, outputs=decoder)
        return self.model

    def _encoder(self, input_data=None, trainable=True):
        encoder = keras.Sequential(
            [
                keras.Input(shape=(784,), name="digits"),
                layers.Dense(64, activation="relu", name="dense_1"),
                layers.Dense(64, activation="relu", name="dense_2"),
            ]
        )
        encoder.trainable = trainable
        return encoder

    def _decoder(self, input_data=None, trainable=True):
        decoder = keras.Sequential(
            [
                keras.Input(shape=(64,)),
                layers.Dense(len(self.output_schema.params.choices), activation="softmax", name="predictions"),
            ]
        )
        decoder.trainable = trainable
        return decoder

    def to_tf(self):
        return self.model
