import superai_schema.universal_schema.data_types as dt
from superai_schema.universal_schema.data_types import validate


def get_exclusive_choice_tag(schema_instance):
    validate(instance=schema_instance, schema=dt.EXCLUSIVE_CHOICE)
    return schema_instance.get("selection", {}).get("tag")


def get_multiple_choice_tags(schema_instance):
    validate(instance=schema_instance, schema=dt.MULTIPLE_CHOICE)
    return [s.get("tag") for s in schema_instance.get("selections", {})]
