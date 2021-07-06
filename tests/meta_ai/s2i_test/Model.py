import json
import os

from superai.meta_ai import BaseModel
from superai.meta_ai.base.base_ai import default_random_seed
from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters

import sklearn


class Model(BaseModel):
    @classmethod
    def load_weights(cls, weights_path):
        print(sklearn.__version__)
        print(list(os.walk(weights_path)))
        pass

    def predict(self, inputs):
        return [{"prediction": f"some_sort_of_prediction_for_{json.dumps(inputs)}", "score": 0}]

    def train(
        self,
        model_save_path,
        training_data,
        validation_data=None,
        test_data=None,
        production_data=None,
        encoder_trainable: bool = True,
        decoder_trainable: bool = True,
        hyperparameters: HyperParameterSpec = None,
        model_parameters: ModelParameters = None,
        callbacks=None,
        random_seed=default_random_seed,
    ):
        pass

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
