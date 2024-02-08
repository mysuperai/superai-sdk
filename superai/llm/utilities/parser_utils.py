import json
from typing import Dict

from superai.llm.configuration import Configuration
from superai.llm.data_types.message import ChatMessage
from superai.llm.foundation_models import ChatGPT
from superai.llm.utilities.json_utils import (
    dict_has_valid_key,
    fix_json,
    is_valid_json,
    is_valid_schema,
    json_schema_from_dict,
)
from superai.log import logger

config = Configuration()

log = logger.get_logger(__name__)


class Parser:
    def __init__(
        self,
        foundation_model=None,
        use_ai=False,
        prompt=None,
        prompt_output_format=None,
        output_schema=None,
        commands=None,
    ):
        if foundation_model is None:
            foundation_model = ChatGPT(engine=config.fast_foundation_model_engine)
        self.foundation_model = foundation_model
        self.use_ai = use_ai
        self.prompt = prompt
        self.prompt_output_format = prompt_output_format
        self.output_schema = output_schema
        self.commands = commands

        if config.debug:
            if self.use_ai:
                log.debug(f"Using foundation model {self.foundation_model} to fix json responses")
            else:
                log.debug(f"Not using foundation model to fix json responses")

    def to_dict(self, response: str):
        output_json_schema = json_schema_from_dict(self.prompt_output_format)

        is_valid, _ = is_valid_json(response)
        if config.debug:
            log.debug(f"JSON is valid? {is_valid}")
        if not is_valid:
            if config.debug:
                log.debug(f"Fixing json")
            response = fix_json(response)
            is_valid, _ = is_valid_json(response)
            if is_valid:
                return json.loads(response)
            if self.use_ai:
                if self.prompt is not None:
                    prompt = f"""I originally sent you this prompt: {self.prompt}\n\n----\n\n"""
                else:
                    prompt = ""
                prompt += f"""The response you gave did not give a valid json output. 
                This was your response: {response}
                This is the output_schema that it needs to validate against: {output_json_schema}
                Please try again to give a response that matches the output schema. Don't respond with anything else, except the output specified by the schema."""
                messages = [ChatMessage(content=prompt, role="system")]
                response = self.foundation_model.predict(messages)
                if config.debug:
                    log.debug(f"Using AI to try and create a valid output json")
                is_valid, _ = is_valid_json(response)
                if is_valid:
                    return json.loads(response)
                else:
                    raise ValueError(f"Response is not valid json: {response}")
        else:
            return json.loads(response)

    def get_command(self, response: str, max_tries: int = 3) -> Dict[str, any]:
        tries = 0
        valid_command = None
        output_json_schema = json_schema_from_dict(self.prompt_output_format)
        command_json_schema = json_schema_from_dict(self.prompt_output_format["command"])

        while tries < max_tries:
            response_dict = self.to_dict(response)

            is_valid, _ = is_valid_schema(response_dict, output_json_schema)
            if config.debug:
                log.debug(f"Response Schema is valid? {is_valid}")
            if not is_valid and self.use_ai:
                if self.prompt is not None:
                    prompt = f"""I originally sent you this prompt: {self.prompt}\n\n----\n\n"""
                else:
                    prompt = ""
                prompt += f"""The response you gave does not match the specified output schema. 
                This was your response: {response}
                This is the output_schema that it needs to validate against: {output_json_schema}
                Please try again to give a response that matches the output schema. Don't respond with anything else, except the output specified by the schema."""
                messages = [ChatMessage(content=prompt, role="system")]
                if config.debug:
                    log.debug(f"Using AI to fix schema at try {tries}")
                response = self.foundation_model.predict(messages)

            if config.debug:
                log.debug(f"'command' in response dictionary? {is_valid}")
            if not dict_has_valid_key("command", response_dict) and self.use_ai:
                if self.prompt is not None:
                    prompt = f"""I originally sent you this prompt: {self.prompt}\n\n----\n\n"""
                else:
                    prompt = ""
                prompt += f"""The response you gave does not have the key `command` in the response. 
                This was your response: {response}
                This is the output_schema that it needs to validate against: {output_json_schema}
                Please try again to give a response that has 'command' in the output dictionary. Don't respond with anything else, except the output specified by the schema."""
                messages = [ChatMessage(content=prompt, role="system")]
                if config.debug:
                    log.debug(f"Using AI to fix missing command key at try {tries}")
                response = self.foundation_model.predict(messages)

            is_valid, _ = is_valid_schema(response_dict["command"], command_json_schema)
            if config.debug:
                log.debug(f"Command schema is valid? {is_valid}")
            if not is_valid and self.use_ai:
                if self.prompt is not None:
                    prompt = f"""I originally sent you this prompt: {self.prompt}\n\n----\n\n"""
                else:
                    prompt = ""
                prompt += f"""The response you gave in does not have the appriopriate structure for command which should be: {command_json_schema}. 
                This was your response['command']: {response}
                This is the command_schema['command'] that it needs to validate against: {command_json_schema}
                Please try again to give a response that matches the output schema. Don't respond with anything else, except the output specified by the schema."""
                messages = [ChatMessage(content=prompt, role="system")]
                if config.debug:
                    log.debug(f"Using AI to fix command schema at try {tries}")
                response = self.foundation_model.predict(messages)

            is_valid, _ = is_valid_command(response_dict["command"])
            if config.debug:
                log.debug(f"Is {response_dict['command']['name']} a valid command? {is_valid}")
            if not is_valid and self.use_ai:
                if self.prompt is not None:
                    prompt = f"""I originally sent you this prompt: {self.prompt}\n\n----\n\n"""
                else:
                    prompt = ""
                prompt += f"""The command in response['command']['name'] doesn't match a name in {self.commands} you gave in does not have the appriopriate structure for command which should be: {command_json_schema}. 
                Please try again to give a response with a command which matches one of the above commands."""
                messages = [ChatMessage(content=prompt, role="system")]
                if config.debug:
                    log.debug(f"Using AI to fix command name at try {tries}")
                response = self.foundation_model.predict(messages)

            else:
                valid_command = response_dict["command"]
                if config.debug:
                    log.debug(f"{valid_command} is Valid")
                break

            tries += 1
            if config.debug:
                log.debug(f"{tries}/{max_tries} tries to parse output.")

        if valid_command is None:
            raise ValueError("Couldn't extract a valid command from the response")

        return valid_command

    def get_output(self, response: str, max_tries: int = 3, output_key=None) -> Dict[str, any]:
        tries = 0
        valid_output = None
        output_json_schema = json_schema_from_dict(self.prompt_output_format)

        while tries < max_tries:
            response_dict = self.to_dict(response)

            is_valid, _ = is_valid_schema(response_dict, output_json_schema)
            if config.debug:
                log.debug(f"Response Schema is valid? {is_valid}")
            if not is_valid and self.use_ai:
                if self.prompt is not None:
                    prompt = f"""I originally sent you this prompt: {self.prompt}\n\n----\n\n"""
                else:
                    prompt = ""
                prompt += f"""The response you gave does not match the specified output schema. 
                This was your response: {response}
                This is the output_schema that it needs to validate against: {output_json_schema}
                Please try again to give a response that matches the output schema. Don't respond with anything else, except the output specified by the schema."""
                messages = [ChatMessage(content=prompt, role="system")]
                if config.debug:
                    log.debug(f"Using AI to fix schema at try {tries}")
                response = self.foundation_model.predict(messages)

            if output_key is not None:
                if config.debug:
                    log.debug(f"'{output_key}' in response dictionary? {is_valid}")
                if not dict_has_valid_key({output_key}, response_dict) and self.use_ai:
                    if self.prompt is not None:
                        prompt = f"""I originally sent you this prompt: {self.prompt}\n\n----\n\n"""
                    else:
                        prompt = ""
                    prompt += f"""The response you gave does not have the key `output` in the response. 
                    This was your response: {response}
                    This is the output_schema that it needs to validate against: {output_json_schema}
                    Please try again to give a response that has {output_key} in the output dictionary. Don't respond with anything else, except the output specified by the schema."""
                    messages = [ChatMessage(content=prompt, role="system")]
                    if config.debug:
                        log.debug(f"Using AI to fix missing output key at try {tries}")
                    response = self.foundation_model.predict(messages)
            if output_key is not None:
                is_valid, _ = is_valid_schema(response_dict[output_key], self.output_schema)
            else:
                is_valid, _ = is_valid_schema(response_dict, self.output_schema)
            if config.debug:
                log.debug(f"output schema is valid? {is_valid}")
            if not is_valid and self.use_ai:
                if self.prompt is not None:
                    prompt = f"""I originally sent you this prompt: {self.prompt}\n\n----\n\n"""
                else:
                    prompt = ""
                prompt += f"The response you gave in does not have the appriopriate structure for output which should be: {self.output_schema}."
                if output_key is not None:
                    prompt += f"This was your response['{output_key}']: {response}"
                else:
                    prompt += f"This was your response: {response}"
                prompt += f"\nThis is the output_schema that it needs to validate against: {self.output_schema}"
                prompt += "Please try again to give a response that matches the output schema. Don't respond with anything else, except the output specified by the schema."
                messages = [ChatMessage(content=prompt, role="system")]
                if config.debug:
                    log.debug(f"Using AI to fix output schema at try {tries}")
                response = self.foundation_model.predict(messages)

            else:
                if output_key is not None:
                    valid_output = response_dict[output_key]
                else:
                    valid_output = response_dict
                if config.debug:
                    log.debug(f"{valid_output} is Valid")
                break

            tries += 1
            if config.debug:
                log.debug(f"{tries}/{max_tries} tries to parse output.")

        if valid_output is None:
            raise ValueError("Couldn't extract a valid output from the response")

        return valid_output


# Test script
if __name__ == "__main__":
    prompt = None
    response = '{"thoughts": {"text": "I need to find the real name, URL, and phone number of the business with the given name and address.", "reasoning": "I will start by searching for the name and address on Google to find the real name of the business.", "plan": "- Google search the name and address\\n- Find the real name\\n- Discover the URL of the website\\n- Find the phone number", "criticism": "None", "speak": "I will find the real name, URL, and phone number of the business with the given name and address."}, "command": {"name": "google", "args": {"input": "SUPER 1 FOODS 617 1500 N TRENTON ST RUSTON LA 71270"}}}'
    output_format = {
        "thoughts": {
            "text": "thought",
            "reasoning": "reasoning",
            "plan": "- short bulleted\n- list that conveys\n- long-term plan",
            "criticism": "constructive self-criticism",
            "speak": "thoughts summary to say to user",
        },
        "command": {"name": "command name", "args": {}},
    }

    output_parser = Parser(
        foundation_model=ChatGPT(engine=config.smart_foundation_model_engine),
        use_ai=True,
        prompt=prompt,
        prompt_output_format=output_format,
    )
    command = output_parser.get_command(response)
    print(command)
