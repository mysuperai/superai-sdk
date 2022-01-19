IMAGE_VERSION=1
SHELL:=/bin/bash

ifndef PYTHON_VERSION
	PYTHON_VERSION=3.7.11
endif
IMAGE_PYTHON_VERSION=$(shell echo -n $(PYTHON_VERSION) | sed 's/\.//g')

ifndef mode
	mode=cpu
endif

ifeq ($(mode), cpu)
	BASE_IMAGE=python:${PYTHON_VERSION}-slim-buster
else ifeq ($(mode), eia)
	BASE_IMAGE=763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-inference-eia:2.3.0-cpu-py37-ubuntu18.04
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

docker-login:
	$$(aws ecr get-login --no-include-email --region us-east-1)

push: docker-login
	docker tag "superai-model-s2i-python3711-${mode}:1" "185169359328.dkr.ecr.us-east-1.amazonaws.com/superai-model-s2i-python3711-${mode}:1"
	docker push "185169359328.dkr.ecr.us-east-1.amazonaws.com/superai-model-s2i-python3711-${mode}:1"


push-lambda: docker-login
	docker tag "superai-model-s2i-python3711-${mode}-lambda:1" "185169359328.dkr.ecr.us-east-1.amazonaws.com/superai-model-s2i-python3711-${mode}-lambda:1"
	docker push "185169359328.dkr.ecr.us-east-1.amazonaws.com/superai-model-s2i-python3711-${mode}-lambda:1"

push-seldon: docker-login
	docker tag "superai-model-s2i-python3711-${mode}-seldon:1" "185169359328.dkr.ecr.us-east-1.amazonaws.com/superai-model-s2i-python3711-${mode}-seldon:1"
	docker push "185169359328.dkr.ecr.us-east-1.amazonaws.com/superai-model-s2i-python3711-${mode}-seldon:1"


.PHONY: all build tag push permissions

ifndef TARGET_PLATFORM
TARGET_PLATFORM=linux/amd64
endif

build: permissions
	DOCKER_BUILDKIT=1 docker build -f Dockerfile \
		--platform=${TARGET_PLATFORM} \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg BASE_IMAGE=${BASE_IMAGE} \
		-t ${IMAGE_NAME}:${IMAGE_VERSION} \
		--secret id=aws,src=${HOME}/.aws/credentials \
		.

build-lambda: permissions
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.lambda \
		--platform=${TARGET_PLATFORM} \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg BASE_IMAGE=${BASE_IMAGE} \
		-t ${IMAGE_NAME}-lambda:${IMAGE_VERSION} \
		--secret id=aws,src=${HOME}/.aws/credentials \
		.

build-seldon: permissions
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.seldon \
		--platform=${TARGET_PLATFORM} \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg BASE_IMAGE=${BASE_IMAGE} \
		-t ${IMAGE_NAME}-seldon:${IMAGE_VERSION} \
		--secret id=aws,src=${HOME}/.aws/credentials \
		.

all: build build-lambda build-seldon push push-lambda push-seldon