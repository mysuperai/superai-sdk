# coding: utf-8


from setuptools import setup, find_packages

NAME = "superai_api_client"
VERSION = "0.0.1"
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
    author_email="",
    url="https://super.ai/",
    keywords=["super.AI API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    super.AI App Store API  
    """,
    entry_points={
        'console_scripts': [
            'superai=superai.cli:main',
        ],
    },
)
