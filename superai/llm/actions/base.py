from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Type, Union, get_args, get_origin

from pydantic import BaseModel, Extra, Field, ValidationError
from pydantic.main import ModelMetaclass


class ActionMetaclass(ModelMetaclass):
    """Metaclass for BaseAction to validate params_schema."""

    def __new__(
        cls: Type[ActionMetaclass], name: str, bases: Tuple[Type, ...], attrs: dict[str, Any]
    ) -> ActionMetaclass:
        if "params_schema" in attrs:
            schema_annotations = attrs.get("__annotations__", {})
            args_schema_type = schema_annotations.get("params_schema", None)

            # Check if the params_schema annotation is missing or wrongly set to BaseModel
            if args_schema_type is None or args_schema_type == BaseModel:

                # Get the origin and arguments of the type annotation
                annotation_origin = get_origin(args_schema_type)
                annotation_args = get_args(args_schema_type)

                # Check if the origin is of Type and if the first argument is a subclass of BaseModel
                if annotation_origin != Type or (
                    len(annotation_args) > 0 and not issubclass(annotation_args[0], BaseModel)
                ):
                    typehint_mandate = """
                    When providing an params_schema, you must add a type annotation to params_schema:
                    `params_schema: Type[<YourSchema>]` where <YourSchema> is the schema class you want to use."""
                    raise TypeError(typehint_mandate)

        return super().__new__(cls, name, bases, attrs)


class BaseAction(ABC, BaseModel, metaclass=ActionMetaclass):
    """Actions must inherit from this class."""

    name: str = Field(..., description="A unique name that explicitly communicates its purpose.")
    description: str = Field(..., description="Tell the agent why, how, and when to use this action.")
    params_schema: Optional[Type[BaseModel]] = Field(
        None, description="A pydantic BaseModel that describes the arguments for this action."
    )

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        arbitrary_types_allowed = True

    @property
    def params(self) -> dict:
        """Return the parameters for this action."""
        if self.params_schema is not None:
            output_dict = {}
            for key, value in self.params_schema.schema()["properties"].items():
                output_dict[key] = value["type"]
                if "items" in value:
                    output_dict[key] = f"{value['type']}[{value['items']['type']}]"
                if "additionalProperties" in value:
                    output_dict[key] = f"{value['type']}[{value['additionalProperties']['type']}]"
            return output_dict
        else:
            return {k: _format_type(v) for k, v in self._run.__annotations__.items()}

    @abstractmethod
    def _run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Functionality which actually executes the action"""
        raise NotImplementedError

    def run(self, input: Union[str, Dict], **kwargs: Any) -> Any:
        """Actually execute the action"""
        self._parse_input(input)
        try:
            action_args, action_kwargs = self._to_args_and_kwargs(input)
            output = self._run(*action_args, **action_kwargs)
        except (Exception, KeyboardInterrupt) as e:
            raise e
        return output

    def _to_args_and_kwargs(self, input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        if isinstance(input, str):
            return (input,), {}
        else:
            return (), input

    def _parse_input(
        self,
        input: Union[str, Dict],
    ) -> None:
        """Convert action input to pydantic model."""
        input_args = self.params_schema
        if isinstance(input, str):
            if input_args is not None:
                key_ = next(iter(input_args.__fields__.keys()))
                input_args.validate({key_: input})
        else:
            if input_args is not None:
                input_args.validate(input)
            else:
                expected_args = self.params
                for key, value in input.items():
                    if key not in expected_args:
                        raise ValidationError(f"Unexpected argument '{key}'")
                    expected_type = expected_args[key]
                    actual_type = _format_type(type(value))
                    if actual_type != expected_type:
                        raise ValidationError(
                            message=f"Argument '{key}' has incorrect type. Expected '{expected_type}', got '{actual_type}'"
                        )


def _format_type(t: Type) -> str:
    type_name_map = {"int": "integer", "str": "string"}

    origin = get_origin(t)
    if origin is None:
        return type_name_map.get(t.__name__.lower(), t.__name__.lower())
    elif origin in (list, tuple):
        return f"array[{_format_type(get_args(t)[0])}]"
    elif origin is dict:
        key_type, value_type = get_args(t)
        return f"object[{_format_type(value_type)}]"
    else:
        return type_name_map.get(t.__name__.lower(), t.__name__.lower())
