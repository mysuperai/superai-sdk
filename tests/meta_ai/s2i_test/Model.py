import json
import os

import sklearn
from test_local_folder.test_another_module import deep_imported_random_string
from testing_local_module import random_string

from superai.meta_ai import BaseModel
from superai.meta_ai.base.base_ai import default_random_seed
from superai.meta_ai.parameters import HyperParameterSpec, ModelParameters


class Model(BaseModel):
    @classmethod
    def load_weights(cls, weights_path):
        print(sklearn.__version__)
        print(list(os.walk(weights_path)))

    def predict(self, inputs, context=None):
        print(random_string())
        print(deep_imported_random_string())
        return [{"prediction": f"some_sort_of_prediction_for_{json.dumps(inputs)}", "score": 0}]

    def predict_raw(self, inputs):
        return self.predict(inputs)

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
