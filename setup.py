# coding: utf-8


import sys

from setuptools import find_packages, setup  # type: ignore

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    # Remove dependency on external files in case we only want to install requirements
    print("README.md not found")
    long_description = ""

NAME = "superai"

# VERSION is defined in superai/version.py
try:
    sys.path[:0] = [NAME]
    from version import __version__  # type: ignore
except ImportError:
    # Fallback in case we only want to install requirements
    __version__ = "0.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "attrs>=22.1.0",
    "awesome-pattern-matching>=0.22.0",
    "boto3>=1.15",
    "click>=7.0",
    "diskcache>=5.4.0",
    "dynaconf>=3.1.12",
    "fastapi>=0.70.0, <0.104.0",  # 0.104 contains typing-extensions 4.8 which is not compat. with tensorflow 2.13.0
    "futures-then>=0.1.1",
    "genson>=1.2.2",
    "jinja2>=2.11.2",
    "joblib>=0.17.0",
    "jsonmerge>=1.7.0",
    "jsonpickle>=1.4.1",
    "pandas>=1.2.5",
    "pip>=19.1",
    "pycognito>=2022.12.0",
    "pydantic<2.0.0",
    "pyyaml>=3.13",
    "requests>=2.22",
    "rich>=10.1",
    "scikit-learn>=0.23.2",
    "sentry-sdk>=0.19.4",
    "sgqlc[websocket]>=16.2",
    "uvicorn>=0.15.0",
    "superai_logging>=0.1.0",
    "opentelemetry-distro[otlp]>=0.40b0",
    "opentelemetry-instrumentation-botocore>=0.40b0",
    "opentelemetry-instrumentation-requests>=0.40b0",
    "opentelemetry-instrumentation-fastapi>=0.40b0",
]


AI_REQUIRES = [
    "docker>=5.0.0",
    "polyaxon>=1.14.3",
    "protobuf>=3.20.1, <4",
    # 4.21.0 broke the sagemaker imports, see https://github.com/protocolbuffers/protobuf/issues/10051
    "netifaces>=0.11.0",
    "jsonlines>=4.0.0",
    "superai-builder>=0.9.1",
    "pydantic>=1.8.2,<2",
]
SUPERAI_COMMON_REQUIRES = [
    "superai-dataclient~=0.1.0",
    "superai-schema~=0.7",
    "pydantic>=1.8.2,<2",
]

BUILD_REQUIRES = [
    "Sphinx>=3.2.1",
    "black",
    "bump2version>=1.0.0",
    "setuptools>=50.3.2",
    "twine>=3.2.0",
    "wheel>=0.35.1",
]

DP_REQUIRES = [
    "pyngrok>=6.0.0",
    "superai-transport>=1.0.16",
]

TEST_REQUIRES = [
    "coverage>=5.3",
    "deepdiff>=4.0.7",
    "dictdiffer>=0.9.0",
    "moto>=3.1.12",
    "pytest-cov>=2.10.1",
    "pytest-env>=0.6.2",
    "pytest-mock~=3.10.0",
    "pytest-vcr>=1.0.2",
    "pytest-httpserver>=1.0.8",
    "pytest>=6.1.2",
    "superai-builder>=0.9.1",
    "tox>=2.9.1",
    "vcrpy>=4.1.1",
    "httpx~=0.25.1",
]

LLM_REQUIRES = [
    "tabulate~=0.9.0",
    "tiktoken~=0.4.0",
    "openai~=1.3.5",
    "shapely>=2.0.2",
]

LLM_REQUIRES_EXTRA = [
    "GitPython",
    "Pillow~=9.5.0",
    "PyPDF2",
    "aioconsole",
    "aiofile",
    "colorama",
    "duckduckgo-search",
    "evaluate",
    "faker",
    "flake8==6.1.0",
    "google-api-python-client",
    "google-search-results",
    "jiwer",
    "jupyter",
    "langchain~=0.0.130",
    "numpy~=1.26.2",
    "openpyxl",
    "orjson",
    "pdf2image~=1.16.3",
    "pinecone-client",
    "pydantic>=1.8.2,<2",
    "pytesseract",
    "python-dotenv",
    "reportlab",
    "selenium",
    "soundfile",
    "tabulate~=0.9.0",
    "textract-trp~=0.1.3",
    "tiktoken~=0.4.0",
    "tweepy",
    "watchdog==3.0.0",
    "webdriver-manager",
    "wikipedia",
    "wolframalpha",
]

setup(
    name=NAME,
    version=__version__,
    description="super.AI API",
    author="super.AI",
    author_email="support@super.ai",
    url="https://github.com/mysuperai/superai-sdk",
    keywords=["super.AI API", "super.AI SDK"],
    install_requires=REQUIRES,
    extras_require={
        "build": DP_REQUIRES + BUILD_REQUIRES + SUPERAI_COMMON_REQUIRES,
        "dp": DP_REQUIRES + SUPERAI_COMMON_REQUIRES,
        "ai": AI_REQUIRES + SUPERAI_COMMON_REQUIRES,
        "llm": LLM_REQUIRES + AI_REQUIRES + DP_REQUIRES + SUPERAI_COMMON_REQUIRES,
        "test": LLM_REQUIRES + TEST_REQUIRES + DP_REQUIRES + AI_REQUIRES + SUPERAI_COMMON_REQUIRES,
        "complete": BUILD_REQUIRES + DP_REQUIRES + AI_REQUIRES + LLM_REQUIRES + TEST_REQUIRES + SUPERAI_COMMON_REQUIRES,
    },
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "superai=superai.cli:main",
        ],
    },
)
