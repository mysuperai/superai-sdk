import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import jsonpickle  # type: ignore
from apm import *  # type: ignore
from pydantic import BaseModel, root_validator, validator

from superai.apis.meta_ai.meta_ai_graphql_schema import RawPrediction
from superai.log import logger

log = logger.get_logger(__name__)


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
            log.info(f"Received input : {input}")
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
            log.info(f"Received input : {args}")
            raise AttributeError("Keys `prediction` needs to be present")
        if not match(args, {"score": "score" @ (InstanceOf(int) | InstanceOf(float)) & Between(0, 1)}).bind(result):
            log.info(f"Received input : {args}")
            raise AttributeError("Keys `score` needs to be present and between 0 and 1")
        return True


class LogMetric(BaseModel):
    step: int
    timestamp: datetime.datetime
    name: str
    value: Any

    class Config:
        validate_assignment = True
        validate_all = True


class ManyMetric(BaseModel):
    step: int
    timestamp: datetime.datetime
    metrics: List[Tuple[str, Any]]

    @validator("metrics")
    def check_metrics(cls, v: List[Tuple[str, Any]]) -> List[Tuple[str, Any]]:
        assert len(v), "Should not be an empty list"
        assert dict(v), "Should be convertible to a dictionary"
        keys = [x[0] for x in v]
        assert sorted(list(set(keys))) == sorted(
            keys
        ), "None of the metrics should be duplicated, i.e. check if a metric exists twice."
        return v

    class Config:
        validate_assignment = True
        validate_all = True


class TrainerOutput(BaseModel):
    metric: Optional[Dict[str, Any]] = None
    metrics: Optional[List[LogMetric]] = None
    collection: Optional[List[ManyMetric]] = None

    @root_validator()
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        conditions = [
            values.get("metric") is None,
            values.get("metrics") is None,
            values.get("collection") is None,
        ]
        if conditions.count(True) == 3:
            raise ValueError("One of `metric`, `metrics`or `collection` should be present")
        if conditions.count(False) > 1:
            raise ValueError("Only one of `metric`, `metrics`or `collection`should be present, more than one provided")
        if values.get("metrics") is not None and not values.get("metrics", []):
            raise ValueError("`metrics` should not be an empty list")
        if values.get("collection") is not None and not values.get("collection", []):
            raise ValueError("`collection` should not be an empty list")

        return values

    class Config:
        validate_assignment = True
        validate_all = True


class TaskElement(BaseModel):
    type: str
    schema_instance: Any

    def __getitem__(self, item):
        """allows access via "[field]" to make backwards compatible with old code"""
        return getattr(self, item)


class TaskIO(BaseModel):
    __root__: List[TaskElement]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)


class TaskInput(TaskIO):
    pass


class TaskOutput(TaskIO):
    pass


class TaskBatchIO(BaseModel):
    __root__: List[TaskInput]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class TaskBatchInput(TaskBatchIO):
    pass


class TaskBatchOutput(TaskBatchIO):
    pass
