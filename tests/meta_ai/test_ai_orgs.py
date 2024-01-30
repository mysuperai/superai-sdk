import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Union
from unittest import mock
from unittest.mock import patch

import boto3
import pytest
from moto import mock_aws

from superai import settings
from superai.apis.auth import User
from superai.meta_ai.ai import AI
from superai.meta_ai.ai_helper import instantiate_superai
from superai.meta_ai.ai_uri import AiURI


@pytest.fixture(scope="module")
def vcr(vcr):
    """All local API requests to Meta-AI Api are recorded in a cassette.
    The main config lives in fixtures/ai_client_fixture.py.
    This just extends that config with some local overrides.

    To re-record the cassette, delete the cassette file and run the tests again.
    """
    # Add switch for debugging
    vcr.record_mode = "once"
    # Ignore AWS calls
    vcr.ignore_hosts = ["amazonaws.com"]
    return vcr


@pytest.fixture(scope="module")
def aws_credentials(monkeysession):
    """Mocked AWS Credentials for moto."""
    monkeysession.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeysession.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeysession.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeysession.setenv("AWS_SESSION_TOKEN", "testing")
    monkeysession.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture(scope="module", autouse=True)
def record_cassette(vcr, aws_credentials):
    """Record cassette for all API requests for tests in this module"""
    with vcr.use_cassette("test_ai_orgs.yaml"):
        yield


@pytest.fixture(scope="module", autouse=True)
def set_dev_env():
    with settings.using_env("dev"):
        yield


@pytest.fixture(scope="module")
def aws_credentials(monkeysession):
    """Mocked AWS Credentials for moto."""
    monkeysession.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeysession.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeysession.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeysession.setenv("AWS_SESSION_TOKEN", "testing")
    monkeysession.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture(scope="module")
def tmp_path():
    """Create deterministic temp dir so we can use it in the cassette without matching issues caused by random names"""
    temp = Path("/tmp/ai_test")
    temp.mkdir(parents=True, exist_ok=True)
    yield temp
    # remove dir and contents
    for f in temp.glob("*"):
        if f.is_dir():
            shutil.rmtree(f)
        else:
            f.unlink()


@pytest.fixture(scope="module")
def s3(aws_credentials):
    """Mocked S3 client for moto."""
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="module")
def ecr(aws_credentials, module_mocker):
    """Mocked ECR client for moto, disabled ECR login."""
    with mock_aws():
        # Disable unused ecr login
        module_mocker.patch("superai.meta_ai.ai_helper.aws_ecr_login", return_value=0)
        yield boto3.client("ecr")


@pytest.fixture(scope="module")
def sts(aws_credentials):
    """Mocked STS client for moto, hooks into SSO token logic."""
    with mock_aws():
        yield boto3.client("sts")


@pytest.fixture(scope="module")
def bucket(s3: boto3.client):
    """Create a bucket for testing uploads"""
    s3.create_bucket(
        Bucket=settings["meta_ai_bucket"],
    )


@pytest.fixture(scope="module")
def ai_name():
    """Generate static name for AI

    Was random before, but this caused issues with the cassette.
    """
    return "test_ai"


@pytest.fixture(scope="module")
def local_ai(bucket, ai_name, tmp_path, ecr, sts) -> AI:
    """Define local AI object for testing.
    It should be enough to specify the model class and the path to the model."""
    model_path = Path(__file__).parent / "fixtures" / "model"
    ai = AI(
        name=ai_name,
        model_class="DummyAI",
        model_class_path=str(model_path.absolute()),
        weights_path=tmp_path,
    )
    yield ai


@contextmanager
def user_session(org_id: Union[str, int], owner_id: Union[str, int]):
    """Mock Client with user A owner_id=2
    MetaAISession:
        @property
        def organization_id(self):
            return self._organization_id

        @property
        def owner_id(self):
            return self._owner_id
    """
    with mock.patch(
        "superai.apis.meta_ai.session.MetaAISession.organization_id",
        new_callable=mock.PropertyMock,
        return_value=str(org_id),
    ), mock.patch(
        "superai.apis.meta_ai.session.MetaAISession.owner_id",
        new_callable=mock.PropertyMock,
        return_value=str(owner_id),
    ):
        yield


