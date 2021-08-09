import importlib
import json
import os
import platform
from typing import Optional, Dict, List, Union

import pandas as pd
from jinja2 import Template
from superai import Client
from superai.log import logger
from superai.meta_ai.template_contents import entry_script
from superai.utils import load_api_key, load_auth_token, load_id_token

log = logger.get_logger(__name__)


def prepare_dockerfile_string(
    force_amd64: bool = False,
    enable_cuda: bool = False,
    lambda_mode: bool = False,
    conda_env: Optional[str] = None,
    requirements: Optional[str] = None,
    artifacts: Optional[dict] = None,
    dockerd_entrypoint: str = "dockerd-entrypoint.py",
    location: Optional[str] = None,
):
    """
    Prepare the dockerfile content according to the configuration
    Args:
        force_amd64: Use amd64 for container build
        enable_cuda: Enable CUDA to use GPU
        lambda_mode: Lambda mode for container build
        conda_env: Optional Conda Environment
        requirements: Optional requirements file
        artifacts: Optional artifacts file
        dockerd_entrypoint: File name of docker entrypoint
        location: Path location of where to write the dependencies
    Returns:
        String containing the Dockerfile
    """
    homedir = "/home/model-server/"

    ################################################################################################################
    # Select Base
    ################################################################################################################
    dockerfile_content = [
        "# syntax=docker/dockerfile:1.2",
    ]

    platform_string = "--platform=linux/amd64" if force_amd64 else ""
    if enable_cuda:
        dockerfile_content.append(f"FROM {platform_string} nvidia/cuda:10.2-cudnn8-runtime-ubuntu18.04")
    else:
        dockerfile_content.append(f"FROM {platform_string} python:3.7.11-slim-buster")

    ################################################################################################################
    # Install System Dependencies
    ################################################################################################################
    if not lambda_mode:
        dockerfile_content.extend(
            [
                "\nRUN mkdir -p /usr/share/man/man1",
                "\nRUN apt-get update "
                "&& apt-get -y install --no-install-recommends build-essential ca-certificates default-jdk curl "
                "&& apt-get clean && rm -rf /var/lib/apt/lists/*",
                "\nLABEL com.amazonaws.sagemaker.capabilities.multi-models=true",
                "LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true",
            ]
        )
    else:
        dockerfile_content.extend(
            [
                "RUN apt-get update && "
                "apt-get -y install --no-install-recommends build-essential ca-certificates g++"
                " make cmake unzip libcurl4-openssl-dev curl "
                "&& apt-get clean && rm -rf /var/lib/apt/lists/*"
            ]
        )
    dockerfile_content.append(f"RUN mkdir -p {homedir}")
    ################################################################################################################
    # Install Conda and initialize
    ################################################################################################################
    aarch = "x86_64" if force_amd64 or platform.machine() == "x86_64" else "aarch64"
    conda_installer = f"Anaconda3-2021.05-Linux-{aarch}.sh"
    dockerfile_content.extend(
        [
            "# Download and install Anaconda.",
            f"RUN cd /tmp && curl -O https://repo.anaconda.com/archive/{conda_installer} "
            f"&& chmod +x /tmp/{conda_installer}",
            f'RUN mkdir /root/.conda && bash -c "/tmp/{conda_installer} -b -p /opt/conda"',
        ]
    )
    ################################################################################################################
    # Create Conda Environment
    ################################################################################################################
    if conda_env is not None:
        dockerfile_content.extend(
            [
                f"COPY conda.yml {homedir}",
                f"RUN /opt/conda/bin/conda env create -f {os.path.join(homedir, 'conda.yml')} -n env",
            ]
        )
    else:
        dockerfile_content.append("RUN /opt/conda/bin/conda create -n env python=3.7.10")
    dockerfile_content.extend(
        [
            'RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc ' '&& echo "conda activate env" >> ~/.bashrc',
            "ENV PATH /opt/conda/envs/env/bin:$PATH",
        ]
    )
    env_name = "env"

    dockerfile_content.append(
        f'SHELL ["/opt/conda/bin/conda", "run", "--no-capture-output", "-n", "{env_name}", "/bin/bash", "-c"]'
    )

    ################################################################################################################
    # Install Serving Requirements
    ################################################################################################################
    if not lambda_mode:
        serving_reqs = "multi-model-server sagemaker-inference retrying awscli~=1.18.195"
    else:
        serving_reqs = "awslambdaric awscli~=1.18.195"
    dockerfile_content.append(f"RUN pip install --no-cache-dir {serving_reqs}")

    ################################################################################################################
    # Install pip requirements
    ################################################################################################################
    superai_reqs = "superai_schema superai"
    dockerfile_content.extend(
        [
            'RUN echo "export SUPERAI_CONFIG_ROOT=/tmp/.superai" >> ~/.bashrc',
            "ARG AWS_DEFAULT_REGION=us-east-1",
            "RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true"
            " --mount=type=cache,target=/opt/conda/pkgs "
            f"aws codeartifact login --tool pip --domain superai --repository pypi-superai && "
            f"pip install --no-cache-dir {superai_reqs}",
        ]
    )
    dockerfile_content.extend(
        [
            f"",
            f"### Model specific dependencies ",
        ],
    )

    ################################################################################################################
    # Custom install commands (require copy of workdir)
    ################################################################################################################
    dockerfile_content.append(f"WORKDIR {homedir}")
    if requirements:
        # Only copy and install requirements file to allow better caching
        dockerfile_content.extend(
            [
                "COPY requirements.txt . ",
                "RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true"
                " --mount=type=cache,target=/opt/conda/pkgs "
                f"aws codeartifact login --tool pip --domain superai --repository pypi-superai && "
                "pip install -r requirements.txt",
            ]
        )

    ################################################################################################################
    # Copy complete contents of local folder
    ################################################################################################################
    dockerfile_content.append(f"COPY . {homedir}")
    if artifacts is not None:
        if "run" in artifacts:
            dockerfile_content.extend(
                [
                    f"RUN chmod +x {os.path.join(homedir, artifacts['run'])}",
                    "RUN --mount=type=secret,id=aws,target=/root/.aws/credentials,required=true "
                    "--mount=type=cache,target=/opt/conda/pkgs "
                    f"aws codeartifact login --tool pip --domain superai --repository pypi-superai && "
                    f"bash {os.path.join(homedir, artifacts['run'])}",
                ]
            )

    ################################################################################################################
    # Create and initialize entrypoint to container
    ################################################################################################################
    if not lambda_mode:
        dockerfile_content.extend(
            [
                f"RUN chmod +x {os.path.join(homedir, dockerd_entrypoint)}",
                f'ENTRYPOINT ["/opt/conda/bin/conda", "run", "--no-capture-output", "-n", "{env_name}", "python",'
                f' "{os.path.join(homedir, dockerd_entrypoint)}"]',
                'CMD ["serve"]',
            ]
        )
    else:
        rie_url = "https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie"
        with open(os.path.join(location, "entry_script.sh"), "w") as entry_file_writer:
            template = Template(entry_script)
            entry_script_args = dict(env=env_name)
            entry_file_content: str = template.render(entry_script_args)
            entry_file_writer.write(entry_file_content)
        dockerfile_content.extend(
            [
                f"ADD {rie_url} /usr/local/bin/aws-lambda-rie",
                f"RUN chmod +x /usr/local/bin/aws-lambda-rie && chmod +x {os.path.join(homedir, 'entry_script.sh')}",
                f"ENTRYPOINT [\"{os.path.join(homedir, 'entry_script.sh')}\"]",
                'CMD ["handler.processor"]',
            ]
        )

    return dockerfile_content


