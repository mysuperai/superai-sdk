# Earthfile
VERSION --use-no-manifest-list 0.6

ARG PYTHON_MAJOR=3.9
ARG PYTHON_VERSION=$PYTHON_MAJOR.12
FROM python:$PYTHON_VERSION-alpine

RUN apk add --no-cache git gcc libffi-dev build-base bash
ARG SOURCE_DIR="superai"
ENV AWS_DEFAULT_REGION="us-east-1"
# Flag to enable codeartifact login
ARG INTERNAL=true

pre-commit:
    RUN pip install --no-cache-dir pre-commit==2.17.0 black
    COPY . ./app
    WORKDIR /app
    RUN --mount=type=cache,target=/root/.cache/pre-commit pre-commit run --all-files

linter:
    BUILD +pre-commit

PIP_INSTALL:
    COMMAND
    ARG REQTARGET="."
    ARG AWS_ACCESS_KEY_ID=""
    ARG AWS_SECRET_ACCESS_KEY=""
    ARG AWS_SESSION_TOKEN=""
    IF  [ "$INTERNAL" = "true" ]
        RUN --mount=type=secret,id=+secrets/aws,target=/root/.aws/credentials \
            --mount=type=cache,target=/root/.cache/pip \
            aws codeartifact login --tool pip --domain superai --domain-owner 185169359328 --repository pypi-superai-internal --region us-east-1 && \
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
        pkg-config \
        libcairo2-dev \
        libjpeg-dev \
        libgif-dev \
        && apt-get clean  \
        && rm -rf /var/lib/apt/lists/*

    # Install the runtime interface client
    RUN pip install --upgrade --no-cache-dir pip~=23.1.2 && pip install --no-cache-dir awscli==1.27.135 

    # This a temporal workaround for missing assets in AWS CodeArtifacts
    RUN pip install lxml==4.9.2
    
    ENV AWS_DEFAULT_REGION=us-east-1
    ARG PIP_TMP_DIR=/tmp/pip_dir

    WORKDIR /app

    COPY setup.py .

    # AWS Credentials defaulting to empty string if aws secret is provided
    # Placing the following args in the PIP_INSTALL command does not work as the ARG command should be within a stage, not a command
    ARG AWS_ACCESS_KEY_ID=""
    ARG AWS_SECRET_ACCESS_KEY=""
    ARG AWS_SESSION_TOKEN=""

    DO +PIP_INSTALL --REQTARGET="." --AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

base-superai-install:
    # Contains the base install for the superai package
    FROM +runtime-pip
    COPY . .
    # Install the superai package with all files copied
    DO +PIP_INSTALL --REQTARGET="." --AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

test-superai-cli:
    # Test the superai CLI (run in CI/CD)
    # Mainly fails, if there are imports for the superai package that are not in the setup.py base requirements
    FROM +base-superai-install
    RUN superai info

build-requirements:
    FROM +runtime-pip

    ARG AWS_ACCESS_KEY_ID=""
    ARG AWS_SECRET_ACCESS_KEY=""
    ARG AWS_SESSION_TOKEN=""

    DO +PIP_INSTALL --REQTARGET=".[build]" --AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

test-requirements:
    FROM +runtime-pip

    ARG AWS_ACCESS_KEY_ID=""
    ARG AWS_SECRET_ACCESS_KEY=""
    ARG AWS_SESSION_TOKEN=""

    DO +PIP_INSTALL --REQTARGET=".[test]" --AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN

ai-requirements:
    FROM --platform=linux/amd64 python:$PYTHON_VERSION-slim

    # Install the runtime interface client
    RUN pip install --upgrade --no-cache-dir pip~=23.1.2 && pip install --no-cache-dir awscli==1.27.135
    ARG DOCKER_VERSION="5:20.10.24~3-0~debian-bullseye"
    RUN apt-get update && apt-get install --no-install-recommends -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gcc \
        git \
        gnupg \
        g++ \
        make \
        net-tools \
        cmake \
        unzip \
        git \
        libcurl4-openssl-dev \
        libgeos-c1v5 \
        linux-libc-dev \
        libc6-dev \
        lsb-release \
        && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg  \
        && echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null  \
        && curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | tee /usr/share/keyrings/helm.gpg > /dev/null \
        && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list \
        && apt-get update  \
        && apt-get install --no-install-recommends -y docker-ce=${DOCKER_VERSION} docker-ce-cli=${DOCKER_VERSION} containerd.io docker-buildx-plugin docker-compose-plugin helm \
        && apt-get clean  \
        && rm -rf /var/lib/apt/lists/*

    # Creating user
    ENV USER_HOME /var/user_home
    ARG user=jenkins
    ARG group=jenkins
    ARG uid=1000
    ARG gid=1000
    RUN groupadd -g ${gid} ${group} \
        && useradd -d "${USER_HOME}" -u ${uid} -g ${gid} -m -s /bin/bash ${user}  \
        && usermod -aG docker ${user}
    RUN mkdir /rules

    WORKDIR ${USER_HOME}
    ARG SEMGREP_VERSION=0.86.5
    RUN --mount=type=cache,target=/root/.cache/pip \
        pip install pre-commit==2.17.0 semgrep==$SEMGREP_VERSION python-semantic-release==7.34.3

    # This a temporal workaround for missing assets in AWS CodeArtifacts
    RUN pip install lxml==4.9.2

    COPY setup.py .

    ARG AWS_ACCESS_KEY_ID=""
    ARG AWS_SECRET_ACCESS_KEY=""
    ARG AWS_SESSION_TOKEN=""

    RUN --mount=type=secret,id=+secrets/aws,target=/root/.aws/credentials \
            --mount=type=cache,target=/root/.cache/pip \
            aws codeartifact login --tool pip --domain superai --domain-owner 185169359328 --repository pypi-superai-internal --region us-east-1 && \
            pip install ".[test]"

    COPY . .

    RUN --mount=type=secret,id=+secrets/aws,target=/root/.aws/credentials \
            --mount=type=cache,target=/root/.cache/pip \
            aws codeartifact login --tool pip --domain superai --domain-owner 185169359328 --repository pypi-superai-internal --region us-east-1 && \
            pip install ".[ai]"

    ENV PATH "$PATH:${USER_HOME}/.local/bin"

    COPY scripts/integrationTest.sh /var/user_home/integrationTest.sh
    RUN chmod +x /var/user_home/integrationTest.sh

    USER root
    RUN chown -R ${uid}:${gid} ${USER_HOME}
    USER ${uid}

    ARG IMAGE_TAG="185169359328.dkr.ecr.us-east-1.amazonaws.com/superai-sdk-internal"
    SAVE IMAGE --no-manifest-list --push ${IMAGE_TAG}

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
    SAVE ARTIFACT dist AS LOCAL .

sonarcloud:
    FROM openjdk:21-slim
    ARG SONAR_SCANNER_VERSION=4.8.0.2856
    RUN apt-get update && apt-get install -y wget unzip \
        &&  wget -U "scannercli" -q -O /opt/sonar-scanner-cli.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}.zip \
        && unzip /opt/sonar-scanner-cli.zip -d /opt && rm /opt/sonar-scanner-cli.zip \
        && ln -s /opt/sonar-scanner-${SONAR_SCANNER_VERSION}/bin/sonar-scanner /usr/local/bin/sonar-scanner

    ARG SONAR_TOKEN
    ARG SONAR_HOST_URL="https://sonarcloud.io"
    ARG SONAR_EXTRA_ARGS=""
    WORKDIR /app
    COPY . .
    RUN ls -la
    # Copy repository files (including coverage)
    RUN --mount=type=cache,target=/root/.sonar/cache \
                sonar-scanner \
                -Dsonar.login=${SONAR_TOKEN}  \
                -Dsonar.python.coverage.reportPaths=.test/coverage.xml \
                -Dsonar.python.xunit.reportPath=.test/junit.xml \
                ${SONAR_EXTRA_ARGS}
