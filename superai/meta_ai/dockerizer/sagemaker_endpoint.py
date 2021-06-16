import json
import os
import time

import boto3
import requests
import sagemaker
from botocore.exceptions import ClientError
from sagemaker import get_execution_role

from superai import log


def create_endpoint(
    arn_role=None,
    region="us-east-1",
    image_name=None,
    version="latest",
    model_url=None,
    initial_instance_count=1,
    instance_type="ml.m5.xlarge",
    mode="SingleModel",
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
    """
    sm_client = boto3.client(service_name="sagemaker")
    if arn_role is not None:
        # arn_role = "arn:aws:iam::185169359328:role/service-role/AmazonSageMaker-ExecutionRole-20180117T160866"
        sts_client = boto3.client("sts")
        assumed_role_object = sts_client.assume_role(
            RoleArn=arn_role, RoleSessionName="MultiEndpointSession", ExternalId="0c18cdd7-3626-497d-8c4e-f3fb5ce76cd1"
        )
        credentials = assumed_role_object["Credentials"]
        boto_session = boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
            region_name=region,
        )
        account_id = sts_client.get_caller_identity()["Account"]
        region = boto_session.region_name
        sagemaker_session = sagemaker.Session(boto_session=boto_session)
        role = get_execution_role(sagemaker_session)
    else:
        region = boto3.Session().region_name
        role = get_execution_role()
        account_id = boto3.client("sts").get_caller_identity()["Account"]

    container = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:{version}"
    model_name = f"DEMO-{image_name.replace('_', '-')}-{version}-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    log.info("Container image: " + container)
    log.info("Model name: " + model_name)
    log.info("Model data Url: " + model_url)

    assert mode in ["SingleModel", "MultiModel"], "Mode should be one of ['SingleModel', 'MultiModel']"
    container = {"Image": container, "ModelDataUrl": model_url, "Mode": mode}

    try:
        create_model_response = sm_client.create_model(
            ModelName=model_name, ExecutionRoleArn=role, Containers=[container]
        )
    except Exception as e:
        if mode == "SingleModel":
            assert model_url.endswith(".tar.gz"), "For SingleModel mode, you need to provide a path to `tar.gz`"
        log.error("Check that `model_url` is a folder for `MultiModel` mode and a `tar.gz` for `SingleModel`")
        raise e

    log.info("Model Arn: " + create_model_response["ModelArn"])

    endpoint_config_name = f"Deploy-{image_name.replace('_', '-')}-{version}-" + time.strftime(
        "%Y-%m-%d-%H-%M-%S", time.gmtime()
    )
    log.info("Endpoint config name: " + endpoint_config_name)

    create_endpoint_config_response = sm_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                "InstanceType": instance_type,
                "InitialInstanceCount": initial_instance_count,
                "InitialVariantWeight": 1,
                "ModelName": model_name,
                "VariantName": "AllTraffic",
            }
        ],
    )

    log.info("Endpoint config Arn: " + create_endpoint_config_response["EndpointConfigArn"])

    endpoint_name = f"DEMO-{image_name.replace('_', '-')}-{version}"
    log.info("Endpoint name: " + endpoint_name)
    try:
        create_endpoint_response = sm_client.create_endpoint(
            EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
        )
    except ClientError:
        log.info("Endpoint already exists, deleting and recreating")
        sm_client.delete_endpoint(EndpointName=endpoint_name)
        time.sleep(5)
        create_endpoint_response = sm_client.create_endpoint(
            EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
        )
    log.info("Endpoint Arn: " + create_endpoint_response["EndpointArn"])

    resp = sm_client.describe_endpoint(EndpointName=endpoint_name)
    status = resp["EndpointStatus"]
    log.info("Endpoint Status: " + status)

    log.info("Waiting for {} endpoint to be in service...".format(endpoint_name))
    waiter = sm_client.get_waiter("endpoint_in_service")
    waiter.wait(EndpointName=endpoint_name)
    log.info(f"{create_endpoint_response['EndpointArn']} ready for invocations")


def upload_model_to_s3(bucket: str, prefix: str, model: str):
    """
    Upload model file to s3, model file should end with .tar.gz
    :param bucket: Bucket name in s3
    :param prefix: Prefix name
    :param model: Path to model file
    """
    assert model.endswith(".tar.gz"), "Model path should point to a tar.gz file"
    s3 = boto3.resource("s3")
    try:
        s3.meta.client.head_bucket(Bucket=bucket)
    except ClientError:
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": boto3.Session().region_name})

    key = os.path.join(prefix, model)
    with open("data/" + model, "rb") as file_obj:
        s3.Bucket(bucket).Object(key).upload_fileobj(file_obj)
        log.info(f"Loaded model to bucket: {bucket}, prefix: {prefix}, with path: {model}")


def invoke_local(mime: str, body: str):
    """
    Send a post request to the locally deployed docker container
    :param mime: MIME type
    :param body: Body or path to file to be passed as payload
    """
    url = f"http://localhost/model/predict"
    headers = {"Content-Type": mime}
    if mime.endswith("json"):
        res = requests.post(url, json=body, headers=headers)
    else:
        if os.path.exists(body):
            with open(body, "rb") as f:
                payload = f.read()
        else:
            payload = body
        res = requests.post(url, data=payload, headers=headers)
    if res.status_code == 200:
        log.info(res.json())
    else:
        message = "Error , received error code {}: {}".format(res.status_code, res.text)
        log.error(message)


def invoke_sagemaker_endpoint(endpoint, mime, payload, mode="SingleModel", target_model=None, arn_role=None):
    # arn_role = "arn:aws:iam::185169359328:role/service-role/AmazonSageMaker-ExecutionRole-20180117T160866"
    assert mode in ["SingleModel", "MultiModel"], "Mode should be one of ['SingleModel', 'MultiModel']"
    if mode == "MultiModel":
        assert target_model is not None, "TargetModel is required when using 'MultiModel' mode"
        assert target_model.endswith(
            ".tar.gz"
        ), "TargetModel should point to a 'tar.gz' file. Just the file name should be enough"
    if arn_role is None:
        runtime_sm_client = boto3.client(service_name="sagemaker-runtime")
    else:
        sts_client = boto3.client("sts")
        ext_id = "0c18cdd7-3626-497d-8c4e-f3fb5ce76cd1"
        assumed_role_object = sts_client.assume_role(
            RoleArn=arn_role, RoleSessionName="MultiEndpointSession", ExternalId=ext_id
        )
        credentials = assumed_role_object["Credentials"]
        boto_session = boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
            region_name="us-east-1",
        )
        runtime_sm_client = boto_session.client(service_name="sagemaker-runtime")
    body = payload
    if not mime.endswith("json"):
        if os.path.exists(payload):
            with open(payload, "rb") as f:
                body = f.read()
    if mode == "SingleModel":
        response = runtime_sm_client.invoke_endpoint(EndpointName=endpoint, ContentType=mime, Body=body)
    else:
        response = runtime_sm_client.invoke_endpoint(
            EndpointName=endpoint,
            ContentType=mime,
            TargetModel=target_model,
            Body=body,
        )
    log.info(f"Response from endpoint: {response}")
    response = json.loads(response["Body"].read())
    log.info(f"Model response: {response}")
    return response


if __name__ == "__main__":
    create_endpoint(
        arn_role="arn:aws:iam::185169359328:role/service-role/AmazonSageMaker-ExecutionRole-20180117T160866",
        image_name="genre_model",
        version="2",
        model_url="s3://canotic-ai/meta_ai_models/saved_models/fairseq_entity_disambiguation_aidayago.tar.gz",
    )
    invoke_sagemaker_endpoint(
        endpoint="DEMO-genre-model-2",
        mime="application/json",
        payload='{"data":{"sentences": ["Einstein was a [START_ENT] German [END_ENT] physicist."]}}',
    )
