import json

import dictdiffer

from superai.meta_ai.parameters import (
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
