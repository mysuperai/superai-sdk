from superai.data_program.hatchery import BuildConfig, RuntimeConfig


def test_build_config_defaults():
    build_config = BuildConfig()
    assert build_config.agent.host
    assert build_config.agent.websocket.endswith("/agent")
    assert build_config.api_key
    assert isinstance(build_config.args, list)
    assert build_config.build == False
    assert build_config.build_folder == ".hatchery"
    assert build_config.version


def test_runtime_config_defaults():
    name = "test_name"
    runtime_config = RuntimeConfig(name)
    assert runtime_config.concurrency == 100
    assert not runtime_config.container
    assert not runtime_config.force_schema
    assert runtime_config.local
    assert runtime_config.name == name
    assert runtime_config.py3
    assert runtime_config.serve
    assert not runtime_config.simulation
