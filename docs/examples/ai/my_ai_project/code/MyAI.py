from superai.log import get_logger
from superai.meta_ai import BaseAI

log = get_logger(__name__)


class MyAI(BaseAI):
    model = None

    def __init__(self, *args, **kwargs):
        super(MyAI, self).__init__(*args, **kwargs)
        # Custom init logic

    def load_weights(self, weights_path):
        self.model = None
        # self.model = LinearRegression()

    def predict(self, inputs, *args, **kwargs):
        log.info(f"Predict Input: {inputs}")

        # Example of using the model to make a prediction
        # self.model.predict(inputs)

        # The prediction needs to be a list of prediction instances, each containing prediction data and a score
        prediction_list = [
            {
                "prediction": {"mnist_class": "1"},
                "score": float(1),
            }
        ]
        return prediction_list

    def train(self, model_save_path, **kwargs):
        """The train method is used to train the model and save the weights to the specified path"""
        # Optional
