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

### Requirements

- Python 3.6 or later. On systems that have both Python 2 and Python 3 installed, you may need to replace the call to `pip` with `pip3`.
- Dependencies in this package rely on the Clang build tools on MacOS. If you have recently updated or installed XCode, you may have to run `sudo xcodebuild -license` prior to installation.
- A super.AI account.

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

1. Find your API key in the [super.AI dashboard](https://super.ai/dashboard/) by hovering over the profile icon in the lower left of the screen, then heading to **API keys**. You can copy the key by clicking on the copy (insert icon here) button.
2. Provide your API key to the client using the following command (replacing `{api-key}` with your actual API key): `sh superai config --api-key {api-key}`

### Logging out

You can log out and thereby remove your API key by running the following command:

```bash
superai logout
```

## CLI commands

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

```bash
import superai as aiclient = ai.Client("{api-key}")client.create_jobs(    app_id="{project-id}",    inputs=[{"image_url":"https://cdn.super.ai/cool-bulldog.jpg"},{"image_url":"https://cdn.super.ai/hot-dog-01.jpeg"}])
```