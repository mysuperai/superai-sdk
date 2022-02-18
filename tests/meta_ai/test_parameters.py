from superai.meta_ai.parameters import parameter_processor, HyperParameterSpec


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
