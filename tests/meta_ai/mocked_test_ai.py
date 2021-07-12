"""
These tests need tensorflow==2.1.0 and opencv-python-headless to run. That is why they are excluded from normal tests.
"""

import json
import logging
import os
import shutil
import time
from urllib.request import urlopen

import cv2
import numpy as np
import pytest
import superai_schema.universal_schema.task_schema_functions as df
import vcr
from tensorflow import keras
from tensorflow.keras import layers

import superai
from superai import DeploymentApiMixin, ModelApiMixin, ProjectAiApiMixin
from superai.meta_ai import BaseModel
from superai.meta_ai.ai import AI, Mode, DeployedPredictor, LocalPredictor, AWSPredictor, AITemplate
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema
from superai.utils import log
from tests.apis.test_meta_ai import APP_ID, scrub_string, before_record_cb

weights_path = os.path.join(os.path.dirname(__file__), "../../docs/examples/ai/resources/my_model")


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


my_vcr = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="fixtures/cassettes",
    record_mode="once",
    match_on=["body", "headers", "method"],
    filter_headers=["x-api-key", "x-app-id", "Content-Length", "User-Agent"],
    before_record_response=scrub_string(APP_ID, "FAKE_APP_ID"),
    before_record_request=before_record_cb,
    decode_compressed_response=True,
)


@pytest.fixture()
def model_api():
    with my_vcr.use_cassette("model_api.yaml"):
        yield ModelApiMixin()


@pytest.fixture()
def ai_api():
    with my_vcr.use_cassette(
        "ai_api.yaml",
    ):
        yield ProjectAiApiMixin()


@pytest.fixture()
def cleanup():
    if os.path.exists(".AISave"):
        shutil.rmtree(".AISave")


@pytest.fixture()
def ai(cleanup):
    template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        model_class=MyKerasModel,
        name="My_template",
        description="Template for my new awesome project",
        requirements=["tensorflow==2.1.0", "opencv-python-headless"],
    )
    ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=[str(x) for x in range(10)]),
        name="my_mnist_model",
        version=1,
        weights_path=weights_path,
        model_class=MyKerasModel,
    )
    yield ai
    # delete contents of folder
    del ai


def test_create_model(model_api, caplog):
    # TODO: Fix logging
    caplog.set_level(logging.INFO)
    model_name = "my_mnist_model"

    template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        model_class=MyKerasModel,
        name="My_template",
        description="Template for my new awesome project",
        requirements=["tensorflow==2.1.0", "opencv-python-headless"],
    )
    my_ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=[str(x) for x in range(10)]),
        name="my_mnist_model",
        version=2,
        weights_path=weights_path,
        model_class=MyKerasModel,
    )
    assert type(my_ai) == AI
    shutil.rmtree(".AISave")


def test_load_ai_local(ai, caplog):
    # we are loading a fixture which creates a ai class in .AISave/my_mnist_model
    caplog.set_level(logging.INFO)

    ai2 = AI.load(".AISave/my_mnist_model/1", weights_path=weights_path)
    ai3 = AI.load_local(".AISave/my_mnist_model/1", weights_path=weights_path)
    print(ai2)
    print(ai3)
    assert ai2 == ai3
    # assert ai == ai2 == ai3 # TODO: Match the schema dictionaries to pass this


def test_mock_load_from_model_hub(ai, monkeypatch):
    monkeypatch.setattr(
        superai.meta_ai.ai,
        "list_models",
        lambda *a, **k: [
            {
                "name": "my_mnist_model",
                "stage": "DEV",
                "version": "1",
                "description": None,
                "modelSavePath": "s3://my_mnist_model/1",
                # so that we can test the local loading aspect of s3 loading
            }
        ],
    )
    # TODO: replace above patch with a VCS call.
    monkeypatch.setattr(AI, "load_from_s3", lambda path: AI.load_local(".AISave/" + path.split("s3://")[-1]))

    ai2 = AI.load("model://my_mnist_model/1")
    assert ai2


def test_mock_load_from_s3(ai, monkeypatch):
    monkeypatch.setattr(AI, "load_from_s3", lambda path, other: AI.load_local(".AISave/" + path.split("s3://")[-1]))

    ai2 = AI.load("s3://my_mnist_model/1")
    assert ai2


def test_transition_ai_version_stage():
    # TODO: Yet to implement
    pass


def test_mock_deploy_local(ai, monkeypatch):
    monkeypatch.setattr(AI, "build_image", lambda *a, **k: None)
    predictor = ai.deploy(mode=Mode.LOCAL)
    # standard type checks
    assert type(predictor) == LocalPredictor
    assert issubclass(type(predictor), DeployedPredictor)