@contextmanager
def superai_org_session():
    """Creates a session imitating superai org and owner id."""
    with user_session(org_id="1", owner_id="1"):
        yield


@contextmanager
def user_b_session():
    with user_session(org_id="2", owner_id="2"):
        yield


@pytest.fixture(scope="module", autouse=True)
def mock_user_api():
    dummy_data = {
        "id": "1",
        "created": "2023-03-23T13:02:47.285+00:00",
        "company": "RandomCo",
        "sysAdmin": True,
        "groups": ["GROUP1", "group2"],
        "plan": "FULL",
        "username": "random_user",
        "organizationMemberships": [
            {
                "id": 999,
                "status": "INACTIVE",
                "role": "MEMBER",
                "invited": "2021-08-17T09:59:52.926000+00:00",
                "accepted": "2021-08-17T10:00:13.596000+00:00",
                "created": "2021-08-17T09:59:52.926000+00:00",
                "orgId": 888,
                "orgUsername": "random_org",
                "userId": 111,
                "userEmail": "random@email.com",
            }
        ],
        "email": "random@email.com",
        "active": False,
    }
    user = User.parse_obj(dummy_data)

    with patch("superai.client.Client.get_user") as mock_get:
        mock_get.return_value = user
        yield


@pytest.fixture(scope="module")
def public_ai(local_ai: AI):
    """Save the local AI object to the backend and return the registered uuid"""
    local_ai.name = "public_ai"
    local_ai.visibility = "PUBLIC"
    with superai_org_session():
        ai_uuid = local_ai.save(overwrite=True)
    assert ai_uuid
    yield local_ai
    with superai_org_session():
        deleted = local_ai._client.delete_ai(local_ai.id)
    assert deleted


def test_load_public_ai(public_ai):
    """Test that we can load a public AI object"""
    my_id = 2
    with user_session(org_id=my_id, owner_id=my_id):
        ai = AI.load("ai://superai/public_ai")
        assert ai
        assert ai.name == public_ai.name
        instance = ai.create_instance("user_b_instance")
        assert instance
        assert instance.name == "user_b_instance"
        assert instance.visibility == "PRIVATE"
        assert instance.owner_id == my_id
        assert not instance.organization_id

        reload_ai = AI.load("ai://superai/public_ai")
        assert reload_ai
        assert reload_ai.owner_id != my_id
        assert not reload_ai.organization_id


@patch("superai.client.Client._get_user_id", return_value=3)
def test_instantiate_public_superai(mocked_user_id_call, public_ai):
    my_id = 3
    with user_session(org_id=my_id, owner_id=my_id):
        ai_uri = "ai://superai/public_ai"
        uri = AiURI.parse(ai_uri)
        my_instance = instantiate_superai(
            ai_name=uri.model_name, ai_version=uri.version, new_instance_name="user_b_instance"
        )
        assert my_instance
        assert my_instance.name == "user_b_instance"
        assert my_instance.visibility == "PRIVATE"
        assert my_instance.owner_id == my_id
        assert not my_instance.organization_id

        my_instance2 = instantiate_superai(
            ai_name=uri.model_name, ai_version=uri.version, new_instance_name="user_b_instance2"
        )
        assert my_instance2
        assert my_instance2.name == "user_b_instance2"
        assert my_instance2.visibility == "PRIVATE"
        assert my_instance2.owner_id == my_id
        assert not my_instance2.organization_id

        checkpoint1 = my_instance.get_checkpoint()
        checkpoint2 = my_instance2.get_checkpoint()
        assert checkpoint1.id != checkpoint2.id
        assert checkpoint1.template_id == checkpoint2.template_id
