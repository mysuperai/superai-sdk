import uuid

import ai_marketplace_hub.universal_schema.data_types as dt

from superai.data_program import SuperAI, Worker

# Defining the template interface
dp_definition = {
    "input_schema": dt.bundle(mnist_image_url=dt.IMAGE),
    "parameter_schema": dt.bundle(instructions=dt.TEXT, choices=dt.array_to_schema(dt.TEXT, min_items=0)),
    "output_schema": dt.bundle(mnist_class=dt.EXCLUSIVE_CHOICE),
}

# Using uuid.getnode() to get a unique name for your first template
TEMPLATE_NAME = "MyFirstDataProgramTemplate" + str(uuid.getnode())

# Creating a SuperAI.
superAI = SuperAI(
    template_name=TEMPLATE_NAME,
    dp_definition=dp_definition,
    params={
        "instructions": "My simple instructions",
        "choices": [f"{i}" for i in range(10)],
    },
)


mnist_urls = [
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/1one.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/2two.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/3three.png",
]
inputs = [{"mnist_image_url": url} for url in mnist_urls]

labels = superAI.process(inputs=inputs, worker=Worker.me, open_browser=True)
