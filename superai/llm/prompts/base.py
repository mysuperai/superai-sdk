from abc import ABC
from typing import Dict, List, Union

from pydantic import BaseModel, Extra

from superai.llm.configuration import Configuration
from superai.llm.data_types.message import ChatMessage
from superai.llm.utilities import generate_ordered_list, generate_unordered_list

# TODO: add prompt template functionality
# TODO: add validation for prompt fields
# TODO: add from_examples, from_metaprompt, generate_similar, to/from json
# TODO: add deploy and load to/from hub

config = Configuration()


class PromptExample(BaseModel):
    """Example to add to LLM prompt"""

    input: str
    output: str


class Prompt(BaseModel, ABC):
    prompt: str = None

    name: str = None
    role: str = None
    advice: List[str] = []
    goals: List[str] = []
    constraints: List[str] = []
    prompt_prefix: str = None
    prompt_suffix: str = None
    examples: List[Union[str, PromptExample]] = []
    anti_examples: List[Union[str, PromptExample]] = []
    context: List[str] = []
    input: str = None
    output: str = None
    output_format: str = None
    output_constraints: str = None
    memories: List[str] = []

    actions: List[str] = []
    user_feedback: List[str] = []
    performance_evaluations: List[str] = []

    max_send_tokens: int = None
    ai_role: str = None

    template: str = None
    template_variables: List[str] = []

    metadata: Dict = {}

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    def set_input(self, input: str):
        self.input = input
        self.prompt = self.construct_prompt()

    def set_output(self, output: str):
        self.output = output
        self.prompt = self.construct_prompt()

    def construct_prompt(self):
        prompt = ""

        # prefix prompt
        if self.prompt_prefix:
            prompt += f"{self.prompt_prefix}"

        # main instructions
        if self.name:
            if self.prompt_prefix:
                prompt += "\n\n"
            prompt += f"You are {self.name}"
            if self.role:
                prompt += f", {self.role}"
        else:
            if self.role:
                if self.prompt_prefix:
                    prompt += "\n\n"
                prompt += f"Your role is {self.role}."

        if self.goals:
            prompt += f"\n\nGoals:\n{generate_ordered_list(self.goals)}"

        if self.advice:
            prompt += f"\n\nAdvice:\n{generate_ordered_list(self.advice)}"

        if self.constraints:
            prompt += f"\n\nConstraints:\n{generate_ordered_list(self.constraints)}"

        # add actions prompt
        if self.actions:
            prompt += "\n\nActions:\n"
            actions_prompt_list = []
            for action in self.actions:
                params = {key: value for key, value in action.params.items() if key != "return"}
                actions_prompt_list.append(f'"{action.name}" (params={params}): {action.description}')
            # add finish state
            actions_prompt_list.append(
                f"'Finish task' (params={{}}): Useful for when you think you have generated the desired output and have acheived all goals and constraints."
            )
            prompt += generate_ordered_list(actions_prompt_list)

        # add context from vector store
        if self.context:
            prompt += f"\n\nContext:\n{generate_ordered_list(self.context)}"

        # add input output examples
        if self.examples:
            examples_string = "\n\nExamples:"
            for i, example in enumerate(self.examples):
                if isinstance(example, str):
                    examples_string += f"\n\n Example {i+1}:\n{example}"
                elif isinstance(example, PromptExample):
                    examples_string += f"\n\n Example input {i+1}:\n{example.input}"
                    examples_string += f"\n\n Example output {i+1}:\n{example.output}"
                examples_string += "\n\n###"
            prompt += examples_string

        # add master goal
        prompt += f"\n\nMaster Goal:\nYour overall goal is to "
        if self.input:
            prompt += f"take as input: '{self.input}' and complete what is outlined above and below."
        else:
            prompt += f"complete what is outlined above and below."

        if self.output_constraints:
            prompt += f"""\nOutput Constraints:\nThe outputs should satisfy the following constraints:\n{self.output_constraints}"""

        if self.output_format:
            prompt += f"""\nYou should only respond with a JSON output of the form:\n{self.output_format}\nEnsure the response can be parsed by Python json.loads."""

        if self.output:
            prompt += f"\n\nCurrent Output: This is the output you have so far:\n{self.output}"
            prompt += f"\nComplete your task once the output is complete."

        # add current performance
        if self.performance_evaluations:
            prompt += f"\n\nCurrent Performance:\n{generate_ordered_list(self.performance_evaluations)}"

        # add relevant memories
        if self.memories:
            prompt += f"\n\n:This reminds you of these events from your past:\n{generate_unordered_list(self.memories)}"

        # add user feedback
        if self.user_feedback:
            prompt += f"\n\nAct on the following user feedback:\n{generate_ordered_list(self.user_feedback)}"

        # add suffix
        if self.prompt_suffix:
            prompt += f"\n\n{self.prompt_suffix}"

        self.prompt = prompt
        return self.prompt

    def add_context(self, file, file_type):
        if file_type == "document":
            text = self._document_to_text(file, file_type)
        elif file_type == "image":
            text = self._image_to_text(file)
        elif file_type == "audio":
            text = self._audio_to_text(file)
        elif file_type == "webpage":
            text = self._webpage_to_text(file)
        else:
            raise ValueError("Invalid file type. Supported file types: document, image, audio, webpage.")
        self.context.append(text)

    def _document_to_text(self, file, file_type):
        raise NotImplementedError

    def _image_to_text(self, file):
        raise NotImplementedError

    def _audio_to_text(self, file):
        raise NotImplementedError

    def _webpage_to_text(self, file):
        raise NotImplementedError

    @classmethod
    def from_components(
        cls,
        name=None,
        role=None,
        advice=[],
        goals=[],
        constraints=[],
        prompt_prefix=None,
        prompt_suffix=None,
        examples=[],
        anti_examples=[],
        context=[],
        input=None,
        output=None,
        output_format=None,
        output_constraints=None,
        actions=[],
        user_feedback=[],
        performance_evaluations=[],
        max_send_tokens=None,
        template=None,
        template_variables=[],
        metadata={},
        memories=[],
    ):
        cls = cls()
        cls.name = name or cls.name
        cls.role = role or cls.role
        cls.advice = advice or cls.advice
        cls.goals = goals or cls.goals
        cls.constraints = constraints or cls.constraints
        cls.prompt_prefix = prompt_prefix or cls.prompt_prefix
        cls.prompt_suffix = prompt_suffix or cls.prompt_suffix
        cls.examples = examples or cls.examples
        cls.anti_examples = anti_examples or cls.anti_examples
        cls.context = context or cls.context
        cls.input = input or cls.input
        cls.output = output or cls.output
        cls.output_format = output_format or cls.output_format
        cls.output_constraints = output_constraints or cls.output_constraints
        cls.actions = actions or cls.actions
        cls.user_feedback = user_feedback or cls.user_feedback
        cls.performance_evaluations = performance_evaluations or cls.performance_evaluations
        cls.max_send_tokens = max_send_tokens or cls.max_send_tokens
        cls.template = template or cls.template
        cls.template_variables = template_variables or cls.template_variables
        cls.metadata = metadata or cls.metadata
        cls.memories = memories or cls.memories
        cls.prompt = cls.construct_prompt()
        return cls

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, "r") as f:
            generated_prompt = f.read()
        instance = cls(prompt=generated_prompt)
        instance.prompt = instance.construct_prompt()
        return instance

    def to_file(self, filepath):
        with open(filepath, "w") as f:
            f.write(self.prompt)

    @classmethod
    def from_template(cls, template: str, template_format="f-string", validate_template=True, **kwargs):
        raise NotImplementedError

    def to_template(self, template_format="f-string"):
        raise NotImplementedError

    @classmethod
    def from_string(cls, string):
        return cls(prompt=string)

    def to_string(self):
        return self.prompt

    def to_message(self, role=None):
        if not role:
            if self.ai_role:
                role = self.ai_role
            else:
                role = "system"

        return ChatMessage(content=self.prompt, role=role)

    @classmethod
    def from_message(cls, message: ChatMessage):
        return cls(prompt=message.content)

    def deploy(self):
        raise NotImplementedError

    def __str__(self):
        return f"Prompt(prompt={self.prompt})"

    def __repr__(self):
        return self.__str__()
