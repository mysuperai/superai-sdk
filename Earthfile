# Earthfile
VERSION 0.6

ARG PYTHON_MAJOR=3.9
ARG PYTHON_VERSION=$PYTHON_MAJOR.12
FROM python:$PYTHON_VERSION-alpine

RUN apk add --no-cache git gcc libffi-dev build-base bash
ARG SOURCE_DIR="superai"
ENV AWS_DEFAULT_REGION="us-east-1"
# Flag to enable codeartifact login
ARG INTERNAL=true
ARG SEMGREP_VERSION=0.86.5

pre-commit:
    RUN pip install --no-cache-dir pre-commit==2.17.0 black
    COPY . ./app
    WORKDIR /app
    RUN --mount=type=cache,target=/root/.cache/pre-commit pre-commit run --all-files

semgrep:
    RUN pip install --no-cache-dir semgrep==$SEMGREP_VERSION
    # Download rules separately for caching purposes in .ci/semgrep_rules
    RUN mkdir /rules
    COPY . ./app
    WORKDIR /app
    RUN semgrep --metrics=off --error --severity ERROR --disable-version-check --config .ci/semgrep_rules

linter:
    BUILD +semgrep
    BUILD +pre-commit

PIP_INSTALL:
    COMMAND
    ARG REQTARGET="."
    IF  [ "$INTERNAL" = "true" ]
        RUN --mount=type=secret,id=+secrets/aws,target=/root/.aws/credentials \
            --mount=type=cache,target=/root/.cache/pip \
            aws codeartifact login --tool pip --domain superai --repository pypi-superai-internal && \
            pip install "$REQTARGET"
    ELSE
        RUN --mount=type=cache,target=/root/.cache/pip \
            pip install "$REQTARGET"
    END


runtime-pip:
    # This step builds/installs the runtime Python dependencies used in the Lambda and also for integration tests
    FROM python:$PYTHON_VERSION-slim

    RUN apt-get update && \
        apt-get install --no-install-recommends -y \
        g++ \
        make \
        cmake \
        unzip \
        git \
        libcurl4-openssl-dev \
        && apt-get clean  \
        && rm -rf /var/lib/apt/lists/*

    # Install the runtime interface client
    RUN pip install --upgrade --no-cache-dir pip~=22.0.4 && pip install --no-cache-dir awscli==1.18.140
    
    ENV AWS_DEFAULT_REGION=us-east-1
    ARG PIP_TMP_DIR=/tmp/pip_dir

    WORKDIR /app

    COPY setup.py .
    DO +PIP_INSTALL --REQTARGET="."

build-requirements:
    FROM +runtime-pip
    DO +PIP_INSTALL --REQTARGET=".[build]"

test-requirements:
    FROM +runtime-pip
    DO +PIP_INSTALL --REQTARGET=".[test]"

ai-requirements:
    FROM +runtime-pip
    DO +PIP_INSTALL --REQTARGET=".[ai]"
    RUN RUN pip install --no-cache-dir pre-commit==2.17.0 semgrep==$SEMGREP_VERSION

    ARG IMAGE_TAG
    SAVE IMAGE $IMAGE_TAG

test:
    FROM +test-requirements
    COPY . .
    RUN make test
    # Output coverage and junit file
    SAVE ARTIFACT .test AS LOCAL .

dist:
    FROM +build-requirements
    COPY . .
    RUN make dist
    # copy dist folder in directory of Earthfile
    # Contains wheel file
    SAVE ARTIFACT  dist AS LOCAL .