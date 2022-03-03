# coding: utf-8


from setuptools import find_packages, setup  # type: ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "superai"

VERSION = "0.1.0.beta5.dev13"
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
    "colorama>=0.3.0",
    "dynaconf>=3.1.2",
    "docker>=4.0.0",
    "fastapi>=0.70.0",
    "futures-then>=0.1.1",
    "genson>=1.2.2",
    "jinja2>=2.11.2",
    "joblib>=0.17.0",
    "jsonmerge>=1.7.0",
    "jsonpickle>=1.4.1",
    "pip>=19.1",
    "rich>=10.1",
    "pyyaml>=3.13",
    "requests>=2.22",
    "sentry-sdk>=0.19.4",
    "scikit-learn>=0.23.2",
    "sgqlc>=14.1",
    "sentry-sdk>=0.19.4",
    "six",
    "uvicorn>=0.15.0",
    "pycognito>=2021.3.1",
    "pandas>=1.2.5",
    "polyaxon>=1.14.3",
    "sagemaker>=1.64.1",
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
    "superai-schema~=0.1.15",
]

TEST_REQUIRES = [
    "deepdiff>=4.0.7",
    "tox>=2.9.1",
    "coverage>=5.3",
    "pytest>=6.1.2",
    "pytest-cov>=2.10.1",
    "pytest-env>=0.6.2",
    "pytest-vcr>=1.0.2",
    "vcrpy>=4.1.1",
    "pytest-mock~=3.7.0",
    "seldon-core>=1.11.2",
]

setup(
    name=NAME,
    version=VERSION,
    description="super.AI API",
    author="super.AI",
    author_email="support@super.ai",
    url="https://github.com/mysuperai/superai-sdk",
    keywords=["super.AI API", "super.AI SDK"],
    install_requires=REQUIRES,
    extras_require={
        "build": DP_REQUIRES + BUILD_REQUIRES,
        "dp": DP_REQUIRES,
        "test": TEST_REQUIRES + DP_REQUIRES,
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
