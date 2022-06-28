"""
Training on the Intel Image Classification Dataset
(https://www.kaggle.com/datasets/puneet6060/intel-image-classification)

The adaptation of the model is done from https://www.kaggle.com/code/vincee/intel-image-classification-cnn-keras
"""
import logging
import os
from typing import Tuple

import cv2
import numpy as np
import tensorflow as tf
from sklearn.utils import shuffle
from tqdm import tqdm

from superai.meta_ai import BaseModel
from superai.meta_ai.base.base_ai import add_default_tracking, default_random_seed
from superai.meta_ai.base.training_helpers import (
    AvailableCallbacks,
    DefaultCallbackFactory,
    get_tensorboard_tracking_path,
)
from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters
from superai.meta_ai.schema import TrainerOutput

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

directory_to_extract_to = "./directory"


class IntelImageClassification(BaseModel):
    def __init__(self, **kwargs):
        super(IntelImageClassification, self).__init__(**kwargs)
        self.class_names = ["mountain", "street", "glacier", "buildings", "sea", "forest"]
        self.class_names_label = {class_name: i for i, class_name in enumerate(self.class_names)}
        self.nb_classes = len(self.class_names)
        self.IMAGE_SIZE = (150, 150)

    @staticmethod
    def get_training_path(path_to_zipped_file: str) -> Tuple[str, str]:
        """
        Creates training and testing paths
        :param path_to_zipped_file:
        :return:
        """
        return (
            os.path.join(path_to_zipped_file, "seg_train/seg_train"),
            os.path.join(path_to_zipped_file, "seg_test/seg_test"),
        )

    def load_data(self, train_path, test_path):
        """
        Load the data:
            - 14,034 images to train the network.
            - 3,000 images to evaluate how accurately the network learned to classify images.
        """

        datasets = [train_path, test_path]
        output = []

        # Iterate through training and test sets
        for dataset in datasets:

            images = []
            labels = []

            print("Loading {}".format(dataset))

            # Iterate through each folder corresponding to a category
            for folder in os.listdir(dataset):
                try:
                    label = self.class_names_label[folder]

                    # Iterate through each image in our folder
                    for file in tqdm(os.listdir(os.path.join(dataset, folder))):
                        # Get the path name of the image
                        img_path = os.path.join(os.path.join(dataset, folder), file)

                        # Open and resize the img
                        image = cv2.imread(img_path)
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        image = cv2.resize(image, self.IMAGE_SIZE)

                        # Append the image and its corresponding label to the output
                        images.append(image)
                        labels.append(label)
                except Exception as e:
                    logger.exception(e)

            images = np.array(images, dtype="float32")
            labels = np.array(labels, dtype="int32")

            output.append((images, labels))

        return output

    def load_weights(self, weights_path: str):
        """Might be good for some fancy transfer learning"""

    def predict(self, inputs, context=None):
        pass

    @add_default_tracking
    def train(
        self,
        model_save_path,
        training_data,
        validation_data=None,
        test_data=None,
        production_data=None,
        weights_path=None,
        encoder_trainable: bool = True,
        decoder_trainable: bool = True,
        hyperparameters: HyperParameterSpec = None,
        model_parameters: ModelParameters = None,
        callbacks=None,
        random_seed=default_random_seed,
    ) -> TrainerOutput:
        """
        Training algorithm implementation

        :param model_save_path: Save location of model
        :param training_data: Points to the local directory where training data is stored
        :param validation_data: Points to the local directory where validation data is stored
        :param test_data: Points to the local directory where test data is stored
        :param production_data: Points to the local directory where production data is stored
        :param weights_path: Points to where transfer learning weights are stored
        :param encoder_trainable:
        :param decoder_trainable:
        :param hyperparameters:
        :param model_parameters:
        :param callbacks:
        :param random_seed:
        :return:
        """
        if callbacks is None or isinstance(callbacks, str):
            callbacks = []

        # Load data
        logger.info(f"Loading data from {training_data}")
        training_data_path, test_data_path = self.get_training_path(training_data)
        (train_images, train_labels), (test_images, test_labels) = self.load_data(training_data_path, test_data_path)
        train_images, train_labels = shuffle(train_images, train_labels, random_state=random_seed)
        logger.info("Dataset prepared")

        # Prepare model
        logger.info("Preparing model...")
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Conv2D(
                    model_parameters.conv1_size,
                    (3, 3),
                    activation="relu",
                    input_shape=(self.IMAGE_SIZE[0], self.IMAGE_SIZE[1], 3),
                ),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Conv2D(model_parameters.conv2_size, (3, 3), activation="relu"),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(model_parameters.dense_size, activation=tf.nn.relu),
                tf.keras.layers.Dense(self.nb_classes, activation=tf.nn.softmax),
            ]
        )
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

        # setup callbacks
        logger.info("Preparing callbacks...")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=get_tensorboard_tracking_path())
        callbacks.extend([tensorboard_callback, DefaultCallbackFactory.get_default_callback(AvailableCallbacks.Keras)])

        # start training
        logger.info("Starting training...")
        history = model.fit(
            train_images,
            train_labels,
            batch_size=hyperparameters.batch_size,
            epochs=hyperparameters.epochs,
            validation_split=hyperparameters.validation_split,
            callbacks=callbacks,
        )
        accuracy = model.evaluate(test_images, test_labels)[1]

        # track and save
        if not os.path.exists(model_save_path):
            os.makedirs(model_save_path)
        model.save(model_save_path)
        logger.info(f"Training complete, saved model in {model_save_path}")

        return TrainerOutput(metric=dict(eval_accuracy=accuracy))
