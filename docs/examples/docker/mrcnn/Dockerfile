ARG UBUNTU_VERSION=16.04

ARG CUDA=10.0
FROM nvidia/cuda:${CUDA}-base-ubuntu${UBUNTU_VERSION} as base
ARG CUDA=10.0
ARG CUDADASH=10-0
ARG CUDNN=7.4.1.5-1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential cuda-command-line-tools-${CUDADASH} cuda-cublas-${CUDADASH} cuda-cufft-${CUDADASH} cuda-curand-${CUDADASH} cuda-cusolver-${CUDADASH} cuda-cusparse-${CUDADASH} curl libcudnn7=${CUDNN}+cuda${CUDA} libfreetype6-dev libhdf5-serial-dev libzmq3-dev pkg-config software-properties-common unzip wget && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
        apt-get install nvinfer-runtime-trt-repo-ubuntu1604-5.0.2-ga-cuda${CUDA} \
        && apt-get update \
        && apt-get install -y --no-install-recommends libnvinfer5=5.0.2-1+cuda${CUDA} \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH /usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

ARG PYTHON=python3.7

ENV LANG C.UTF-8

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install --no-install-recommends -y ${PYTHON}

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN ${PYTHON} get-pip.py
RUN ln -sf /usr/bin/${PYTHON} /usr/local/bin/python3
RUN ln -sf /usr/local/bin/pip /usr/local/bin/pip3

RUN pip3 --no-cache-dir install --upgrade \
    pip \
    setuptools

RUN ln -s $(which ${PYTHON}) /usr/local/bin/python

LABEL maintainer="ankit <ankit@super.ai>"

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         nginx \
         gcc \
         ca-certificates \
         make \
         g++ \
         git \
         libsndfile1 wget curl gnupg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# PYTHONUNBUFFERED keeps Python from buffering the standard
# output stream, which means that logs can be delivered to the user quickly.
# PYTHONDONTWRITEBYTECODE keeps Python from writing the .pyc files which are unnecessary in this case.

LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true

ARG PYTHON=python3
ARG PIP=pip3
ARG TFS_SHORT_VERSION=2.1
ARG TFS_URL=https://tensorflow-aws.s3-us-west-2.amazonaws.com/2.1/Serving/GPU/tensorflow_model_server

ENV NCCL_VERSION=2.4.7-1+cuda10.1
ENV CUDNN_VERSION=7.6.2.24-1+cuda10.1
ENV TF_TENSORRT_VERSION=6.0.1

# See http://bugs.python.org/issue19846
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
# Python won’t try to write .pyc or .pyo files on the import of source modules
ENV PYTHONUNBUFFERED=1
ENV SAGEMAKER_TFS_VERSION="${TFS_SHORT_VERSION}"
ENV PATH="$PATH:/sagemaker"
ENV MODEL_BASE_PATH=/models
# The only required piece is the model name in order to differentiate endpoints
ENV MODEL_NAME=model
# Fix for the interactive mode during an install in step 21
ENV DEBIAN_FRONTEND=noninteractive

RUN pip install --upgrade --no-cache-dir pip setuptools wheel

RUN git clone https://github.com/matterport/Mask_RCNN /root/Mask_RCNN
WORKDIR /root/Mask_RCNN
RUN python setup.py install

ENV AWS_SHARED_CREDENTIALS_FILE="./sagify_base/.aws/credentials"
ENV TF_FORCE_GPU_ALLOW_GROWTH="true"
