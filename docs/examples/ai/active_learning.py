import json
import os
import shutil
import uuid
from urllib.request import urlopen

import cv2
import numpy as np
import superai_schema.universal_schema.data_types as dt
import superai_schema.universal_schema.task_schema_functions as df
from tensorflow import keras
from tensorflow.keras import layers

from superai.data_program import Project, Worker
from superai.meta_ai import AI
from superai.meta_ai.ai import AITemplate
from superai.meta_ai.base import BaseModel
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema
from superai.utils import log


class MyKerasModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super(MyKerasModel, self).__init__(*args, **kwargs)

    def load_weights(self, weights_path):
        self.model = keras.models.load_model(weights_path)

    def predict(self, input):
        log.info(input)
        image_url = input["data"]["image_url"]
        req = urlopen(image_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
        input = np.reshape(img, (1, 28 * 28))
        pred = self.model.predict(input)
        output = np.argmax(pred[0])
        return {
            "prediction": df.exclusive_choice(choices=list(map(str, range(10))), selection=int(output)),
            "score": float(pred[0][int(output)]),
        }

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
        with open(os.path.join(model_save_path, "experiments/model_config.json"), "w") as json_writer:
            json.dump(json_config, json_writer)

    @staticmethod
    def define_model():
        inputs = keras.Input(shape=(784,), name="digits")
        x = layers.Dense(64, activation="relu", name="dense_1")(inputs)
        x = layers.Dense(64, activation="relu", name="dense_2")(x)
        outputs = layers.Dense(10, activation="softmax", name="predictions")(x)

        model = keras.Model(inputs=inputs, outputs=outputs)

        return model


###########################################################################
# Cleanup
###########################################################################

if os.path.exists(".AISave"):
    shutil.rmtree(".AISave")


# TODO: revert back to outside the function
# Register an AI. Similar to a Data Program, an AI specifies the schema that all the models are subject to. In this
# step we only define the AI schema, version and metadata, so far we haven't register an AIModel
ai_definition = {
    "input_schema": Schema(my_image=dt.IMAGE),
    "output_schema": Schema(mnist_class=dt.EXCLUSIVE_CHOICE),
}


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
ai1 = AI(
    ai_template=template,
    input_params=template.input_schema.parameters(),
    output_params=template.output_schema.parameters(choices=[str(x) for x in range(10)]),
    name="my_mnist_model",
    version=2,
    weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
    model_class=MyKerasModel,
)

log.info(
    "Prediction from AI : {}".format(
        ai1.predict(
            inputs={"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
        ),
    )
)

# Push model to S3 and create an entry in DB
ai1.push()

# Transitions version 1 to `"production"` stage
ai1.transition_ai_version_stage(version=1, stage="PROD")

# Updates the weights_path and creates a new ai version
ai1.update_weights_path(weights_path="./new_path")


class MyClass(BaseModel):
    pass


# Increases version
ai1.update_ai_class(ai_class=MyClass)

# Creates a new version (if version 3 already exists this method throws an error).
ai1.update(version=3, stage="PROD", weights_path="./new_path", ai_class=MyClass)

# Loads model
ai2 = AI.load_local(
    ".AISave/my_keras_mnist_ai/DEV/1",
    weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
)
log.info(
    "Prediction from loaded AI : {}".format(
        ai2.predict(
            inputs={"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
        ),
    )
)

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

project.add_ai(ai1, active_learning=True)

# Send some data for labeling
mnist_urls = [
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/RandomBitmap.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/Brain.jpg",
]

inputs = [{"mnist_image_url": url} for url in mnist_urls]

labels = project.process(inputs=inputs, worker=Worker.me, open_browser=True)
