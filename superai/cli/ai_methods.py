import pathlib

import click


@click.group(name="method")
def ai_method_group():
    """Directly call the AI methods to train and predict"""


@ai_method_group.command("train", help="Start training of an AI object")
@click.option(
    "--path",
    "-p",
    default=".",
    help="Path to AI object save location. A new AI template and instance will be created from this path. Ensure this "
    "is the absolute path",
    required=True,
    type=click.Path(exists=True, readable=True, dir_okay=True),
)
@click.option(
    "--model-save-path",
    "-mp",
    help="Path to location where the weights will be saved.",
    required=True,
    show_default=True,
    type=click.Path(),
)
@click.option(
    "--training-data-path",
    "-tp",
    help="Path to location where the training data is stored in the local file system.",
    required=True,
    type=click.Path(exists=False, readable=False),
)
@click.option(
    "--test-data-path",
    "-tsp",
    help="Path to location where the test data is stored in the local file system.",
    type=click.Path(exists=False, readable=False),
)
@click.option(
    "--validation-data-path",
    "-vp",
    help="Path to location where the validation data is stored in the local file system.",
    type=click.Path(exists=False, readable=False),
)
@click.option(
    "--production-data-path",
    "-pp",
    help="Path to location where the production data is stored in the local file system.",
    type=click.Path(exists=False, readable=False),
)
@click.option(
    "--weights-path",
    "-wp",
    help="Path to location where the existing weights is stored local file system.",
    type=click.Path(exists=False, readable=False),
)
@click.option("--encoder-trainable/--no-encoder-trainable", default=False, show_default=True, type=bool)
@click.option("--decoder-trainable/--no-decoder-trainable", default=False, show_default=True, type=bool)
@click.option(
    "--hyperparameters",
    "-h",
    multiple=True,
    help="Hyperparameters to be passed. Please pass them as `-h train_split=0.2 -h cross_valid=False`",
)
@click.option(
    "--model-parameters",
    "-m",
    multiple=True,
    help="Model parameters to be passed. Please pass them as `-m some_parameter=0.2 -h other_parameter=False -h "
    "listed=['list','of','strings']`",
)
@click.option(
    "--callbacks",
    "-cl",
    help="Callbacks to be passed to training (yet to be implemented)",
)
@click.option(
    "--train-logger",
    "-tl",
    multiple=True,
    help="Train logger (yet to be implemented)",
)
def train(
    path,
    model_save_path,
    training_data_path,
    test_data_path,
    validation_data_path,
    production_data_path,
    weights_path,
    encoder_trainable,
    decoder_trainable,
    hyperparameters,
    model_parameters,
    callbacks,
    train_logger,
):
    """Start training locally"""
    from superai.meta_ai.ai import AI
    from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters

    click.echo(
        f"Starting training from the path {path} with hyperparameters {hyperparameters} "
        f"and model parameters {model_parameters}"
    )
    processed_hyperparameters = HyperParameterSpec.load_from_list(hyperparameters)
    processed_model_parameters = ModelParameters.load_from_list(model_parameters)
    ai_object = AI.load(path, weights_path=weights_path, pull_db_data=False)
    ai_object.train(
        model_save_path=model_save_path,
        training_data=training_data_path,
        test_data=test_data_path,
        production_data=production_data_path,
        validation_data=validation_data_path,
        weights_path=weights_path,
        encoder_trainable=encoder_trainable,
        decoder_trainable=decoder_trainable,
        hyperparameters=processed_hyperparameters,
        model_parameters=processed_model_parameters,
        callbacks=callbacks,
        train_logger=train_logger,
    )


@ai_method_group.command("predict", help="Predict from AI")
@click.option(
    "--path",
    "-p",
    default=".",
    help="Path to AI object save location. A new AI template and instance will be created from this path",
    required=True,
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--data-path",
    "-dp",
    help="Path to file location where the input data is stored in the local file system.",
    type=click.Path(exists=True, readable=True, dir_okay=False),
    required=False,
)
@click.option("--json-input", "-i", required=False, type=str, help="Prediction input. Should be a valid JSON string")
@click.option(
    "--weights-path",
    "-wp",
    required=False,
    help="Path to weights to be loaded",
    type=click.Path(exists=True, readable=True),
)
@click.option(
    "--metrics-output-dir",
    required=False,
    help="If provided, metrics will be computed and saved to this directory.",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
)
def predict(path, json_input=None, data_path: str = None, weights_path=None, metrics_output_dir=None):
    """Load a model and predict"""
    from superai.meta_ai.ai_helper import load_and_predict

    result = load_and_predict(
        model_path=path,
        weights_path=weights_path,
        data_path=data_path,
        json_input=json_input,
        metrics_output_dir=metrics_output_dir,
    )
    click.echo(f"Result : {result}")
