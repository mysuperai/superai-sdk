import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import jsonpickle  # type: ignore
from apm import *  # type: ignore
from pydantic import BaseModel, Field, ValidationError, root_validator, validator

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
    --- DEPRECATED ---: use `TaskPredictionInstance` directly instead.

    A prediction object which verifies the predictions obtained from the model.

    Usage should be like:
        pred = EasyPredictions(basemodel.predict(input)).value
    """

    def __init__(self, input: Optional[Union[Dict, List[Dict], RawPrediction, List[RawPrediction]]] = None):
        if isinstance(input, RawPrediction) or (isinstance(input, list) and isinstance(input[0], RawPrediction)):
            log.warning("RawPrediction is deprecated. Use TaskPredictionInstance instead.")
        else:
            TaskPredictionInstance.validate_prediction(input)
        self.value = input


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
    # Dict represents new schema, TODO: add proper validation of new schema fields
    __root__: Union[List[TaskElement], dict]

    def __iter__(self):
        return iter(self.__root__)

    def __len__(self):
        return len(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class TaskInput(TaskIO):
    pass


class TaskOutput(TaskIO):
    pass


class TaskBatchIO(BaseModel):
    __root__: List[TaskIO]

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


class TaskPredictionInstance(BaseModel):
    prediction: Union[TaskOutput, dict, str, RawPrediction]  # TODO: Deprecated dict,str usage here
    score: float = Field(..., ge=0, le=1)

    def __getitem__(self, item):
        """allows access via "[field]" to make backwards compatible with old code"""
        return getattr(self, item)

    class Config:
        arbitrary_types_allowed = True

    @validator("prediction")
    def validate_prediction_field(cls, value):
        if isinstance(value, TaskOutput):
            return value
        elif isinstance(value, (dict, str, RawPrediction)):
            log.warning(
                f"Deprecation: TaskPredictionInstance.prediction is expected to be of type `TaskOutput`, but got a {type(value)}. "
            )
            return value
        else:
            try:
                parsed = TaskOutput.parse_obj(value)
                return parsed
            except ValidationError:
                raise ValueError(
                    "TaskPredictionInstance.prediction is expected to be of type `TaskOutput` or be compatible with it."
                )

    @classmethod
    def validate_prediction(cls, prediction) -> Union[List["TaskPredictionInstance"], "TaskPredictionInstance", Any]:
        if isinstance(prediction, list):
            result = [cls.parse_obj(x) for x in prediction]
        elif isinstance(prediction, dict):
            log.warning("model_class.predict returned a dict. We expect a list of TaskPredictionInstance.")
            result = cls.parse_obj(prediction)
        elif prediction is None:
            result = cls.parse_obj(prediction)
        else:
            log.warning("model_class.predict returned a non-standard object. Expecting List[TaskPredictionInstance].")
            result = prediction
        return result

    @classmethod
    def validate_prediction_batch(cls, batch) -> List[List["TaskPredictionInstance"]]:
        # Parse TaskPredictionInstance in nested list
        # The outer list is of size(len(inputs))
        # The inner list has unknown size, since it is a list of possible prediction_instances generated by the model
        result = [[cls.parse_obj(instance) for instance in prediction] for prediction in batch]
        return result