@pytest.mark.skip("TODO")
def test_mock_deploy_sagemaker(ai, monkeypatch):
    monkeypatch.setattr(AI, "build_image", lambda *a, **k: None)
    monkeypatch.setattr(AI, "push_model", lambda *a, **k: None)

    predictor = ai.deploy(mode=Mode.AWS)
    # standard type checks
    assert type(predictor) == AWSPredictor
    assert issubclass(type(predictor), DeployedPredictor)
    assert predictor.endpoint_name == ai.name


def test_predict(ai):
    # needs ai to be loaded with weights
    result = ai.predict(
        inputs={"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
    )
    print("Result : ", result)
    assert result


def test_mock_predict_from_local_deployment(ai, monkeypatch):
    monkeypatch.setattr(LocalPredictor, "predict", ai.predict)
    monkeypatch.setattr(AI, "build_image", lambda *a, **k: None)
    predictor = ai.deploy(mode=Mode.LOCAL)

    assert predictor
    prediction = predictor.predict(
        {"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
    )
    print(prediction)
    assert prediction


@pytest.mark.skip("TODO")
def test_mock_predict_from_sagemaker(ai, monkeypatch):
    monkeypatch.setattr(AI, "build_model", lambda *a, **k: None)
    monkeypatch.setattr(AI, "push_model", lambda *a, **k: None)
    monkeypatch.setattr(AWSPredictor, "predict", ai.predict)
    predictor = ai.deploy(mode=Mode.AWS)
    assert predictor
    prediction = predictor.predict(
        {"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
    )  # TODO: pass kwarg input_data

    print(prediction)
    assert prediction


def test_predict_from_sagemaker(cleanup, caplog):
    caplog.set_level(logging.INFO)
    template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        model_class=MyKerasModel,
        name="Genre_Template",
        description="Template for genre models",
        requirements=["torch>=1.6"],
    )

    ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(),
        name="genre_model",
        version=2,
        weights_path=".",
    )

    predictor: LocalPredictor = ai.deploy(mode=Mode.AWS, skip_build=True, lambda_mode=False)
    # predictor.log()
    time.sleep(5)

    log.info(
        "Local predictions: {}".format(
            predictor.predict(input={"data": {"sentences": ["Einstein was a [START_ENT] German [END_ENT] physicist."]}})
        )
    )


def test_train_and_predict(cleanup):
    # can check if weights file is generated.
    template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        model_class=MyKerasModel,
        name="My_template",
        description="Template for my new awesome project",
        requirements=["tensorflow", "opencv-python-headless"],
    )
    ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=map(str, range(0, 10))),
        name="my_mnist_model",
        version=1,
        model_class=MyKerasModel,
    )
    model_weights_path = ".AISave/my_model"
    ai.train(model_weights_path, None)

    assert os.path.exists(model_weights_path)
    model_name = "my_mnist_model"
    my_ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=map(str, range(0, 10))),
        name=model_name,
        version=2,
        model_class=MyKerasModel,
        weights_path=model_weights_path,
    )
    result = my_ai.predict(
        inputs={"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
    )
    print("Result : ", result)
    assert result


def test_write_dockerfile(ai):
    ai._create_dockerfile()
    assert os.path.exists(os.path.join(ai._location, "handler.py"))


@pytest.mark.skip("Prevent docker in docker")
def test_build_image():
    template = AITemplate(
        input_schema=Schema(),
        output_schema=Schema(),
        configuration=Config(),
        model_class=MyKerasModel,
        name="My_template",
        description="Template for my new awesome project",
        requirements=["tensorflow", "opencv-python-headless"],
        artifacts={"run": "runDir/run_this.sh"},
        code_path=["resources/runDir"],
    )
    ai = AI(
        ai_template=template,
        input_params=template.input_schema.parameters(),
        output_params=template.output_schema.parameters(choices=map(str, range(0, 10))),
        name="my_mnist_model",
        version=1,
        weights_path=os.path.join(os.path.dirname(__file__), "../experiments/my_model"),
        model_class=MyKerasModel,
    )
    ai._create_dockerfile()
    image_name = "test_build_image"
    ai.build_image(image_name)
    os.system(f"docker inspect --type=image {image_name}")


def test_create_endpoint(ai, monkeypatch):
    monkeypatch.setattr(AI, "_create_dockerfile", lambda *a, **k: None)
    monkeypatch.setattr(AI, "push_model", lambda *a, **k: None)
    monkeypatch.setattr(DeploymentApiMixin, "check_endpoint_is_available", lambda *a, **k: True)

    predictor = ai.deploy(mode=Mode.AWS)
    assert type(predictor) == AWSPredictor
    assert hasattr(predictor, "predict")

    monkeypatch.setattr(DeploymentApiMixin, "predict_from_endpoint", lambda *a, **k: 20)
    assert predictor.predict({"some": "data"}) == 20


def test_delete_endpoint(ai, monkeypatch):
    monkeypatch.setattr(DeploymentApiMixin, "undeploy", lambda *a, **k: (True, ""))
    res = ai.undeploy()
    assert res