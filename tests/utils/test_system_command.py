import pytest

from superai.utils import system


def test_system():
    assert system("ls") == 0
    with pytest.raises(FileNotFoundError):
        assert system("aaaaaaaaaa") == -1
