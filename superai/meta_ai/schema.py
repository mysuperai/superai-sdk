from typing import Optional, Union, Dict, List

import jsonpickle  # type: ignore
from apm import *  # type: ignore

from superai.apis.meta_ai.meta_ai_graphql_schema import RawPrediction


class Schema:
    """Mocked class for all schema related functionalities."""

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.params = None

    def parameters(self, **kwargs) -> "SchemaParameters":
        self.params = SchemaParameters(**kwargs)
        return self.params

    @property
    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, input):
        return jsonpickle.decode(input)

    def __eq__(self, other):
        return self.to_json == other.to_json


class Image(Schema):
    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)


class SingleChoice(Schema):
    def __init__(self, **kwargs):
        super(SingleChoice, self).__init__(**kwargs)


class SchemaParameters:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, input):
        return jsonpickle.decode(input)


class EasyPredictions:
    """
    A prediction object which verifies the predictions obtained from the model.

    Usage should be like:
        pred = EasyPredictions(basemodel.predict(input)).value
    """

    def __init__(self, input: Optional[Union[Dict, List[Dict], RawPrediction, List[RawPrediction]]] = None):
        if isinstance(input, RawPrediction):
            pass
        elif isinstance(input, dict):
            assert self.verify(input)
        elif isinstance(input, list):
            input_list = input
            if len(input) == 1 and isinstance(input[0], list):
                # Sagemaker does not allow returning simple list (it checks for length of Batch)
                # in that case we wrap the model output in another list
                # this allows the verification to inspect the correct elements
                input_list = input[0]
            for a in input_list:
                if not isinstance(a, RawPrediction):
                    assert self.verify(a)
        else:
            raise ValueError(f"Unexpected type {type(input)}, needs to be a dict or list")
        self.value = input

    @staticmethod
    def verify(args):
        if args is None:
            raise AttributeError("Need to pass some input")
        result = {}
        if not match(
            args,
            {"prediction": "prediction" @ _},
        ).bind(result):
            raise AttributeError("Keys `prediction` needs to be present")
        if not match(args, {"score": "score" @ (InstanceOf(int) | InstanceOf(float)) & Between(0, 1)}).bind(result):
            raise AttributeError("Keys `score` needs to be present and between 0 and 1")
        return True
