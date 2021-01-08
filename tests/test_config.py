from os import makedirs, rename
from pathlib import Path
from random import random
from typing import Optional

import pytest
import yaml

from superai.config import (
    __env_switcher,
    __local_settings_path,
    __secrets_path,
    __settings_path,
    add_secret_settings,
    get_config_dir,
    list_env_configs,
    set_env_config,
)

base_dir = Path(get_config_dir()).expanduser()


def _mv_file(src: Path, dst: Path = None) -> Optional[Path]:
    # Nothing to do
    if not src:
        return

    file_path = Path(src).expanduser()
    tmp_file_path = Path(dst).expanduser() if dst else Path(f"{file_path.absolute()}.{random()}")

    # Nothing to do
    if not file_path.exists():
        return None

    # # Do not override existing tmp file since that indicates that a previous test didn't clean properly
    if tmp_file_path.exists():
        raise ValueError(f"tmp_path {dst} exists already")

    rename(file_path.absolute(), tmp_file_path.absolute())

    return tmp_file_path


def _setup_file(file_path: Path) -> Path:
    makedirs(base_dir.absolute(), exist_ok=True)
    f_path = Path(file_path).expanduser().absolute()
    tmp = _mv_file(f_path)

    if not f_path.exists():
        f_path.touch()
    return tmp


@pytest.fixture()
def with_secrets_file():
    s_path = Path(__secrets_path).expanduser().absolute()
    tmp = _setup_file(s_path)
    yield str(s_path.absolute())
    s_path.unlink()
    if tmp:
        _mv_file(tmp, s_path)
        assert s_path.exists()


@pytest.fixture()
def with_settings_file():
    s_path = Path(__settings_path).expanduser().absolute()
    tmp = _setup_file(s_path)
    yield str(s_path.absolute())
    s_path.unlink()
    if tmp:
        _mv_file(tmp, s_path)
        assert s_path.exists()


@pytest.fixture()
def with_dotenv_file():
    dot_env_path = base_dir / ".env"
    s_path = Path(dot_env_path).expanduser().absolute()
    tmp = _setup_file(s_path)
    yield str(s_path.absolute())
    s_path.unlink()
    if tmp:
        _mv_file(tmp, s_path)
        assert s_path.exists()


def test_root_dir_created():
    """
    If the init method is run, then the base folder should exist
    """
    assert base_dir.absolute().exists()


def test_file_is_not_modified_with_emtpy_content(with_secrets_file):
    secrets_path = Path(with_secrets_file).expanduser().absolute()
    with open(secrets_path, "r") as f:
        secrets_before = dict(yaml.load(f, yaml.SafeLoader) or {})
    content = None
    add_secret_settings(content)
    with open(secrets_path, "r") as f:
        secrets_after = dict(yaml.load(f, yaml.SafeLoader) or {})
    assert secrets_before == secrets_after


def test_new_content_is_added(with_secrets_file):
    secrets_path = Path(with_secrets_file).expanduser().absolute()
    content = {"my_test_content": "testing"}
    add_secret_settings(content)
    with open(secrets_path, "r") as f:
        secrets_after = dict(yaml.load(f, yaml.SafeLoader) or {})

    assert secrets_after.items() <= content.items()


def test_new_content_override(with_secrets_file):
    secrets_path = Path(with_secrets_file).expanduser().absolute()
    content = {"my_key": "testing"}
    add_secret_settings(content)
    with open(secrets_path, "r") as f:
        secrets_after = dict(yaml.load(f, yaml.SafeLoader) or {})
    assert secrets_after == content
    content = {"my_key": "modified"}
    add_secret_settings(content)
    with open(secrets_path, "r") as f:
        secrets_after = dict(yaml.load(f, yaml.SafeLoader) or {})
    assert secrets_after.items() <= content.items()


def test_list_envs_ignores(capsys):
    local_settings = Path(__local_settings_path).expanduser().absolute()
    with open(local_settings, "r") as f:
        settings_dict = dict(yaml.load(f, yaml.SafeLoader) or {})
    assert settings_dict["testing"] and settings_dict["default"]
    assert list_env_configs()["testing"]
    assert not list_env_configs().get("default")
    captured = capsys.readouterr()
    assert "- default" not in captured.out
    assert "- testing" not in captured.out
    assert "- sandbox" in captured.out
    assert "- prod" in captured.out


def test_set_env_success():
    dot_env_path = Path(base_dir / ".env").expanduser().absolute()
    set_env_config("testing")
    env = f"{__env_switcher}=testing"
    with open(dot_env_path, "r") as f:
        dot_env = f.readline()
    assert dot_env == env


@pytest.mark.xfail(ValueError, reason="Env config doesn't exist")
def test_set_env_fails_not_existent(with_dotenv_file):
    set_env_config("d")
