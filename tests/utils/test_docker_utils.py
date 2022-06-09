import pytest

from superai.meta_ai.dockerizer import aws_ecr_login, get_boto_session


@pytest.mark.skip("Not supported in CI")
def test_ecr_login():
    region = "us-east-1"
    boto_session = get_boto_session(region_name=region)
    account = boto_session.client("sts").get_caller_identity()["Account"]
    registry_name = f"{account}.dkr.ecr.{region}.amazonaws.com"
    code = aws_ecr_login(region, registry_name)
    assert code == 0
