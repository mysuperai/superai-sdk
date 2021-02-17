# coding: utf-8


from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "superai"
VERSION = "0.0.9"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "names",  # TODO: Remove in next versions
    "boto3>=1.16",
    "click>=7.0",
    "colorama>=0.4.3",
    "dynaconf>=3.1.2",
    "futures-then>=0.1.1",
    "genson>=1.2.2",
    "jinja2>=2.11.2",
    "joblib>=0.17.0",
    "jsonmerge~=1.7.0",
    "jsonpickle>=1.4.1",
    "pyyaml>=5.3.1",
    "requests>=2.22",
    "sentry-sdk>=0.19.4",
    "scikit-learn>=0.23.2",
    "warrant>=0.6",
]

BUILD_REQUIRES = [
    "awscli>=1.18.163",
    "bump2version~=1.0.1",
    "setuptools>=50.3.2",
    "Sphinx>=3.2.1",
    "wheel>=0.35.1",
]
DEV_REQUIRES = [
]
TEST_REQUIRES = [
    "deepdiff>=4.0.7",
    "tox>=2.9.1",
    "coverage>=5.3",
    "pytest>=6.1.2",
    "pytest-cov>=2.10.1",
    "pytest-env>=0.6.2",
]

setup(
    name=NAME,
    version=VERSION,
    description="super.AI API",
    author="super.AI",
    author_email="support@super.ai",
    url="https://github.com/mysuperai/superai-api-client",
    keywords=["super.AI API"],
    install_requires=REQUIRES,
    extras_require={
        "build": BUILD_REQUIRES,
        "dev": DEV_REQUIRES,
        "test": TEST_REQUIRES,
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
