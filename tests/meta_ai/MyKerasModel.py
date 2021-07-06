import json
import os
from urllib.request import urlopen

import cv2
import numpy as np
import superai_schema.universal_schema.task_schema_functions as df
from superai.meta_ai import BaseModel
from superai.utils import log
from tensorflow import keras
from tensorflow.keras import layers


class MyKerasModel(BaseModel):
    model = None

    def __init__(self, *args, **kwargs):
        super(MyKerasModel, self).__init__(*args, **kwargs)

    def load_weights(self, weights_path):
        self.model = keras.models.load_model(weights_path)

    def predict(self, input):
        log.info("Predict Input: ", input)
        image_url = input["data"]["image_url"]
        req = urlopen(image_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
        input = np.reshape(img, (1, 28 * 28))
        pred = self.model.predict(input)
        output = np.argmax(pred[0])
        return [
            {
                "prediction": {
                    "mnist_class": df.exclusive_choice(
                        choices=list(map(str, range(10))),
                        selection=int(output),
                    )
                },
                "score": float(pred[0][int(output)]),
            }
        ]

    def train(self, model_save_path, **kwargs):
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

        model = self.define_model()

        model.compile(
            optimizer=keras.optimizers.RMSprop(learning_rate=1e-3),
            loss=keras.losses.SparseCategoricalCrossentropy(),
            metrics=[keras.metrics.SparseCategoricalAccuracy()],
        )

        print("Fit model on training data")
        history = model.fit(
            x_train,
            y_train,
            batch_size=64,
            epochs=10,
            # We pass some validation for
            # monitoring validation loss and metrics
            # at the end of each epoch
            validation_data=(x_val, y_val),
        )

        # Picked from https://www.tensorflow.org/guide/keras/save_and_serialize
        model.save(model_save_path)

        # we could also store the model config in a json format in the save path
        json_config = model.to_json()
        with open(os.path.join(model_save_path, "model_config.json"), "w") as json_writer:
            json.dump(json_config, json_writer)
        with open(os.path.join(model_save_path, "config.json"), "w") as json_config_writer:
            json.dump(kwargs, json_config_writer)

    @staticmethod
    def define_model():
        inputs = keras.Input(shape=(784,), name="digits")
        x = layers.Dense(64, activation="relu", name="dense_1")(inputs)
        x = layers.Dense(64, activation="relu", name="dense_2")(x)
        outputs = layers.Dense(10, activation="softmax", name="predictions")(x)

        model = keras.Model(inputs=inputs, outputs=outputs)

        return model

    def to_tf(self):
        if self.model is not None:
            return self.model
        else:
            return self.define_model()
