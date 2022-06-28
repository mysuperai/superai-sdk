# syntax=docker/dockerfile:1.2
ARG BASE_IMAGE
FROM $BASE_IMAGE

LABEL io.openshift.s2i.scripts-url="image:///s2i/bin"
LABEL com.amazonaws.sagemaker.capabilities.multi-models=true
LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true

# prevents public key not available error for Nvidia images (https://github.com/NVIDIA/nvidia-docker/issues/1632)
RUN rm -rf /etc/apt/sources.list.d/cuda.list && rm -rf /etc/apt/sources.list.d/nvidia-ml.list
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update --yes && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install --yes --no-install-recommends  \
      build-essential  \
      ca-certificates  \
      wget \
      default-jre-headless \
      libjpeg-dev zlib1g-dev \
      git && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG ANACONDA_VERSION=py39_4.10.3
ARG PYTHON_VERSION
RUN CONDA_VERSION=${ANACONDA_VERSION} \
    && UNAME_M="$(uname -m)" \
    && if [ "${UNAME_M}" = "x86_64" ]; then  \
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh";\
       elif [ "${UNAME_M}" = "aarch64" ]; then \
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-aarch64.sh";\
    fi && wget -O /tmp/anaconda.sh "${MINICONDA_URL}" &&  \
    chmod +x /tmp/anaconda.sh && \
    mkdir /root/.conda && \
    bash -c "/tmp/anaconda.sh -b -p /opt/conda" && \
    rm /tmp/anaconda.sh && \
    /opt/conda/bin/conda create -n env python=${PYTHON_VERSION} && \
    /opt/conda/bin/conda clean -ya && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate env" >> ~/.bashrc
SHELL ["/opt/conda/bin/conda", "run", "--no-capture-output", "-n", "env", "/bin/bash", "-c"]

RUN mkdir /home/model-server
WORKDIR /home/model-server

# Install requirements
RUN pip install --no-cache-dir -U pip awscli~=1.18.195
COPY requirements.txt /home/model-server/.requirements/base_requirements.txt
ARG AWS_DEFAULT_REGION=us-east-1
ARG PIP_REPO
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true \
    --mount=type=cache,target=/root/.cache/pip \
    aws codeartifact login --tool pip --domain superai --repository ${PIP_REPO} && \
    pip install --no-cache-dir -r /home/model-server/.requirements/base_requirements.txt
    
# Install superai version from local path/repository
COPY .dist/*.whl /home/model-server/.requirements/
ARG SUPERAI_WHL
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true \
    --mount=type=cache,target=/root/.cache/pip \
    aws codeartifact login --tool pip --domain superai --repository ${PIP_REPO} && \
    pip install --no-cache-dir '/home/model-server/.requirements/${SUPERAI_WHL}[ai]'

COPY s2i/bin /s2i/bin
COPY s2i/bin /opt/program

ENV PATH="/opt/program:${PATH}"

RUN chmod a+rwx /opt/program

RUN mkdir -p /.conda && \
    chmod a+rwx /.conda

EXPOSE 5000
WORKDIR /opt/program
