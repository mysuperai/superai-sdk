# coding: utf-8


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "superai"
VERSION = "0.0.5"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "boto3>=1.9",
    "requests>=2.22",
    "Click>=7.0",
    "warrant>=0.6",
]

setup(
    name=NAME,
    version=VERSION,
    description="super.AI API",
    author='super.AI',
    author_email="support@super.ai",
    url="https://github.com/mysuperai/superai-api-client",
    keywords=["super.AI API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'superai=superai.cli:main',
        ],
    },
)
