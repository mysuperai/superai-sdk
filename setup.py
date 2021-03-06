# coding: utf-8


from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "superai"
VERSION = "0.1.0.alpha2"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "boto3>=1.15",
    "click>=7.0",
    "colorama>=0.3.0",
    "dynaconf>=3.1.2",
    "futures-then>=0.1.1",
    "genson>=1.2.2",
    "jinja2>=2.11.2",
    "joblib>=0.17.0",
    "jsonmerge>=1.7.0",
    "jsonpickle>=1.4.1",
    "pip>=19.1",
    "pyyaml>=3.13",
    "requests>=2.22",
    "scikit-learn>=0.23.2",
    "sgqlc>=12.1",
    "sentry-sdk>=0.19.4",
    "six",
    "warrant>=0.6",
]

BUILD_REQUIRES = [
    "black",
    "bump2version>=1.0.0",
    "setuptools>=50.3.2",
    "Sphinx>=3.2.1",
    "twine>=3.2.0",
    "wheel>=0.35.1",
    "sagemaker>=1.64.1",
]

DP_REQUIRES = [
    "awscli>=1.18.163",
    "superai-dataclient~=0.1.0",
    "superai-schema~=0.0.1",
]

TEST_REQUIRES = [
    "deepdiff>=4.0.7",
    "tox>=2.9.1",
    "coverage>=5.3",
    "pytest>=6.1.2",
    "pytest-cov>=2.10.1",
    "pytest-env>=0.6.2",
    "vcrpy>=4.1.1",
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
