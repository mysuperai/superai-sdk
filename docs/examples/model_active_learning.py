import uuid

import superai_schema.universal_schema.data_types as dt
from superai.data_program import Project, Worker
from superai.metaai import AI
from superai.metaai.base import BaseAI
from superai_schema.universal_schema.data_types import bundle as Schema


class MyModel(BaseAI):
    def __init__(self):
        super().__init__()

    def load_weights(cls, weights_path):
        if self.model is None:
            print("Model Content : ", os.listdir(weights_path))
            # Local path to trained weights file
            COCO_MODEL_PATH = weights_path

            # Create model object in inference mode.
            model = modellib.MaskRCNN(mode="inference", model_dir=os.path.join("logs"), config=config)

            # Load weights trained on MS-COCO
            model.load_weights(COCO_MODEL_PATH, by_name=True)

    def preprocess(self, request):
        return request

    def postprocess(self, inference_output):
        return inference_output

    def predict(self, input):
        return self.model.predict(input)

    def train(self, input_data_path, model_save_path, hyperparams_path=None):
        pass


# Register an AI. Similar to a Data Program, an AI specifies the schema that all the models are subject to. In this
# step we only define the AI schema, version and metadata, so far we haven't register an AIModel
ai_definition = {
    "input_schema": Schema(my_image=dt.IMAGE),
    "output_schema": Schema(mnist_class=dt.EXCLUSIVE_CHOICE),
}

ai1 = AI(
    ai_definition=ai_definition,  # immutable
    name="my_instance_segmentation_ai",
    version=1,
    stage="development",
    description="cool model",
    ai_class=MyModel,
    weights_path="mask_rcnn_coco_v01.h5",
)

# Transitions version 1 to `"production"` stage
ai1.transition_model_version_stage(version=1, stage="production")

# Updates the weights_path and creates a new ai version
ai1.update_weights_path(weights_path="./new_path")

# Increases version
ai1.update_ai_class(ai_class=MyClass)

# Creates a new version (if version 3 already exists this method throws an error).
ai1.update(version=3, stage="Production", weights_path="./new_path", ai_class=MyClass)

# Loads model
ai2 = AI.load("model:/my_instance_segmentation_ai/production")

#######################################################################################


DP_NAME = "MyFirstAI" + str(uuid.getnode())

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
