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

account:=$(shell (aws sts get-caller-identity --query Account --output text))
region:=$(shell (aws configure get region))
ecr_account:=${account}.dkr.ecr.${region}.amazonaws.com
fullname=${ecr_account}/${IMAGE_NAME}:${IMAGE_VERSION}

permissions:
	chmod +x s2i/bin/*

docker-login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ecr_account}

ifndef INTERNAL
  INTERNAL=true
endif

ifeq ($(INTERNAL), true)
    IMAGE_NAME=superai-model-s2i-python${IMAGE_PYTHON_VERSION}-${mode}-internal
else
    IMAGE_NAME=superai-model-s2i-python${IMAGE_PYTHON_VERSION}-${mode}
endif

push: docker-login
	docker tag "${IMAGE_NAME}:${IMAGE_VERSION}" "${ecr_account}/${IMAGE_NAME}:${IMAGE_VERSION}"
	aws ecr create-repository --repository-name ${IMAGE_NAME} || true
	docker push "${ecr_account}/${IMAGE_NAME}:${IMAGE_VERSION}"


push-lambda: docker-login
	docker tag "${IMAGE_NAME}-lambda:${IMAGE_VERSION}" "${ecr_account}/${IMAGE_NAME}-lambda:${IMAGE_VERSION}"
	aws ecr create-repository --repository-name ${IMAGE_NAME}-lambda || true
	docker push "${ecr_account}/${IMAGE_NAME}-lambda:${IMAGE_VERSION}"

push-seldon: docker-login
	docker tag "${IMAGE_NAME}-seldon:${IMAGE_VERSION}" "${ecr_account}/${IMAGE_NAME}-seldon:${IMAGE_VERSION}"
	aws ecr create-repository --repository-name ${IMAGE_NAME}-seldon || true
	docker push "${ecr_account}/${IMAGE_NAME}-seldon:${IMAGE_VERSION}"


.PHONY: all build tag push permissions build-all push-all

ifndef TARGET_PLATFORM
  TARGET_PLATFORM=linux/amd64
endif



ifeq ($(INTERNAL), true)
    PIP_REPO=pypi-superai-internal
else
    PIP_REPO=pypi-superai
endif

build: permissions
	DOCKER_BUILDKIT=1 docker build -f Dockerfile \
		--platform=${TARGET_PLATFORM} \
		--progress=plain \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg BASE_IMAGE=${BASE_IMAGE} \
		--build-arg PIP_REPO=${PIP_REPO} \
		-t ${IMAGE_NAME}:${IMAGE_VERSION} \
		--secret id=aws,src=${HOME}/.aws/credentials \
		.

build-lambda: permissions
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.lambda \
		--platform=${TARGET_PLATFORM} \
		--progress=plain \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg BASE_IMAGE=${BASE_IMAGE} \
		--build-arg PIP_REPO=${PIP_REPO} \
		-t ${IMAGE_NAME}-lambda:${IMAGE_VERSION} \
		--secret id=aws,src=${HOME}/.aws/credentials \
		.

build-seldon: permissions
	DOCKER_BUILDKIT=1 docker build -f Dockerfile.seldon \
		--platform=${TARGET_PLATFORM} \
		--progress=plain \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg BASE_IMAGE=${BASE_IMAGE} \
		--build-arg PIP_REPO=${PIP_REPO} \
		-t ${IMAGE_NAME}-seldon:${IMAGE_VERSION} \
		--secret id=aws,src=${HOME}/.aws/credentials \
		.

build-all: build build-lambda build-seldon

push-all: push push-lambda push-seldon

all: build-all push-all