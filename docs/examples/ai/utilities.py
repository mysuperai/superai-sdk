import mock
from colorama import Fore, Style


class MockedReturns:
    def __init__(self, ai_object):
        self.ai_object = ai_object
        self.s3 = mock.patch("superai.meta_ai.AI.load_from_s3", return_value=ai_object)
        self.list = mock.patch("superai.meta_ai.ai.list_models", return_value=self.list_models())
        self.local = mock.patch("superai.meta_ai.ai.LocalPredictor.predict", side_effect=self.ai_object.predict)

        self.sage_pred = mock.patch(
            "superai.apis.meta_ai.model.DeploymentApiMixin.predict_from_endpoint",
            lambda x, a, b, c: self.ai_object.predict(c),
        )
        self.push = mock.patch("superai.meta_ai.AI.push_model", return_value=True)
        self.undep = mock.patch("superai.meta_ai.AI.undeploy", return_value=True)
        self.train = mock.patch("superai.meta_ai.AI.train", return_value=True)

    @staticmethod
    def list_models():
        return [
            {
                "name": "my_instance_segmentation_model",
                "stage": "DEV",
                "version": "1",
                "description": None,
                "modelSavePath": "s3://my_instance_segmentation_model/DEV/1",
                "weightsPath": "s3://some_model_path"
                # so that we can test the local loading aspect of s3 loading
            }
        ]

    @staticmethod
    def sage_check(ret: bool):
        sage = mock.patch("superai.apis.meta_ai.model.DeploymentApiMixin.check_endpoint_is_available", return_value=ret)
        return sage


def color(x: str):
    return Fore.YELLOW + x + Style.RESET_ALL
