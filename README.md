# super.AI API Client

Use this library to interact with super.AI API

## Preliminary - please read.

- The CLI included in this package uses Python 3. On systems that have both Python 2 and Python 3 installed, you may need to replace the calls to `python` and `pip` below with `python3` and `pip3`, respectively.
- Dependencies in this package rely on the clang build tools on Mac OS. If you have recently updated or installed XCode, you may be required to run `sudo xcodebuild -license` before following the instructions below.

## Install
```
pip install superai
```

## Build

```
python setup.py bdist_wheel
```

## Install build

```
pip install --upgrade dist/superai-{version}-py3-none-any.whl
```

## Usage

### CLI

Before you can interact with the API, you will need to register at [super.ai](https://super.ai) and log in to the CLI tool. For more information, please follow the instructions provided by:

```
superai --help
```
Note: If you signed-up using Google you need to set api-key manually using:
```
superai config --api-key <API-KEY>
```
### Python example

```python
import superai as ai

client = ai.Client("API-KEY")

client.create_jobs(app_id="APP_ID",
		callback_url='http://www.example.com/callback',
		inputs=[{"data_url":"http://i.imgur.com/XOJbalC.jpg"}]
)

```