def list_models(
    ai_name: str,
    client: Client = Client(
        api_key=load_api_key(),
        auth_token=load_auth_token(),
        id_token=load_id_token(),
    ),
    raw: bool = False,
    verbose: bool = True,
) -> Union[List[Dict], pd.DataFrame]:
    """List existing models in the database, given the model name.

    Args:
        verbose: Print the output.
        raw: Return unformatted list of models.
        client: Instance of superai.client.
        ai_name: Name of the AI model.
    """

    model_entries = client.get_model_by_name(ai_name)
    if raw:
        if verbose:
            log.info(json.dumps(model_entries, indent=1))
        return model_entries
    else:
        table = pd.DataFrame.from_dict(model_entries)
        if verbose:
            pd.set_option("display.max_colwidth", None)
            log.info(table)
        return table


def get_user_model_class(model_name, path: str = "."):
    """Obtain a class definition given the path to the class module"""
    cwd = os.getcwd()
    if path != ".":
        os.chdir(path)
    parts = model_name.rsplit(".", 1)
    if len(parts) == 1:
        logger.info(f"Importing {model_name}")
        interface_file = importlib.import_module(model_name)
        user_class = getattr(interface_file, model_name)
    else:
        logger.info(f"Importing submodule {parts}")
        interface_file = importlib.import_module(parts[0])
        user_class = getattr(interface_file, parts[1])
    if path != ".":
        os.chdir(cwd)
    return user_class
