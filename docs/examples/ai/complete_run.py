import datetime
import json
import os
import shutil
import time
import uuid
from urllib.request import urlopen

import cv2
import numpy as np
import superai_schema.universal_schema.task_schema_functions as df
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from docs.examples.ai.utilities import MockedReturns, color
from superai.data_program import Project, Worker
from superai.meta_ai import AI, BaseModel
from superai.meta_ai.ai import Mode, LocalPredictor, AWSPredictor, list_models, AITemplate
from superai.meta_ai.parameters import HyperParameterSpec, String, Config
from superai.meta_ai.schema import Image, SingleChoice, Schema
from superai.utils import log

###########################################################################
# Cleanup
###########################################################################

if os.path.exists(".AISave"):
    shutil.rmtree(".AISave")


###########################################################################
# Model Classes used in all mocks
###########################################################################


class MyKerasModel(BaseModel):
    model = None

    def __init__(self, *args, **kwargs):
        super(MyKerasModel, self).__init__(*args, **kwargs)

    def load_weights(self, weights_path):
        log.info("Loading weights")
        self.model = keras.models.load_model(weights_path)

    def predict(self, input):
        log.info("Predict Input: ", input)
        image_url = input["my_image"]["image_url"]
        req = urlopen(image_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
        input = np.reshape(img, (1, 28 * 28))
        pred = self.model.predict(input)
        output = np.argmax(pred[0])
        return [
            {
                "mnist_class": df.exclusive_choice(
                    choices=list(map(str, range(10))),
                    selection=int(output),
                )
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

        log.info("Fit model on training data")
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
        image_url = input["my_image"]["image_url"]
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
                "mnist_class": df.exclusive_choice(
                    choices=list(map(str, range(10))),
                    selection=int(input),
                )
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


###########################################################################
# Create AI
###########################################################################

model_name = "my_mnist_model"
ai_definition = {
    "input_schema": Schema(my_image=Image()),
    "output_schema": Schema(
        my_choice=SingleChoice(
            default="0",
            choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        )
    ),
}

my_ai_template = AITemplate(
    input_schema=ai_definition["input_schema"],
    output_schema=ai_definition["output_schema"],
    configuration=Config(padding=String(default="valid")),
    model_class=MyKerasModel,
    name="my_awesome_template",
    description="Template for the MNIST model experiment with AI tool",
    requirements=["tensorflow", "opencv-python-headless"],
)

my_ai = AI(
    ai_template=my_ai_template,
    input_params=my_ai_template.input_schema.parameters(),
    output_params=my_ai_template.input_schema.parameters(
        choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    ),
    configuration=my_ai_template.configuration(
        conv_layers=None,
        num_conv_layers=None,
        filter_size=3,
        num_filters=32,
        strides=(1, 1),
        padding="valid",
        dilation_rate=(1, 1),
        conv_use_bias=True,
    ),
    name=model_name,
    version=1,
    weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
    description="My super fancy AI model instance",
)
log.info(my_ai)
log.info(os.system("tree .AISave"))

# for mocking
m = MockedReturns(my_ai)

###########################################################################
# Build Image
###########################################################################

template = AITemplate(
    input_schema=Schema(),
    output_schema=Schema(),
    configuration=Config(),
    model_class=MyKerasModel,
    name="My_template",
    description="Template for my new awesome project",
    requirements=["tensorflow==2.1.0", "opencv-python-headless"],
    artifacts={"run": "runDir/run_this.sh"},
    code_path=["resources/runDir"],
)
ai = AI(
    ai_template=template,
    input_params=template.input_schema.parameters(),
    output_params=template.output_schema.parameters(choices=[str(x) for x in range(10)]),
    name="my_mnist_model",
    version=2,
    weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
    model_class=MyKerasModel,
)

predictor: LocalPredictor = ai.deploy(mode=Mode.LOCAL)

time.sleep(5)
log.info(
    color(
        "Local predictions: {}".format(
            predictor.predict(
                input={
                    "my_image": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}
                }
            ),
        )
    )
)
predictor.container.stop()

###########################################################################
# Specify hyperparameters and model parameters
###########################################################################

new_template = AITemplate(
    input_schema=ai_definition["input_schema"],
    output_schema=ai_definition["output_schema"],
    configuration=Config(padding=String(default="valid")),
    model_class=MyEncodeDecodeModel,
    name="my_new_awesome_template",
    description="Template for the MNIST model experiment with AI tool, containing encoder decoder",
    requirements=["tensorflow", "opencv-python-headless"],
)

ai_with_hypes = AI(
    ai_template=new_template,
    input_params=new_template.input_schema.parameters(),
    output_params=new_template.output_schema.parameters(choices=[str(x) for x in range(10)]),
    name="my_mnist_model_with_hyperparameters",
    version=1,
    description="Model with encoder and decoder structure to be trained",
)

ai_with_hypes.train(
    model_save_path=".AISave/hypedModel/cp.ckpt",
    training_data=None,
    hyperparameters=HyperParameterSpec(
        trainable=True,
        epochs=3,
        learning_rate=0.001,
        batch_size=64,
    ),
    encoder_trainable=True,
    decoder_trainable=True,
)

model_1 = ai_with_hypes.model_class.to_tf()

# setting decoder_trainable as False
new_hyped_model = AI(
    ai_template=new_template,
    input_params=new_template.input_schema.parameters(),
    output_params=new_template.output_schema.parameters(choices=[str(x) for x in range(10)]),
    name="my_mnist_model_with_hyperparameters",
    version=2,
    description="Model with encoder and decoder structure trained",
    weights_path=".AISave/hypedModel/cp.ckpt",
)

# Note the loss dips
new_hyped_model.train(
    model_save_path=".AISave/newHypedModel",
    training_data=None,
    hyperparameters=HyperParameterSpec(
        trainable=True,
        epochs=3,
        learning_rate=0.001,
        batch_size=64,
    ),
    encoder_trainable=False,
    decoder_trainable=True,
)

###########################################################################
# Load and Create AI
###########################################################################
local_loaded_ai = AI.load(
    ".AISave/my_mnist_model/1",
    weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
)
log.info(local_loaded_ai)

with m.s3 as s3, m.list as lm:
    s3_loaded_ai: AI = AI.load("s3://my_mnist_model/1")
    db_loaded_ai: AI = AI.load("model://my_mnist_model/1")
log.info(color(f"S3 loaded {s3_loaded_ai}"))
log.info(color(f"DB loaded {db_loaded_ai}"))

###########################################################################
# Predict
###########################################################################
inputs = {"my_image": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
result = local_loaded_ai.predict(input=inputs)
log.info(color(f"Result : {result}"))

assert s3_loaded_ai.predict(input=inputs) == result, "Results should be same"

# with m.local as l:
predictor: LocalPredictor = my_ai.deploy(mode=Mode.LOCAL)
log.info(color(f"Local predictions: {predictor.predict(input=inputs)}"))

with m.push as p, m.sage_check(True) as sc, m.sage_pred as sp:
    predictor: AWSPredictor = my_ai.deploy(mode=Mode.AWS)
    log.info(color(f"AWS Predictions: {predictor.predict(input=inputs)}"))

# might not be required for lambdas
with m.sage_check(False) as sc, m.undep as ud:
    my_ai.undeploy()
    try:
        log.info(f"AWS Predictions: { predictor.predict(input=inputs)}")
    except LookupError as e:
        pass

###########################################################################
# Train
###########################################################################
my_ai.train(model_save_path=".AISave/new_model", training_data=None)
loaded_ai = AI(
    ai_template=my_ai_template,
    input_params=my_ai_template.input_schema.parameters(),
    output_params=my_ai_template.input_schema.parameters(
        choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    ),
    name=model_name,
    version=3,
    weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
    description="My super fancy AI model instance",
)
predictions = loaded_ai.predict(inputs)
log.info(f"Result : {predictions}")

with m.train as t:
    # Mocked, does not do anything
    my_ai.train(model_save_path="s3://some_model_path", training_data="s3://some_training_data", mode=Mode.AWS)


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


###########################################################################
# Model Database operations
# Note: Works with running local hasura deployment, Please clean the
# database to run the following mocks, in the future all caveats will be
# handled
###########################################################################
# Push and create entry in database
my_ai.push()

# list all models
log.info(color(f"All models with name {model_name}"), list_models(model_name))

# another_ai = AI(
#     ai_definition=ai_definition,
#     name=model_name,
#     version=1,
#     weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
#     requirements=["tensorflow", "opencv-python-headless"],
#     model_class=MyKerasModel,
#     description="My super fancy AI model",
# )
#
# log.info(color(f"Checkout the new version: {another_ai.version}"))

# Transitions version 1 to `"production"` stage
transitioned_ai = my_ai.transition_ai_version_stage(version=1, stage="PROD")
log.info(transitioned_ai)

# Updates the weights_path and creates a new ai version
loaded_ai.update_weights_path(weights_path="./new_path")


class MyClass(BaseModel):
    pass


# Increases version
my_ai.update_ai_class(ai_class=MyClass)

# Creates a new version (if version 3 already exists this method throws an error).
my_ai.update(version=5, stage="PROD", weights_path="./new_path", ai_class=MyClass)

#######################################################################################
# ADDING TO PROJECT
#######################################################################################

DP_NAME = "MyFirstAI" + str(uuid.getnode())
dp_definition = None
# Creating a Project.
project = Project(
    dp_name=DP_NAME,
    dp_definition=dp_definition,
    params={
        "instructions": "My simple instructions",
        "choices": [f"{i}" for i in range(10)],
    },
)

project.add_ai(my_ai, active_learning=True)

# Send some data for labeling
mnist_urls = [
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/RandomBitmap.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/Brain.jpg",
]

inputs = [{"mnist_image_url": url} for url in mnist_urls]

labels = project.process(inputs=inputs, worker=Worker.ai, open_browser=False)
