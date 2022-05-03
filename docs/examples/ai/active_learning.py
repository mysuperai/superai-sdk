import os
import shutil
import uuid

import superai_schema.universal_schema.data_types as dt

from superai.data_program import Project, Worker
from superai.meta_ai import AI
from superai.meta_ai.ai import AITemplate
from superai.meta_ai.parameters import Config
from superai.meta_ai.schema import Schema
from superai.utils import log

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
    name="My_template",
    description="Template for my new awesome project",
    model_class="MyKerasModel",
    requirements=["tensorflow==2.1.0", "opencv-python-headless"],
    code_path=["resources/runDir"],
    artifacts={"run": "runDir/run_this.sh"},
)
ai1 = AI(
    ai_template=template,
    input_params=template.input_schema.parameters(),
    output_params=template.output_schema.parameters(choices=[str(x) for x in range(10)]),
    name="my_mnist_model",
    version=2,
    weights_path=os.path.join(os.path.dirname(__file__), "resources/my_model"),
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


# Increases version
ai1.update_ai_class(model_class="MyEncodeDecodeModel")

# Creates a new version (if version 3 already exists this method throws an error).
ai1.update(version=3, stage="PROD", weights_path="./new_path", ai_class="MyEncodeDecodeModel")

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
