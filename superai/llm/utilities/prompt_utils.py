from typing import Any, Dict, List


def get_current_git_branch():
    pass


def generate_command_string(command: Dict[str, Any]) -> str:
    """
    Generate a formatted string representation of a command.
    Args:
        command (dict): A dictionary containing command information.
    Returns:
        str: The formatted command string.
    """
    args_string = ", ".join(f'"{key}": "{value}"' for key, value in command["args"].items())
    return f'{command["label"]}: "{command["name"]}", args: {args_string}'


def generate_ordered_list(items: List[Any], item_type="list") -> str:
    if item_type == "command":
        return "\n".join(f"{i+1}. {generate_command_string(item)}" for i, item in enumerate(items))
    else:
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))


def generate_unordered_list(items: List[Any], item_type="list") -> str:
    if item_type == "command":
        return "\n".join(f"- {generate_command_string(item)}" for i, item in enumerate(items))
    else:
        return "\n".join(f"- {item}" for i, item in enumerate(items))


def stringify_value(val: Any) -> str:
    if isinstance(val, str):
        return val
    elif isinstance(val, dict):
        return "\n" + stringify_dict(val)
    elif isinstance(val, list):
        return "\n".join(stringify_value(v) for v in val)
    else:
        return str(val)


def stringify_dict(data: dict) -> str:
    text = ""
    for key, value in data.items():
        text += key + ": " + stringify_value(value) + "\n"
    return text
