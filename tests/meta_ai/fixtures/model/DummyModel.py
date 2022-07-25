import superai_schema.universal_schema.task_schema_functions as df

from superai.meta_ai import BaseModel
from superai.utils import log


class DummyModel(BaseModel):
    """
    Dummy model for testing, this is not a real model
    """

    model = None

    def __init__(self, *args, **kwargs):
        super(DummyModel, self).__init__(*args, **kwargs)

    def load_weights(self, weights_path):
        self.model = None

    def predict(self, inputs, *args, **kwargs):
        log.info(f"Predict Input: {inputs}")
        return [
            {
                "prediction": {
                    "mnist_class": df.exclusive_choice(
                        choices=list(map(str, range(10))),
                        selection=0,
                    )
                },
                "score": float(1),
            }
        ]

    def train(self, model_save_path, **kwargs):
        pass
