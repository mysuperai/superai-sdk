import enum
from abc import ABCMeta
from typing import TypeVar

from polyaxon import tracking

from superai.log import logger

log = logger.get_logger(__name__)


class AvailableCallbacks(str, enum.Enum):
    Keras = "Keras"
    Tf = "Tf"
    HuggingFace = "HuggingFace"
    PytorchLightning = "PytorchLightning"


class DefaultCallback(metaclass=ABCMeta):

    Type = TypeVar("Type", bound="DefaultCallback")

    callback = None

    def get_callback(self):
        assert self.callback is not None, "Callback not initialized correctly"
        return self.callback


class KerasCallback(DefaultCallback):
    def __init__(self, **kwargs):
        from polyaxon.tracking.contrib.keras import PolyaxonKerasCallback

        self.callback = PolyaxonKerasCallback(run=tracking.TRACKING_RUN, **kwargs)


class TfCallback(DefaultCallback):
    def __init__(self, **kwargs):
        from polyaxon.tracking.contrib.tensorflow import (
            PolyaxonCallback as PolyaxonTfCallback,
        )

        self.callback = PolyaxonTfCallback(run=tracking.TRACKING_RUN, **kwargs)


class HuggingFaceCallback(DefaultCallback):
    def __init__(self, **kwargs):
        from polyaxon.tracking.contrib.hugging_face import (
            PolyaxonCallback as PolyaxonHuggingFaceCallback,
        )

        self.callback = PolyaxonHuggingFaceCallback(run=tracking.TRACKING_RUN)


class PytorchLightningCallback(DefaultCallback):
    def __init__(self, **kwargs):
        from polyaxon.tracking.contrib.pytorch_lightning import (
            PolyaxonCallback as PolyaxonPytorchLightningCallback,
        )

        self.callback = PolyaxonPytorchLightningCallback()


class DefaultCallbackFactory(object):
    __callback_classes = {
        "Keras": KerasCallback,
        "Tf": TfCallback,
        "HuggingFace": HuggingFaceCallback,
        "PytorchLightning": PytorchLightningCallback,
    }

    @staticmethod
    def get_default_callback(fw: AvailableCallbacks, **kwargs):
        default_callback_class = DefaultCallbackFactory.__callback_classes.get(fw)

        if default_callback_class:
            obj = default_callback_class(**kwargs)
            log.info(f"Getting logger for {fw.value}")
            return obj.get_callback()
        raise NotImplementedError(f"The default callback for framework {fw} is not implemented yet.")


def get_tensorboard_tracking_path():
    # tracking path helpers
    superai_tensorboard_path = tracking.get_tensorboard_path()
    return superai_tensorboard_path
