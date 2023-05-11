import contextlib
import json
import re
from typing import Dict, Optional

import jsonschema
from jsonschema import validate


def json_schema_from_dict(data, required=True):
    if isinstance(data, dict):
        schema = {"type": "object", "properties": {}}
        if required:
            schema["required"] = list(data.keys())

        for key, value in data.items():
            schema["properties"][key] = json_schema_from_dict(value, required)
        return schema
    elif isinstance(data, list):
        if len(data) > 0:
            return {"type": "array", "items": json_schema_from_dict(data[0], required)}
        else:
            return {"type": "array", "items": {}}
    else:
        if isinstance(data, str):
            return {"type": "string"}
        elif isinstance(data, int):
            return {"type": "integer"}
        elif isinstance(data, float):
            return {"type": "number"}
        elif isinstance(data, bool):
            return {"type": "boolean"}
        else:
            return {}


def is_valid_json(data: Dict[str, any]) -> bool:
    try:
        if isinstance(data, str):
            json.loads(data)
        else:
            pass
        return True, None
    except json.JSONDecodeError as e:
        return False, e


def is_valid_schema(data: Dict[str, any], schema: Dict[str, any]) -> bool:
    try:
        validate(instance=data, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, e


def dict_has_valid_key(key: str, my_dict: Dict[str, any]) -> bool:
    try:
        if key in my_dict:
            return True, None
        else:
            return False, None
    except TypeError as e:
        print(f"Error: {e}")
        return False, e


def extract_char_position(error_message: str) -> int:
    char_pattern = re.compile(r"\(char (\d+)\)")
    if match := char_pattern.search(error_message):
        return int(match[1])
    else:
        raise ValueError("Character position not found in the error message.")


def fix_trailing_comma(json_string: str) -> str:
    trailing_comma_pattern = re.compile(r",\s*([}\]])")
    corrected_json_string = trailing_comma_pattern.sub(r"\1", json_string)
    return corrected_json_string


def add_missing_comma(json_string: str) -> str:
    missing_comma_pattern = re.compile(r"([}\]])\s*([{\[])")
    corrected_json_string = missing_comma_pattern.sub(r"\1,\2", json_string)
    return corrected_json_string


def fix_single_quotes(json_string: str) -> str:
    single_quotes_pattern = re.compile(r"(')(?:(?=(\\?))\2.)*?\1")
    corrected_json_string = single_quotes_pattern.sub(lambda x: x.group(0).replace("'", '"'), json_string)
    return corrected_json_string


def balance_square_brackets(json_string: str) -> str:
    open_brackets_count = json_string.count("[")
    close_brackets_count = json_string.count("]")

    while open_brackets_count > close_brackets_count:
        json_string += "]"
        close_brackets_count += 1

    while close_brackets_count > open_brackets_count:
        json_string = json_string.rstrip("]")
        close_brackets_count -= 1

    return json_string


def replace_invalid_characters(json_string: str) -> str:
    invalid_chars_pattern = re.compile(r"[\x00-\x1F\x7F-\x9F]")
    corrected_json_string = invalid_chars_pattern.sub("", json_string)
    return corrected_json_string


def replace_control_characters(json_string: str) -> str:
    control_chars_pattern = re.compile(r"\\[bfnrtv]")
    corrected_json_string = control_chars_pattern.sub("", json_string)
    return corrected_json_string


def fix_unquoted_strings(json_string: str) -> str:
    unquoted_string_pattern = re.compile(r":\s*([a-zA-Z_]+)(?=[,\]}])")
    corrected_json_string = unquoted_string_pattern.sub(r':"\1"', json_string)
    return corrected_json_string


def fix_invalid_escape(json_string: str, error_message: str) -> str:
    while error_message.startswith("Invalid \\escape"):
        bad_escape_location = extract_char_position(error_message)
        json_string = json_string[:bad_escape_location] + json_string[bad_escape_location + 1 :]
    return json_string


def balance_braces(json_string: str) -> Optional[str]:
    open_braces_count = json_string.count("{")
    close_braces_count = json_string.count("}")

    while open_braces_count > close_braces_count:
        json_string += "}"
        close_braces_count += 1

    while close_braces_count > open_braces_count:
        json_string = json_string.rstrip("}")
        close_braces_count -= 1

    with contextlib.suppress(json.JSONDecodeError):
        json.loads(json_string)
        return json_string


def add_quotes_to_property_names(json_string: str) -> str:
    def replace_func(match: re.Match) -> str:
        return f'"{match[1]}":'

    property_name_pattern = re.compile(r"(\w+):")
    corrected_json_string = property_name_pattern.sub(replace_func, json_string)
    return corrected_json_string


def fix_double_quotes_inside_values(json_string: str) -> str:
    def replace_func(match: re.Match) -> str:
        return match.group(0).replace('"', '\\"')

    double_quotes_pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
    corrected_json_string = double_quotes_pattern.sub(replace_func, json_string)

    return corrected_json_string


def fix_missing_closing_quotes(json_string: str) -> str:
    missing_closing_quotes_pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)(?=[,\]}\s])')
    corrected_json_string = missing_closing_quotes_pattern.sub(r'\1"', json_string)

    return corrected_json_string


