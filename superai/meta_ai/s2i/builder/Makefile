IMAGE_VERSION=1
SHELL:=/bin/bash

ifndef PYTHON_VERSION
	PYTHON_VERSION=3.7.11
endif
IMAGE_PYTHON_VERSION=$(echo -n $(PYTHON_VERSION) | sed 's/\.//g')

ifndef mode
	mode=cpu
endif

ifeq ($(mode), cpu)
	BASE_IMAGE=python:${PYTHON_VERSION}-slim-buster
else
	BASE_IMAGE=nvidia/cuda:10.2-cudnn8-runtime-ubuntu18.04
endif

IMAGE_NAME=superai-model-s2i-python${IMAGE_PYTHON_VERSION}-${mode}

account=$(eval (aws sts get-caller-identity --query Account | sed -e 's/^"//' -e 's/"$//'))
region=$(eval aws configure get region)
ecr_account=${account}.dkr.ecr.${region}.amazonaws.com

fullname=${ecr_account}/${IMAGE_NAME}:${IMAGE_VERSION}

permissions:
	chmod +x s2i/bin/*

push:
	python -c "import superai.meta_ai.dockerizer as dock;dock.push_image('${IMAGE_NAME}','${IMAGE_VERSION}')"

.PHONY: all build tag push permissions

TARGET_PLATFORM=linux/amd64
build: permissions
	DOCKER_BUILDKIT=1 docker build -f Dockerfile \
		--platform=${TARGET_PLATFORM} \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg BASE_IMAGE=${BASE_IMAGE} \
		-t ${IMAGE_NAME}:${IMAGE_VERSION} \
		--secret id=aws,src=${HOME}/.aws/credentials \
		.

all: build push