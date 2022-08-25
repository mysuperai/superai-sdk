import json

import dictdiffer
import pytest

from superai.meta_ai.parameters import (
    GPUVRAM,
    AiDeploymentParameters,
    HyperParameterSpec,
    ModelParameters,
    TrainingParameters,
    parameter_processor,
)


def test_parameter_processor():
    parameters = ["value=True"]
    processed_params = parameter_processor(parameters)
    assert processed_params == {"value": True}

    parameters = ["value1=0.001", "value2=[0.001, 0.01]", "value3=something"]
    processed_params = parameter_processor(parameters)
    assert processed_params == dict(value1=0.001, value2=[0.001, 0.01], value3="something")

    parameters = ["value2=['something', 'long', 'and', 'lengthy']"]
    processed_params = parameter_processor(parameters)
    assert processed_params == dict(value2=["something", "long", "and", "lengthy"])


def test_hyperparam_loading_known_params():
    parameters = ["trainable=True", "learning_rate=0.1", "validation_metric=accuracy"]
    hps = HyperParameterSpec.load_from_list(parameters)
    assert hps.trainable
    assert hps.learning_rate == 0.1
    assert hps.validation_metric == "accuracy"


def test_hyperparam_loading_unknown_params():
    parameters = ["some_fancy_param=something else"]
    hps = HyperParameterSpec.load_from_list(parameters)
    assert hps.some_fancy_param == "something else"

    defaulter = hps.get("some_random_key", "this value")
    assert defaulter == "this value"
    exister = hps.get("some_fancy_param", "something different altogether")
    assert exister == hps.some_fancy_param == "something else"

    with pytest.raises(KeyError) as e:
        hps.get("random_key")
    assert "HyperParameterSpec" in str(e.value)


def test_training_parameters():
    parameters = [
        "trainable=True",
        "learning_rate=0.1",
        "validation_metric=accuracy",
        "some_fancy_param=something else",
    ]
    hps = HyperParameterSpec.load_from_list(parameters)
    mps = ModelParameters(conv_layers=10, strides=[1, 1, 1])
    tps = TrainingParameters(
        training_data="some_training_data", test_data="some_test_data", hyperparameters=hps, model_parameter=mps
    )
    assert tps.to_json()
    print(tps.to_json())


def test_integration():
    ref_params = {
        "callbacks": None,
        "decoder_trainable": True,
        "encoder_trainable": True,
        "hyperparameters": {
            "batch_size": 128,
            "bucketing_field": None,
            "decay": None,
            "early_stop": 20,
            "epochs": 10,
            "eval_batch_size": 0,
            "increase_batch_size_eval_metric": "LOSS",
            "increase_batch_size_eval_split": "TRAINING",
            "increase_batch_size_on_plateau": 0,
            "increase_batch_size_on_plateau_max": 512,
            "increase_batch_size_on_plateau_patience": 5,
            "increase_batch_size_on_plateau_rate": 2,
            "learning_rate": 0.001,
            "learning_rate_warmup_epochs": 1,
            "log_learning_rate": -3,
            "optimizer": "adam",
            "reduce_learning_rate_eval_metric": "LOSS",
            "reduce_learning_rate_eval_split": "TRAINING",
            "reduce_learning_rate_on_plateau": 0,
            "reduce_learning_rate_on_plateau_patience": 5,
            "reduce_learning_rate_on_plateau_rate": 0.5,
            "regularization_lambda": 0.0,
            "resume": False,
            "skip_save_log": False,
            "skip_save_model": False,
            "skip_save_progress": False,
            "staircase": False,
            "trainable": True,
            "validation_field": "combined",
            "validation_metric": "loss",
        },
        "model_parameter": {
            "conv1_size": 32,
            "conv2_size": 64,
            "conv_activation": "relu",
            "conv_bias_initializer": "zeros",
            "conv_dropout": 0,
            "conv_layers": None,
            "conv_use_bias": True,
            "conv_weights_initializer": "glorot_uniform",
            "dilation_rate": [1, 1],
            "dropout": 0.8,
            "fc_activation": "relu",
            "fc_bias_initializer": "zeros",
            "fc_dropout": 0,
            "fc_size": 128,
            "fc_use_bias": True,
            "fc_weights_initializer": "glorot_uniform",
            "filter_size": 3,
            "hidden1_size": 500,
            "num_conv_layers": None,
            "num_fc_layers": 1,
            "num_filters": 32,
            "padding": "valid",
            "pool_function": "max",
            "strides": [1, 1],
        },
        "test_data_path": None,
        "validation_data_path": None,
        "production_data_path": None,
        "train_logger": None,
        "training_data_path": "/tmp",
    }
    tp = TrainingParameters(
        training_data="/tmp",
        hyperparameters=HyperParameterSpec(trainable=True, optimizer="adam", log_learning_rate=-3, epochs=10),
        model_parameter=ModelParameters(conv1_size=32, conv2_size=64, hidden1_size=500, dropout=0.8),
    )
    assert list(dictdiffer.diff(json.loads(tp.to_json()), ref_params)) == []


def test_deployment_parameters():
    dp = AiDeploymentParameters()
    assert dp
    dumped = dp.dict(by_alias=True, exclude_none=True)
    assert dumped
    assert "minReplicaCount" in dumped

    dp_parsed_json = AiDeploymentParameters.parse_raw(json.dumps(dp.dict(by_alias=True, exclude_none=True)))
    assert dp_parsed_json == dp

    cuda_dp = AiDeploymentParameters(enable_cuda=True)
    assert cuda_dp.enable_cuda

    big_vram_dp = AiDeploymentParameters(enable_cuda=True, gpu_memory_requirement=GPUVRAM.VRAM_24576)
    assert big_vram_dp.gpu_memory_requirement == GPUVRAM.VRAM_24576
    dumped = big_vram_dp.dict(by_alias=True, exclude_none=True)
    assert dumped["gpuMemoryRequirement"] == 24576

    always_on_dp = AiDeploymentParameters(min_replica_count=1, max_replica_count=10)
    assert always_on_dp

    big_memory_dp = AiDeploymentParameters(
        target_memory_requirement="2Gi", target_memory_limit="4Gi", target_average_utilization=1
    )
    assert big_memory_dp.target_memory_requirement == "2Gi"

    db_dict = big_memory_dp.dict_for_db()
    assert db_dict
    assert "enableCuda" not in db_dict
