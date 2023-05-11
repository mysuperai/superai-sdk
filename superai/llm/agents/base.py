from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional

from superai.llm.configuration import Configuration
from superai.llm.data_types import DataType
from superai.llm.data_types.message import Message
from superai.llm.foundation_models import ChatGPT, FoundationModel
from superai.llm.logger import logger
from superai.llm.memory import LocalMemory, Memory

config = Configuration()


class Agent(ABC):

    input_schema: DataType
    output_schema: DataType
    name: str
    foundation_model: FoundationModel = ChatGPT(engine=config.smart_foundation_model_engine)
    database: Memory = LocalMemory(memory_name=config.memory_index, overwrite=True)

    message_history: Optional[List[Message]] = []

    prompt: Optional[str] = None

    role: Optional[str] = None
    advice: Optional[List[str]] = []
    goals: Optional[List[str]] = []
    constraints: Optional[List[str]] = []
    prompt_prefix: Optional[str] = None
    prompt_suffix: Optional[str] = None
    examples: Optional[List[str]] = []
    anti_examples: Optional[List[str]] = []
    context: Optional[List[str]] = []
    input: Optional[str] = None
    output: Optional[str] = None
    output_format: Optional[str] = None
    memories: Optional[List[str]] = []

    actions: Optional[List[str]] = []
    user_feedback: Optional[List[str]] = []
    performance_evaluations: Optional[List[str]] = []

    preprocessing_function: Optional[Callable] = None
    postprocessing_function: Optional[Callable] = None

    max_send_tokens: Optional[int] = None
    ai_role: Optional[str] = None

    template: Optional[str] = None
    template_variables: Optional[List[str]] = []

    metadata: Optional[Dict] = {}

    @abstractmethod
    def run(self, input):
        raise NotImplementedError

    @abstractmethod
    def generate_prompt(self):
        raise NotImplementedError

    def get_relevant_memories(self, data=None, n=9):
        if data is None:
            data = self.message_history[-n:]
        if not isinstance(data, list):
            data = "\n".join(data)
        if not isinstance(data, str):
            data = str(data)
        relevant_memories = self.database.get_relevant(text=data, n=n)
        if config.debug:
            logger.debug(f"relevant memories: {relevant_memories}")
            logger.debug(f"memory stats: {self.database.get_stats()}")
        return relevant_memories

    def set_role(self, role):
        self.role = role

    def add_goal(self, goal):
        # TODO: add structured goals such as Accuracy() > .2
        if isinstance(goal, str):
            self.goals.append(goal)
        else:
            raise ValueError("goal must be a string")

    def add_goals(self, goals):
        if isinstance(goals, list):
            for c in goals:
                self.add_goal(c)
        else:
            raise ValueError("constraints must be a list of strings")

    def add_advice(self, advice):
        if isinstance(advice, list):
            self.advice.extend(advice)
        elif isinstance(advice, str):
            self.advice.append(advice)
        else:
            raise ValueError("advice must be a list of strings or a string")

    def add_constraint(self, constraint):
        # TODO: add structured constraints such as Accuracy() > .2
        if isinstance(constraint, str):
            self.constraints.append(constraint)
        else:
            raise ValueError("constraint must be a string")

    def add_constraints(self, constraints):
        if isinstance(constraints, list):
            for c in constraints:
                self.add_constraint(c)
        else:
            raise ValueError("constraints must be a list of strings")

    def add_command(self, command_label: str, command_name: str, args=None) -> None:
        """
        Add a command to the commands list with a label, name, and optional arguments.
        Args:
            command_label (str): The label of the command.
            command_name (str): The name of the command.
            args (dict, optional): A dictionary containing argument names and their
              values. Defaults to None.
        """
        if args is None:
            args = {}

        command_args = {arg_key: arg_value for arg_key, arg_value in args.items()}

        command = {
            "label": command_label,
            "name": command_name,
            "args": command_args,
        }

        self.commands.append(command)

    def add_commands(self, commands):
        if isinstance(commands, list):
            for t in commands:
                self.add_command(command_label=t[0], command_name=t[1], args=t[2])
        else:
            raise ValueError("commands must be a list of dictionaries")

    def add_evaluation(self, evaluation):
        if isinstance(evaluation, str):
            self.evaluations.append(evaluation)
        else:
            raise ValueError("evaluation must be a string")

    def add_evaluations(self, evaluations):
        if isinstance(evaluations, list):
            for e in evaluations:
                self.add_evaluation(e)
        else:
            raise ValueError("evaluations must be a list of strings")

    def add_context(self, context):
        # TODO: read in data from a file, url or path
        if isinstance(context, list):
            self.context.extend(context)
        elif isinstance(context, str):
            self.context.append(context)
        else:
            raise ValueError("context must be a list of strings or a string")

    def add_memory(self, memory):
        if isinstance(memory, str):
            self.memories.append(memory)
        else:
            raise ValueError("memory must be a string")

    def add_memories(self, memories):
        if isinstance(memories, list):
            for m in memories:
                self.add_memory(m)
        else:
            raise ValueError("memories must be a list of strings")

    def add_example(self, example):
        if isinstance(example, str):
            self.examples.append(example)
        else:
            raise ValueError("example must be a string")

    def add_examples(self, examples):
        if isinstance(examples, list):
            for e in examples:
                self.add_example(e)
        else:
            raise ValueError("examples must be a list of strings")

    def set_prompt_start(self, prompt_start):
        if isinstance(prompt_start, str):
            self.prompt_start = prompt_start
        else:
            raise ValueError("prompt_start must be a string")

    def add_input(self, input):
        if isinstance(input, str):
            self.input = input
        else:
            raise ValueError("input must be a string")

    def add_inputs(self, inputs):
        if isinstance(inputs, list):
            for i in inputs:
                self.add_input(i)
        else:
            raise ValueError("inputs must be a list of strings")
