from superai import DataProgram, Task

dp_definition = {
    "input_schema": {"mnist_image_url": {"type": "image"}},
    "output_schema": {"mnist_class": {"type": "single-choice", "choices": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}},
}
dp_template = DataProgram(dp_definition=dp_definition)

def my_workflow(inputs):
    """
    Simple hello world MNIST workflow
    :param inputs:
    :return:
    """
    task_definition = {
    "input_schema": {"my_task_input": {"type": "image"}},
    "output_schema": {"my_task_mnist_class": {"type": "single-choice", "choices": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}},
}
    task1 = Task(task_definition)
    task_input = [{"my_task_input": inputs["mnist_image_url"]}]
    task_output = task1(inputs=task_input)

    return {
        "mnist_class": task_output['my_task_mnist_class']
    }

dp_template.add_workflow(my_workflow, name="my_mnist_workflow_1")

dp_instance = dp_template(instructions="Select the appropriate class for the MNIST image", quality={"f1": .9})

mnist_urls = ["https://raw.githubusercontent.com/datapythonista/mnist/master/img/img_5.png"]
inputs = [{"image": url} for url in mnist_urls * 3]
labels = dp_instance.label(inputs=inputs)