import time
from typing import Iterable, Optional, Sequence, Union

import boto3
from sagemaker import get_execution_role
from superai.log import logger

from .model import add_model


def deploy_add_model(
    name,
    version=1,
    description="",
    endpoint="",
    metadata=None,
    model_url="",
    instance_type="ml.p2.xlarge",
    initial_instance_count=1,
    mode="SingleModel",
):
    create_endpoint(
        name,
        model_url,
        instance_type=instance_type,
        mode=mode,
        initial_instance_count=initial_instance_count,
        endpoint_name=endpoint,
    )
    id = add_model(name, description=description, version=version, endpoint=endpoint, metadata=metadata)
    return id


def create_endpoint(
    image_name: str = None,
    model_url: str = None,
    initial_instance_count: int = 1,
    instance_type: str = "ml.m5.xlarge",
    mode: str = "SingleModel",
    endpoint_name: Optional[str] = None,
):
    """
    Create endpoint on AWS Sagemaker
    :param image_name: Base image name which is already pushed on ECR
    :param model_url: S3 URI of location where the model weights and params are placed.
                      for :param mode="MultiModel" this is a folder location and
                      for :param mode="SingleModel" this should be a location to a `tar.gz` file
    :param initial_instance_count: Number of instances to serve on the endpoint
    :param instance_type: Type of AWS instance to be used in the endpoint. Note that you cannot use GPU instances for
                          :param mode="MultiModel"
    :param mode: "SingleModel" or "MultiModel" type of instance to use
    :param endpoint_name: If given, the endpoint will be created with this name
    """

    sm_client = boto3.client(service_name="sagemaker")
    region: str = boto3.Session().region_name
    role: str = get_execution_role()
    account_id: str = boto3.client("sts").get_caller_identity()["Account"]

    container = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:latest"
    logger.info("Container image: " + container)
    logger.info("Model name: " + image_name)
    logger.info("Model data Url: " + model_url)

    assert mode in [
        "SingleModel",
        "MultiModel",
    ], "Mode should be one of ['SingleModel', 'MultiModel']"
    container = {"Image": container, "ModelDataUrl": model_url, "Mode": mode}

    try:
        create_model_response: dict = sm_client.create_model(
            ModelName=image_name, ExecutionRoleArn=role, Containers=[container]
        )
    except Exception as e:
        if mode == "SingleModel":
            assert model_url.endswith(".tar.gz"), "For SingleModel mode, you need to provide a path to `tar.gz`"
        logger.error("Check that `model_url` is a folder for `MultiModel` mode and a `tar.gz` for `SingleModel`")
        raise e

    logger.info("Model Arn: " + create_model_response["ModelArn"])

    endpoint_config_name: str = f"Deploy-{image_name}-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    logger.info("Endpoint config name: " + endpoint_config_name)

    create_endpoint_config_response: dict = sm_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                "InstanceType": instance_type,
                "InitialInstanceCount": initial_instance_count,
                "InitialVariantWeight": 1,
                "ModelName": image_name,
                "VariantName": "AllTraffic",
            }
        ],
    )

    logger.info("Endpoint config Arn: " + create_endpoint_config_response["EndpointConfigArn"])
    if endpoint_name is None:
        endpoint_name: str = f"DEMO-{image_name}-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    logger.info("Endpoint name: " + endpoint_name)

    create_endpoint_response: dict = sm_client.create_endpoint(
        EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
    )
    logger.info("Endpoint Arn: " + create_endpoint_response["EndpointArn"])

    resp: dict = sm_client.describe_endpoint(EndpointName=endpoint_name)
    status = resp["EndpointStatus"]
    logger.info("Endpoint Status: " + status)

    logger.info("Waiting for {} endpoint to be in service...".format(endpoint_name))
    waiter = sm_client.get_waiter("endpoint_in_service")
    waiter.wait(EndpointName=endpoint_name)
    logger.info(f"{create_endpoint_response['EndpointArn']} ready for invocations")
    return endpoint_name
