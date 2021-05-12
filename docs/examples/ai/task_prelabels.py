import uuid

import superai_schema.universal_schema.data_types as dt
import superai_schema.universal_schema.task_schema_functions as df
from superai_schema.universal_schema.data_types import bundle as Schema
from superai.data_program import DataProgram, Project, Task, Worker
from superai.meta_ai import AI
from superai.meta_ai.base import BaseModel

from superai.data_program import Project, DataProgram, Worker, Task

# Defining the dataprogram interface
dp_definition = {
    "input_schema": Schema(mnist_image_url=dt.IMAGE),
    "parameter_schema": Schema(instructions=dt.TEXT, choices=dt.array_to_schema(dt.TEXT, min_items=0)),
    "output_schema": Schema(mnist_class=dt.EXCLUSIVE_CHOICE),
}

# Using uuid.getnode() to get a unique name for your first dataprogram
DP_NAME = "MyFirstWorkflow" + str(uuid.getnode())

# Creating a dataprogram object
dp = DataProgram(name=DP_NAME, definition=dp_definition, add_basic_workflow=False)

task_definition = {
    "input_schema": Schema(instructions=dt.TEXT, mnist_image_url=dt.IMAGE),
    "output_schema": Schema(mnist_class=dt.EXCLUSIVE_CHOICE),
}

# Model ran by superai
ai1 = AI.load("model:/my_number_recognizer/latest")
t1 = Task(name="is_number", definition=task_definition, max_attempts=3)
# Adds an AI in a specific stage (defined in the URI) to the task.
t1.add_ai(ai1)

ai2 = AI.load("model:/my_mnist_classifier/3")
t2 = Task(name="choose_number", definition=task_definition, max_attempts=100)
# Adds an AI in a specific version (defined in the URI) to the task.
t2.add_ai(ai2)

# Registering tasks to DP
dp.add_task(t1)
dp.add_task(t2)

# Here we create our first workflow function
# Not injecting AI list in V0
def my_workflow(inputs, params, predictions, tasks, **kwargs):
    """
    Simple hello world MNIST workflow
    :param inputs:
    :return:
    """
    print(f"{dp.name}.my_workflow: Arguments: inputs {inputs} params: {params}, **kwargs: {kwargs} ")

    task1 = tasks.get("is_number")
    task1_inputs = [
        df.text("Is this image a number"),
        df.image(inputs.get("mnist_image_url")),
    ]
    task1_outputs = [df.exclusive_choice(choices=["yes", "no"])]
    task1.process(task_inputs=task1_inputs, task_outputs=task1_outputs)
    task1_response = task1.output.get("values", [])[0].get("schema_instance")

    if task1_response.get("selection", {}).get("value") == "yes":
        task2 = tasks.get("choose_number")
        task2_inputs = [
            df.text("Choose the correct number"),
            df.image(inputs.get("mnist_image_url")),
        ]
        task2_outputs = [df.exclusive_choice(choices=params.get("choices", []))]
        task2(task_inputs=task2_inputs, task_outputs=task2_outputs)
    else:
        return {"mnist_class": {"choices": df.build_choices(params.get("choices", []))}}

    return {"mnist_class": task2.output.get("values", [])[0].get("schema_instance")}


# Registering the workflow function to the dataprogram
my_mnist_workflow_1 = dp.add_workflow(my_workflow, name="my_mnist_workflow_1", default=True)

# ------------------------------------------------------------------------------------
# Create a new Project project
project = Project(
    dataprogram=dp,
    name="FirstSuperAIWorfklow",
    params={
        "instructions": "Select the appropriate class for the MNIST image",
        "choices": ["0", "1", "2", "3"],
    },
    uuid="b568d0eb-d27b-4da2-898a-e20780d56348",
)

# Send some data for labeling
mnist_urls = [
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/RandomBitmap.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/Brain.jpg",
]

inputs = [{"mnist_image_url": url} for url in mnist_urls]

labels = project.process(inputs=inputs, worker=Worker.me, open_browser=True)
