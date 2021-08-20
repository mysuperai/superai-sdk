import json
import os

import tensorflow as tf
from superai.meta_ai import BaseModel
from superai.utils import log
from tensorflow import keras
from tensorflow.keras import layers


###########################################################################
# Tracking a training operation
###########################################################################
class MyTrackerModel(BaseModel):
    model = None

    def __init__(self, *args, **kwargs):
        super(MyTrackerModel, self).__init__(*args, **kwargs)

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
        # x_val = x_train[-10000:]
        # y_val = y_train[-10000:]
        x_train = x_train[:-10000]
        y_train = y_train[:-10000]

        model = self.define_model(encoder_trainable, decoder_trainable)

        loss_obj = keras.losses.SparseCategoricalCrossentropy()
        optimizer = keras.optimizers.RMSprop(learning_rate=hyperparameters.learning_rate)
        train_loss = tf.keras.metrics.Mean("train_loss", dtype=tf.float32)
        train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy("train_accuracy")
        test_loss = tf.keras.metrics.Mean("test_loss", dtype=tf.float32)
        test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy("test_accuracy")
        train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
        test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test))
        log.info("Fit model on training data")
        for epoch in range(hyperparameters.epochs):
            for (x, y) in train_dataset:
                with tf.GradientTape() as tape:
                    predictions = model(x, training=True)
                    loss = loss_obj(y, predictions)
                grads = tape.gradient(loss, model.trainable_variables)
                optimizer.apply_gradients(zip(grads, model.trainable_variables))
                train_loss(loss)
                train_accuracy(y_train, predictions)

            self.tracker.add_scalar("loss", train_loss.result(), step=epoch)
            self.tracker.add_scalar("accuracy", train_accuracy.result(), step=epoch)

            for (x, y) in test_dataset:
                predictions = model(x)
                loss = loss_obj(y, predictions)
                test_loss(loss)
                test_accuracy(y_train, predictions)
            self.tracker.add_scalar("loss", test_loss.result(), step=epoch)
            self.tracker.add_scalar("accuracy", test_accuracy.result(), step=epoch)
        # Picked from https://www.tensorflow.org/guide/keras/save_and_serialize
        model.save(model_save_path)

        # we could also store the model config in a json format in the save path
        json_config = model.to_json()
        with open(os.path.join(model_save_path, "model_config.json"), "w") as json_writer:
            json.dump(json_config, json_writer)

    def define_model(self, train_encoder=True, train_decoder=True):
        inputs = keras.Input(shape=(784,), name="digits")
        encoder = self._encoder(trainable=train_encoder)(inputs)
        decoder = self._decoder(trainable=train_decoder)(encoder)
        model = keras.Model(inputs=inputs, outputs=decoder)
        return model

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
                layers.Dense(10, activation="softmax", name="predictions"),
            ]
        )
        decoder.trainable = trainable
        return decoder

    def to_tf(self):
        return self.model
