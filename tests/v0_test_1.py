from superai import DataProgram

dp_definition = {
    "input_schema": {"image": {"type": "image"}},
    "output_schema": {"choice": {"type": "single-choice", "choices": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}},
}
dp_template = DataProgram(dp_definition=dp_definition)

mnist_urls = ["https://raw.githubusercontent.com/datapythonista/mnist/master/img/img_5.png"]
inputs = [{"image": url} for url in mnist_urls * 3]
labels = dp_template.label(inputs=inputs)
