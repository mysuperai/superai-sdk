# Super.AI API client

The super.AI Python library provides access to the super.AI API via Python and our command line interface (CLI). Full details on our API are listed in our [API reference](https://super.ai/reference). For data programmers, we also offer the Data Program Builder.

In this README, you will find the following sections:

- [Installation](#installation)
- [CLI usage](#cli-usage)
- [CLI commands](#cli-commands)
- [Python usage](#python-usage)
- [Data Program Builder](#data-program-builder)

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

# Data Program Builder

The super.AI Data Program Builder is a Python SDK that lets you create your own Data Programs. Take a look at our [full documentation](https://superai.readme.io/v1.5/docs/data-program-builder-overview).

## Requirements
  - A super.AI data programmer account. Please [contact us](mailto:dataprogrammer@super.ai) to create an account.
  - Python >= `3.6` and < `3.9`. Python > `3.9` is not yet supported.
  - Java JRE installed. To verify if you have Java installed, run `java --version`. If you don't have it installed, follow the relevant installation instructions:
     - [Ubuntu 20-4](https://linoxide.com/ubuntu-how-to/install-java-ubuntu-20-04/),
       [Ubuntu 18-04](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-18-04),
       [Ubuntu 16-04](https://www.atlantic.net/hipaa-compliant-hosting/how-to-install-java-jre-jdk-ubuntu-16-04/),
       [Mac OSX](https://www.java.com/en/download/apple.jsp)
  - **Note** If you are a Windows user, you will need to [install Windows Subsystem for Linux(WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10#manual-installation-steps)
  - For AI components, Source-to-Image package is required. Check the installation [instructions](superai/meta_ai/s2i/ReadMe.md)

## Installation  
  1. Create and activate a virtual environment (we recommend using [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) or Anaconda)
     - If you're using Anaconda, run `conda install -c conda-forge pycryptodome` before moving on
  2. Run `pip install --upgrade pip==20.1.1`
  3. Run `pip install "awscli"`
  4. Run `pip install --upgrade "superai>=0.1.0.alpha1"`
  5. Run `superai env set -e sandbox` 
  6. Run `superai login -u <user_email>`
  7. Verify that the pip was configured correctly by running `pip config get global.index-url`
     If the response is empty then run `superai login --show-pip -u <user_email>` and copy/paste the 
     `pip config set...` command as indicated
  8. Install superai in dataprogramming mode `pip install --upgrade "superai[dp]>=0.1.0.beta2"`
  9. For AI components install `pip install --upgrade superai[ai]>=0.1.0.beta2`
  10. Install everything by `pip install --upgrade superai[complete]>=0.1.0.beta2`

## Usage

Creating a basic super AI is a easy as:
  1. Create a data program name
  2. Define the input, output and paremeter schemas
  3. Instantiate a Project class
  4. *Optional*: Label some data yourself

```python
import uuid

import superai_schema.universal_schema.data_types as dt

from superai.data_program import Project, WorkerType

# 1) First we need to create the interface of our data program. We do this using schemas that define
#    the input, output and parameter types. In this data program we are specifying that its input has
#    to be a dictionary that with `key`:mnist_image_url and its value is an image url e.g. 
#    {"mnist_image_url": "https://superai-public.s3.amazonaws.com/example_imgs/digits/0zero.png"}.

#    An an example of the parameters that validate against the parameters schema is:
#    params={
#        "instructions": "My simple instruction",
#        "choices": ["0","1"]
#    }
#    
#    Finally as output this data program is going to generate an object of type exclusive choice that 
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

# 2) Create a data program name (it has to be unique across super.ai)
# Using uuid.getnode() to get a unique name for your first 
DP_NAME = "MyFirstDataProgram" + str(uuid.getnode())

# 3) Create a Project project by defining the data pogram parameter values
superAI = Project(
    dp_name=DP_NAME,
    dp_definition=dp_definition,
    params={
        "instructions": "My simple instruction",
        "choices": [f"{i}" for i in range(10)],
    },
)

# 4) Now we are ready to test our Project, so let's submit some jobs for processing. One you run the 
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

labels = superAI.process(inputs=inputs, worker=WorkerType.me, open_browser=True)
```

You can find more examples in docs/examples

### Pycharm specific requirement

For better logging when using Pycharm, please change your run configuration to have the following switch enabled. It's easier to do it once for the Python runner template for the project. 

> - [x] Emulate terminal in output console