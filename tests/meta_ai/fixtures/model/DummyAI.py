import superai_schema.universal_schema.task_schema_functions as df

from superai.meta_ai import BaseAI
from superai.utils import log


class DummyAI(BaseAI):
    """
    Dummy model for testing, this is not a real model
    """

    model = None

    def __init__(self, *args, **kwargs):
        super(DummyAI, self).__init__(*args, **kwargs)

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
