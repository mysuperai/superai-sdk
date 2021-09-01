import os
import shutil
import time
import uuid

from docs.examples.ai.utilities import MockedReturns
from superai.data_program import Project, Worker
from superai.meta_ai import AI
from superai.meta_ai.ai import Orchestrator, LocalPredictor, AWSPredictor, list_models, AITemplate
from superai.meta_ai.parameters import HyperParameterSpec, String, Config
from superai.meta_ai.schema import Image, SingleChoice, Schema
from superai.utils import log

###########################################################################
# Cleanup
###########################################################################

if os.path.exists(".AISave"):
    shutil.rmtree(".AISave")


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
    model_class="MyKerasModel",
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
    model_class="MyKerasModel",
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
)

predictor: LocalPredictor = ai.deploy(orchestrator=Orchestrator.LOCAL_DOCKER, skip_build=False)

time.sleep(5)
log.info(
    "Local predictions: {}".format(
        predictor.predict(
            input={"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
        ),
    )
)
predictor.container.stop()
ai.push_model("my_mnist_model", "2")

###########################################################################
# Specify hyperparameters and model parameters
###########################################################################

new_template = AITemplate(
    input_schema=ai_definition["input_schema"],
    output_schema=ai_definition["output_schema"],
    configuration=Config(padding=String(default="valid")),
    model_class="MyEncodeDecodeModel",
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
        epochs=1,
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
        epochs=1,
        learning_rate=0.001,
        batch_size=64,
    ),
    encoder_trainable=False,
    decoder_trainable=True,
)


###########################################################################
# Push and save model in s3
###########################################################################

# Push and create entry in database
my_ai.push(update_weights=True)


###########################################################################
# Load and Create AI
###########################################################################
local_loaded_ai = AI.load(
    ".AISave/my_mnist_model/1",
    weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
)
log.info(local_loaded_ai)

s3_loaded_ai: AI = AI.load(
    path="s3://canotic-ai/meta_ai_models/my_mnist_model/1/AISavedModel.tar.gz",
    weights_path="s3://canotic-ai/meta_ai_models/saved_models/my_model.tar.gz",
)
log.info(
    "S3 predictions : {}".format(
        s3_loaded_ai.predict(
            {"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
        )
    )
)
with m.s3 as s3, m.list as lm:
    db_loaded_ai: AI = AI.load("model://my_mnist_model/1")
log.info(f"S3 loaded {s3_loaded_ai}")
log.info(f"DB loaded {db_loaded_ai}")

###########################################################################
# Predict
###########################################################################
inputs = {"data": {"image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}}
result = local_loaded_ai.predict(inputs=inputs)
log.info(f"Result : {result}")

assert s3_loaded_ai.predict(inputs=inputs) == result, "Results should be same"

predictor: LocalPredictor = my_ai.deploy(orchestrator=Orchestrator.LOCAL_DOCKER, skip_build=True)
time.sleep(5)
log.info(f"Local predictions: {predictor.predict(input=inputs)}")
predictor.container.stop()

with m.push as p, m.sage_check(True) as sc, m.sage_pred as sp:
    predictor: AWSPredictor = my_ai.deploy(orchestrator=Orchestrator.AWS_SAGEMAKER)
    log.info(f"AWS Predictions: {predictor.predict(input=inputs)}")

# might not be required for lambdas
with m.sage_check(False) as sch, m.undep as ud:
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
    my_ai.train(
        model_save_path="s3://some_model_path", training_data="s3://some_training_data", mode=Orchestrator.AWS_SAGEMAKER
    )


###########################################################################
# Model Database operations
# Note: Works with running local hasura deployment, Please clean the
# database to run the following mocks, in the future all caveats will be
# handled
###########################################################################

# list all models
log.info(f"All models with name {model_name}\n" + list_models(model_name))

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
# log.info(f"Checkout the new version: {another_ai.version}")

# Transitions version 1 to `"production"` stage
transitioned_ai = my_ai.transition_ai_version_stage(version=1, stage="PROD")
log.info(transitioned_ai)

# Updates the weights_path and creates a new ai version
loaded_ai.update_weights_path(weights_path="./new_path")

# Increases version
my_ai.update_ai_class(model_class="MyEncodeDecodeModel")

# Creates a new version (if version 3 already exists this method throws an error).
my_ai.update(version=5, stage="PROD", weights_path="./new_path", ai_class="MyTrackerModel")

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
