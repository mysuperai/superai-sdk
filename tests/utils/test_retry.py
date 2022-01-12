from superai.utils import retry
import pytest


def test_retry_logging(caplog):
    @retry(exceptions=Exception, tries=2, logger=None)
    def failing_print():
        raise Exception("Timeout Error")

    with pytest.raises(Exception):
        failing_print()
    assert "Last retry failed:" not in caplog.text


def test_retry_print(caplog):
    @retry(exceptions=Exception, tries=2)
    def failing():
        raise Exception("Timeout Error")

    with pytest.raises(Exception):
        failing()
    assert "Last retry failed:" in caplog.text


def test_sucess_retry(caplog):
    @retry(exceptions=Exception, tries=2)
    def success():
        return True

    assert success()
    assert "retry" not in caplog.text
