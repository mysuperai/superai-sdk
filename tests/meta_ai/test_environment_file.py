import os.path

import pytest

from superai.meta_ai.environment_file import EnvironmentFileProcessor

LOCATION = "."


@pytest.fixture()
def environs():
    env = EnvironmentFileProcessor(location=LOCATION)
    yield env


@pytest.fixture()
def fresh():
    if os.path.exists(os.path.join(LOCATION, "environment")):
        os.remove(os.path.join(LOCATION, "environment"))


def test_file_created(fresh, environs):
    assert os.path.exists(os.path.join(LOCATION, "environment"))


def test_add_environ(fresh, environs):
    environs.add_or_update("MODEL", "MyModel")
    assert "MODEL" in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" in content


def test_add_environ_combined(fresh, environs):
    environs.add_or_update("MODEL=MyModel")
    assert "MODEL" in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" in content


def test_add_environ_multiple(fresh, environs):
    environs.add_or_update("MODEL", "MyModel")
    environs.add_or_update("PERSISTENCE", "0")
    assert "MODEL" in environs and "PERSISTENCE" in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" in content.split("\n") and "PERSISTENCE=0" in content.split("\n")


def test_add_environ_multiple_combined(fresh, environs):
    environs.add_or_update("MODEL = MyModel")
    environs.add_or_update("PERSISTENCE = 0")
    assert "MODEL" in environs and "PERSISTENCE" in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" in content.split("\n") and "PERSISTENCE=0" in content.split("\n")


def test_update_environ(environs):
    environs.add_or_update("MODEL", "MyModel")
    environs.add_or_update("MODEL", "MyOtherModel")
    assert "MODEL" in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyOtherModel" in content


def test_add_exception(fresh, environs):
    with pytest.raises(ValueError) as p:
        environs.add_or_update("MODEL")


def test_update_if_value_match(fresh, environs):
    environs.add_or_update("MODEL", "MyModel")
    environs.update_if_value_match(key="MODEL", value="MyModel", new_value="MyNewModel")
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyNewModel" in content


def test_update_if_value_match_combined(fresh, environs):
    environs.add_or_update("MODEL", "MyModel")
    environs.update_if_value_match(key="MODEL=MyModel", new_value="MyNewModel")
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyNewModel" in content


def test_update_exception(fresh, environs):
    with pytest.raises(ValueError) as p:
        environs.update_if_value_match(key="MODEL", new_value="Something")


def test_update_if_value_doesnt_match(fresh, environs):
    environs.add_or_update("MODEL", "MyModel")
    environs.update_if_value_match(key="MODEL", value="SomeModel", new_value="MyNewModel")
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" in content


def test_delete_environ(fresh, environs):
    environs.add_or_update("MODEL", "MyModel")
    environs.delete("MODEL")
    assert "MODEL" not in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" not in content


def test_delete_if_value_match(fresh, environs):
    environs.add_or_update("MODEL", "MyModel")
    environs.delete_if_value_match("MODEL", "MyModel")
    assert "MODEL" not in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" not in content


def test_delete_exception(fresh, environs):
    with pytest.raises(ValueError) as p:
        environs.delete_if_value_match(key="MODEL")


def test_delete_if_value_doesnt_match(fresh, environs):
    environs.add_or_update("MODEL", "MyModel")
    environs.delete_if_value_match("MODEL", "SomeModel")
    assert "MODEL" in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" in content


def test_delete_non_existing(fresh, environs):
    environs.delete("MODEL")


def test_delete_if_value_match_combined(fresh, environs):
    environs.add_or_update("MODEL=MyModel")
    environs.delete_if_value_match("MODEL=MyModel")
    assert "MODEL" not in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyModel" not in content


def test_object_delete(fresh, environs):
    environs.add_or_update("MODEL=MyModel")
    environs.clear()
    assert "MODEL" not in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert content == ""


def test_from_json(fresh, environs):
    environs.add_or_update("MODEL=MyModel")
    assert "something" not in environs
    environs.from_dict({"MODEL": "MyNewModel", "something": "else"})
    assert "MODEL" in environs and "something" in environs
    with open(os.path.join(LOCATION, "environment"), "r") as env_file:
        content = env_file.read()
    assert "MODEL=MyNewModel" in content.split("\n")
    assert "something=else" in content.split("\n")


def test_to_json(fresh, environs):
    environs.add_or_update("MODEL=MyModel")
    assert environs.to_dict() == {"MODEL": "MyModel"}
    assert environs.to_dict() == environs.environment_variables
