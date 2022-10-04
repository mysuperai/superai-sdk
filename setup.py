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
    sys.path[0:0] = [NAME]
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
    "awesome-pattern-matching>=0.22.0",
    "boto3>=1.15",
    "click>=7.0",
    "diskcache>=5.4.0",
    "dynaconf>=3.1.2",
    "fastapi>=0.70.0",
    "futures-then>=0.1.1",
    "genson>=1.2.2",
    "jinja2>=2.11.2",
    "joblib>=0.17.0",
    "jsonmerge>=1.7.0",
    "jsonpickle>=1.4.1",
    "pandas>=1.2.5",
    "pip>=19.1",
    "pycognito>=2021.3.1",
    "pyyaml>=3.13",
    "requests>=2.22",
    "rich>=10.1",
    "scikit-learn>=0.23.2",
    "sentry-sdk>=0.19.4",
    "sgqlc[websocket]>=16",
    "six",
    "uvicorn>=0.15.0",
]

AI_REQUIRES = [
    "docker>=5.0.0",
    "polyaxon>=1.14.3",
    "sagemaker>=1.64.1",
    "protobuf>=3.20.1, <4.*",
    # 4.21.0 broke the sagemaker imports, see https://github.com/protocolbuffers/protobuf/issues/10051
]

BUILD_REQUIRES = [
    "black",
    "bump2version>=1.0.0",
    "setuptools>=50.3.2",
    "Sphinx>=3.2.1",
    "twine>=3.2.0",
    "wheel>=0.35.1",
]

DP_REQUIRES = [
    "awscli>=1.18.163",
    "superai-dataclient~=0.1.0",
    "superai-schema~=0.3.0",
    "pyngrok>=5.1.0",
]

TEST_REQUIRES = [
    "coverage>=5.3",
    "deepdiff>=4.0.7",
    "dictdiffer>=0.9.0",
    "pytest-cov>=2.10.1",
    "pytest-env>=0.6.2",
    "pytest-mock~=3.8.1",
    "pytest-vcr>=1.0.2",
    "pytest>=6.1.2",
    "seldon-core>=1.11.2",
    "tox>=2.9.1",
    "vcrpy>=4.1.1",
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
        "build": DP_REQUIRES + BUILD_REQUIRES,
        "dp": DP_REQUIRES,
        "ai": BUILD_REQUIRES + AI_REQUIRES + DP_REQUIRES,
        "test": TEST_REQUIRES + DP_REQUIRES + AI_REQUIRES,
        "complete": DP_REQUIRES + AI_REQUIRES + BUILD_REQUIRES + TEST_REQUIRES,
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
