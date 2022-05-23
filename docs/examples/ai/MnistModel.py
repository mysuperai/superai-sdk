from pathlib import Path

import tensorflow as tf
from polyaxon import tracking
from polyaxon.tracking.contrib.keras import PolyaxonKerasCallback
from tensorflow import keras

from superai.meta_ai import BaseModel
from superai.meta_ai.base.base_ai import default_random_seed
from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters

OPTIMIZERS = {
    "adam": tf.keras.optimizers.Adam,
    "rmsprop": tf.keras.optimizers.RMSprop,
    "sgd": tf.keras.optimizers.SGD,
}


class MnistModel(BaseModel):
    def __init__(self, **kwargs):
        super(MnistModel, self).__init__(**kwargs)
        self.model = None

    @staticmethod
    def create_model(x_train, model_parameter: ModelParameters):
        model = tf.keras.models.Sequential()
        model.add(
            tf.keras.layers.Conv2D(
                filters=model_parameter.conv1_size,
                kernel_size=(3, 3),
                activation="relu",
                input_shape=x_train.shape[1:],
            )
        )
        model.add(tf.keras.layers.Conv2D(filters=model_parameter.conv2_size, kernel_size=(3, 3), activation="relu"))
        model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(tf.keras.layers.Dropout(model_parameter.dropout))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(model_parameter.hidden1_size, activation="relu"))
        model.add(tf.keras.layers.Dense(10, activation="softmax"))
        return model

    def load_weights(self, weights_path: str):
        pass

    def predict(self, inputs, context=None):
        pass

    @staticmethod
    def transform_data(x_train, y_train, x_test, y_test):
        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        x_train = x_train.astype("float32") / 255

        x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
        x_test = x_test.astype("float32") / 255

        y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
        y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

        return x_train, y_train, x_test, y_test

    def train(
        self,
        model_save_path,
        training_data,
        validation_data=None,
        test_data=None,
        production_data=None,
        encoder_trainable: bool = True,
        decoder_trainable: bool = True,
        hyperparameters: HyperParameterSpec = None,
        model_parameters: ModelParameters = None,
        callbacks=None,
        random_seed=default_random_seed,
    ):
        print("Training data: ", training_data)
        training_dir = Path(training_data)
        print("Training dir: ", training_dir)
        print("Training dir exists: ", training_dir.exists())
        print("Training dir is dir: ", training_dir.is_dir())
        print("Training dir content: ", list(training_dir.iterdir()))

        if callbacks is None or isinstance(callbacks, str):
            callbacks = []
        print("Hyperparams: ", hyperparameters.__dict__)
        print("Model params: ", model_parameters.__dict__)
        tracking.init()
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        x_train, y_train, x_test, y_test = self.transform_data(x_train, y_train, x_test, y_test)
        optimizer = OPTIMIZERS[hyperparameters.optimizer](lr=10**hyperparameters.log_learning_rate)
        self.model = self.create_model(x_train, model_parameters)
        self.model.compile(
            optimizer=optimizer,
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )

        tensorboard_callback = keras.callbacks.TensorBoard(log_dir=tracking.get_tensorboard_path())
        plx_callback = PolyaxonKerasCallback(run=tracking.TRACKING_RUN)
        callbacks.extend([tensorboard_callback, plx_callback])
        self.model.fit(
            x_train,
            y_train,
            epochs=hyperparameters.epochs,
            batch_size=100,
            callbacks=callbacks,  # Polyaxon
        )
        accuracy = self.model.evaluate(x_test, y_test)[1]

        tracking.log_metrics(eval_accuracy=accuracy)