def fix_missing_opening_quotes(json_string: str) -> str:
    missing_opening_quotes_pattern = re.compile(r'(?<=[\[{,\s])([^"\s]+)(?=")')
    corrected_json_string = missing_opening_quotes_pattern.sub(r'"\1', json_string)

    return corrected_json_string


def remove_comments(json_string: str) -> str:
    single_line_comment_pattern = re.compile(r"//.*?$")
    multi_line_comment_pattern = re.compile(r"/\*.*?\*/", re.DOTALL)
    corrected_json_string = single_line_comment_pattern.sub("", json_string)
    corrected_json_string = multi_line_comment_pattern.sub("", corrected_json_string)

    return corrected_json_string


def fix_boolean_values_in_quotes(json_string: str) -> str:
    boolean_in_quotes_pattern = re.compile(r'"(true|false)"')
    corrected_json_string = boolean_in_quotes_pattern.sub(r"\1", json_string)

    return corrected_json_string


def fix_number_values_in_quotes(json_string: str) -> str:
    number_in_quotes_pattern = re.compile(r'"(-?\d+(\.\d+)?([eE][+-]?\d+)*)"')
    corrected_json_string = number_in_quotes_pattern.sub(r"\1", json_string)

    return corrected_json_string


def fix_null_values_in_quotes(json_string: str) -> str:
    null_in_quotes_pattern = re.compile(r'"null"')
    corrected_json_string = null_in_quotes_pattern.sub(r"null", json_string)

    return corrected_json_string


def fix_extra_commas(json_string: str) -> str:
    extra_commas_pattern = re.compile(r",(,)+\s*(?=[\]})])")
    corrected_json_string = extra_commas_pattern.sub(",", json_string)

    return corrected_json_string


def remove_invalid_string_values(json_string: str) -> str:
    invalid_string_values_pattern = re.compile(r'"[^"]*\0[^"]*"')
    corrected_json_string = invalid_string_values_pattern.sub('""', json_string)

    return corrected_json_string


def fix_invalid_unicode_characters(json_string: str) -> str:
    invalid_unicode_pattern = re.compile(r"\\u([0-9a-fA-F]{1,3})")
    corrected_json_string = invalid_unicode_pattern.sub(lambda m: "\\u0" + m.group(1), json_string)

    return corrected_json_string


def fix_json(json_string: str) -> str:
    fixing_methods = [
        fix_trailing_comma,
        add_missing_comma,
        fix_single_quotes,
        balance_square_brackets,
        replace_invalid_characters,
        replace_control_characters,
        fix_unquoted_strings,
        fix_double_quotes_inside_values,
        fix_missing_closing_quotes,
        fix_missing_opening_quotes,
        remove_comments,
        fix_boolean_values_in_quotes,
        fix_number_values_in_quotes,
        fix_null_values_in_quotes,
        fix_extra_commas,
        remove_invalid_string_values,
        fix_invalid_unicode_characters,
    ]

    is_valid, error = is_valid_json(json_string)

    if not is_valid:
        for method in fixing_methods:
            fixed_json_string = method(json_string)

            is_valid, error = is_valid_json(fixed_json_string)

            if is_valid:
                return fixed_json_string

            json_string = fixed_json_string

    return json_string
