import uuid

import superai_schema.universal_schema.data_types as dt
import superai_schema.universal_schema.task_schema_functions as df

from superai.data_program import Project, DataProgram, Worker, Task

# Defining the dataprogram interface
dp_definition = {
    "input_schema": dt.bundle(mnist_image_url=dt.IMAGE),
    "parameter_schema": dt.bundle(instructions=dt.TEXT, choices=dt.array_to_schema(dt.TEXT, min_items=0)),
    "output_schema": dt.bundle(mnist_class=dt.EXCLUSIVE_CHOICE),
}

# Using uuid.getnode() to get a unique name for your first dataprogram
DP_NAME = "MyFirstWorkflow" + str(uuid.getnode())

# Creating a dataprogram object
dp = DataProgram(name=DP_NAME, definition=dp_definition, add_basic_workflow=False)

# Here we create our first workflow function
def my_workflow(inputs, params, **kwargs):
    """
    Simple hello world MNIST workflow
    :param inputs:
    :return:
    """
    print(f"{dp.name}.my_workflow: Arguments: inputs {inputs} params: {params}, **kwargs: {kwargs} ")

    task1 = Task(name="is_number")
    task1_inputs = [
        df.text("Is this image a number"),
        df.image(inputs.get("mnist_image_url")),
    ]
    task1_outputs = [df.exclusive_choice(choices=["yes", "no"])]
    task1.process(task_inputs=task1_inputs, task_outputs=task1_outputs)
    task1_response = task1.output.get("values", [])[0].get("schema_instance")

    if task1_response.get("selection", {}).get("value") == "yes":
        task2 = Task(name="choose_number")
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
dp.add_workflow(my_workflow, name="my_mnist_workflow_1", default=True)


# ------------------------------------------------------------------------------------
# Create a new Project project
project = Project(
    dataprogram=dp,
    name="FirstSuperAIWorfklow",
    params={
        "instructions": "Select the appropriate class for the MNIST image",
        "choices": ["0", "1", "2", "3"],
    },
)

# Send some data for labeling
mnist_urls = [
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/RandomBitmap.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/Brain.jpg",
]

inputs = [{"mnist_image_url": url} for url in mnist_urls]

labels = project.process(inputs=inputs, worker=Worker.me, open_browser=True)
