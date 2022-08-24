import os.path

from diskcache import Cache

from superai import settings
from superai.data_program.experimental import memo, memoization


def method():
    return {"status": "COMPLETE", "result": "SOMETHING"}


def test_memo(monkeypatch, tmp_path):
    mocked_cache_settings = dict(directory=str(tmp_path), size_limit=settings.cache_size_in_bytes)
    monkeypatch.setattr(memoization, "_push_to_s3", lambda *args, **kwargs: None)
    monkeypatch.setattr(memoization, "_pull_from_s3", lambda *args, **kwargs: None)
    monkeypatch.setattr(memoization, "_refresh_push_to_s3", lambda *args, **kwargs: None)
    filename = "get_job_result/1231"
    filepath = os.path.join("memo", settings.name, filename)
    mocked_cache = Cache(**mocked_cache_settings)
    mocked_cache.delete(filepath)
    assert mocked_cache.get(filepath) is None
    mocked_cache[filepath] = method()
    monkeypatch.setattr(memoization, "cache_settings", mocked_cache_settings)
    result = memo(method, filename)
    assert result == method()
