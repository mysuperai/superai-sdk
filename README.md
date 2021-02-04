# Super.AI API client

The super.AI Python library provides access to the super.AI API via Python and our command line interface (CLI). Full details on our API are listed in our [API reference](https://super.ai/reference).

In this README, you will find the following sections:

- [Installation](#installation)
- [CLI usage](#cli-usage)
- [CLI commands](#cli-commands)
- [Python usage](#python-usage)

## Installation

In your terminal, run:

```
pip install superai
```

**Note**: If you want to create a data program yourself follow these installation [instructions](#Creating-a-data-program)

### Requirements

- Python 3.6 or later. On systems that have both Python 2 and Python 3 installed, you may need to replace the call to `pip` with `pip3`.
- Dependencies in this package rely on the Clang build tools on MacOS. If you have recently updated or installed XCode, you may have to run `sudo xcodebuild -license` prior to installation.
- A [super.AI](https://super.ai/) account

## CLI usage

Installing the API client provides access to the `superai` command from within your terminal.

```bash
superai [command]

# Run `--help` for detailed information about CLI commands, including required and optional flags
superai [command] --help
```

### Logging in

In order to use the CLI, you need to pass us your API key. Use the following command to do this:

```bash
superai login --username {username}
```

Replace `{username}` with your super.AI account username.

When prompted, enter your password and press enter. You should see a confirmation like this:

```bash
Api key {api-key} was set
```

If you created your account through Google Sign-In you will need to manually set your API key:

1. Find your API key in the [super.AI dashboard](https://super.ai/dashboard/) by hovering over the profile icon in the lower left of the screen, then heading to **API keys**. You can copy the key by clicking on the copy button.
2. Provide your API key to the client using the following command (replacing `{api-key}` with your actual API key): `superai config --api-key {api-key}`

### Logging out

You can log out and thereby remove your API key by running the following command:

```bash
superai logout
```

## CLI commands

- `login`
- `create_jobs`
- `list_jobs`
- `fetch_job`
- `get_job_responses`
- `cancel_job`
- `download_jobs`
- `fetch_batch_job`
- `fetch_batches_job`
- `create_ground_truth`
- `list_ground_truth_data`
- `get_ground_truth_data`
- `update_ground_truth`
- `delete_ground_truth_data`

If you're new to using a CLI, our [Getting started with the CLI page](https://super.ai/docs/getting-started-with-the-cli) can show you the ropes.

## Python usage

This client allows you to run Python scripts on your machine to automate your work processes. For example, you can use a script like this to submit data points for processing to a project that takes image inputs, replacing any `{variables}` where necessary:

```python
import superai as ai

client = ai.Client("{api-key}")

client.create_jobs(
    app_id="{project-id}",
    inputs=[{"image_url":"https://cdn.super.ai/cool-bulldog.jpg"},{"image_url":"https://cdn.super.ai/hot-dog-01.jpeg"}]
)
```

# Creating a data program

## Requirements
  - Have a superai `dataprogrammer` account. Please [contact us](mailto:dataprogrammer@super.ai) to create an account.

## Installation  
  1. Create a virtualenv (we recommend to use [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) or conda)
  2. Run `aws codeartifact login --tool pip --domain superai --repository pypi-us-east-1`
  3. Run `pip install awscli~=1.18.163`

------
# REMOVE SECTION BEFORE RELEASE
  1. Make sure that you can open the [codeartifact](https://console.aws.amazon.com/codesuite/codeartifact/d/185169359328/superai/r/pypi-us-east-1/p/pypi/superai/versions?package-versions-meta=eyJmIjp7fSwicyI6e30sIm4iOjIwLCJpIjowfQ&region=us-east-1#) UI in aws. If not contact Enrique
  2. Configure your awscli using your internal superai credentials
  3. Run `aws codeartifact login --tool pip --domain superai --repository pypi-us-east-1`
  4. Run `pip install "superai~=0.1.0.a1.dev12"`
  5. Skip the next step and continue directly with `superai login..` **AND** in the last step execute `pip install superai[dp]~=0.1.0.a1.dev12` 

------
  3. Run `pip install "superai>=0.1.0.a1"`  
  4. Run `superai login -u <user_email>`
  5. Verify that pip was configured correctly by opening your pip configuration `pip config --user edit --editor vim`. If the configuration was successful you should see a value set in the index_url
  6. Install superai in dataprogramming mode `pip install superai[dp]>=0.1.0.a1`. 
      - Note if you are using zsh you need to use `pip install "superai[dp]>=0.1.0.alpha1"` because zsh uses square brackets for globbing / pattern matching. 

## Usage

Creating a basic super AI is a easy as:
  1. Create a template name
  2. Define the input, output and paremeter schemas
  3. Instantiate a SuperAI class
  4. *Optional*: Label some data yourself

```python
import uuid

import ai_marketplace_hub.universal_schema.data_types as dt

from superai.data_program import SuperAI, Worker


# 1) First we need to create the interface of our template. We do this using schemas that define
#    the input, output and parameter types. In this template we are specifying that its input has
#    to be a dictionary that with `key`:mnist_image_url and its value is an image url e.g. 
#    {"mnist_image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}.

#    An an example of the parameters that validate against the parameters schema is:
#    params={
#        "instructions": "My simple instruction",
#        "choices": ["0","1"]
#    }
#    
#    Finally as output this template is going to generate an object of type exclusive choice that 
#    looks like: {
#       "mnist_class": {
#         "choices": [
#           {
#             "tag": "0",
#             "value": "0"
#           },
#           {
#             "tag": "1",
#             "value": "1"
#           }
#         ],
#         "selection": {
#           "tag": "0",
#           "value": "0"
#         }
#       }
#     }
dp_definition = {
    "input_schema": dt.bundle(mnist_image_url=dt.IMAGE),
    "parameter_schema": dt.bundle(instructions=dt.TEXT, choices=dt.array_to_schema(dt.TEXT, 0)),
    "output_schema": dt.bundle(mnist_class=dt.EXCLUSIVE_CHOICE),
}

# 2) Create a template name (it has to be unique across super.ai)
# Using uuid.getnode() to get a unique name for your first template
TEMPLATE_NAME = "MyFirstDataProgramTemplate" + str(uuid.getnode())

# 3) Create a SuperAI project by defining the template parameter values
superAI = SuperAI(
    template_name=TEMPLATE_NAME,
    dp_definition=dp_definition,
    params={
        "instructions": "My simple instruction",
        "choices": [f"{i}" for i in range(10)],
    },
)

# 4) Now we are ready to test our SuperAI, so let's submit some jobs for processing. One you run the 
#    following lines a new browser window will open (because we are passing `open_browser=True` as an 
#    argument to the process function, and a couple of seconds afterwards you should be able to annotate
#    the images yourself
mnist_urls = [
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/1one.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/2two.png",
    "https://superai-public.s3.amazonaws.com/example_imgs/digits/3three.png",
]
inputs = [{"mnist_image_url": url} for url in mnist_urls]

labels = superAI.process(inputs=inputs, worker=Worker.me, open_browser=True)
```

You can find more examples in docs/examples
