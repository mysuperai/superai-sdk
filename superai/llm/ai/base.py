import concurrent.futures
from typing import Callable, Dict, List, Optional, Union

from pydantic import BaseModel
from tqdm import tqdm

from superai.llm.configuration import Configuration
from superai.llm.data_types import ChatMessage, DataType
from superai.llm.dataset import Data, Dataset
from superai.llm.foundation_models import ChatGPT, FoundationModel
from superai.llm.prompts import Prompt
from superai.llm.prompts.base import PromptExample
from superai.llm.utilities.parser_utils import Parser

config = Configuration()

# TODO: validate inputs
# TODO: add from_examples, from_metaprompt, generate_similar, to/from json


class LLM(BaseModel):
    input_schema: DataType
    output_schema: DataType
    foundation_model: FoundationModel = ChatGPT(engine=config.smart_foundation_model_engine)
    name: str = None

    prompt: Optional[Prompt] = None
    prompt_history: Optional[List[Prompt]] = []

    role: Optional[str] = None
    advice: Optional[List[str]] = []
    goals: Optional[List[str]] = []
    constraints: Optional[List[str]] = []
    prompt_prefix: Optional[str] = None
    prompt_suffix: Optional[str] = None
    examples: Optional[List[Union[str, PromptExample]]] = []
    anti_examples: Optional[List[str]] = []
    context: Optional[List[str]] = []
    input: Optional[str] = None
    output: Optional[str] = None
    prompt_output_format: Optional[str] = None
    prompt_output_constraints: Optional[str] = None
    prompt_preprocessing_function: Optional[Callable] = None
    prompt_postprocessing_function: Optional[Callable] = None

    max_send_tokens: Optional[int] = None

    metadata: Optional[Dict] = {}

    def train(self):
        pass

    def deploy(self):
        pass

    def fine_tune(self, data):
        pass

    def predict(self, input, parallelize=True):
        if isinstance(input, list):
            if not all([isinstance(data, Data) for data in input]):
                raise ValueError("Input must be a list of Data objects.")
            return self._process_multiple([data.input for data in input], parallelize)
        if isinstance(input, Data):
            return self._process_single(input.input)
        elif isinstance(input, Dataset):
            return self._process_multiple([data.input for data in input.data], parallelize)
        else:
            return self._process_single(input)

    def _process_single(self, input):
        self.input = input
        if self.prompt_preprocessing_function is not None:
            input = self.prompt_preprocessing_function(input)
            self.preprocessed_input = input
        if self.input_schema.validate_value(value=input):
            if self.prompt is not None:
                self.prompt.set_input(input=input)
                retries = 3
                for _ in range(retries):
                    # try:
                    _ = self.generate_prompt()
                    response = self.foundation_model.predict(
                        ChatMessage(content=self.prompt.to_string(), role="system")
                    )
                    # parse ai response
                    output_parser = Parser(
                        use_ai=False,
                        prompt=self.prompt.to_string(),
                        prompt_output_format=self.prompt_output_format,
                        output_schema=self.output_schema.dict(),
                    )
                    output = output_parser.get_output(response)
                    # valid_response = output_parser.to_dict(response)
                    # parse output from response
                    self.output_schema.validate_value(value=output)
                    self.output = output
                    if self.prompt_postprocessing_function is not None:
                        self.postprocessed_output = self.prompt_postprocessing_function(self.output)
                        output = self.postprocessed_output
                    return Data(input=input, output=output)

                # except Exception as e:
                #     logger.error(f"{e}")
                raise ValueError(f"Failed to generate valid output after {retries} retries.")
            else:
                raise ValueError("No prompt provided.")
        else:
            raise ValueError("Invalid input data.")

    def _process_multiple(self, input_data_list, parallelize):
        if parallelize:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self._process_single, input_data) for input_data in input_data_list]
                results = [None] * len(input_data_list)
                for future in tqdm(
                    concurrent.futures.as_completed(futures), total=len(futures), desc="Processing input data points"
                ):
                    try:
                        result = future.result()
                        index = futures.index(future)
                        results[index] = result
                    except Exception as e:
                        print(f"Error: {e}")
        else:
            results = []
            for input_data in tqdm(input_data_list, desc="Processing input data points"):
                try:
                    result = self._process_single(input_data)
                    results.append(result)
                except Exception as e:
                    print(f"Error: {e}")

        return Dataset(input_schema=self.input_schema, output_schema=self.output_schema, data=results)

    def set_components(
        self,
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
        prompt_output_format=None,
        prompt_output_constraints=None,
        prompt_preprocessing_function=None,
        prompt_postprocessing_function=None,
        max_send_tokens=None,
        metadata={},
    ):
        self.name = name or self.name
        self.role = role or self.role
        self.advice = advice or self.advice
        self.goals = goals or self.goals
        self.constraints = constraints or self.constraints
        self.prompt_prefix = prompt_prefix or self.prompt_prefix
        self.prompt_suffix = prompt_suffix or self.prompt_suffix
        self.examples = examples or self.examples
        self.anti_examples = anti_examples or self.anti_examples
        self.context = context or self.context
        self.input = input or self.input
        self.output = output or self.output
        self.prompt_output_format = prompt_output_format or self.prompt_output_format
        self.prompt_output_constraints = prompt_output_constraints or self.prompt_output_constraints
        self.prompt_preprocessing_function = prompt_preprocessing_function or self.prompt_preprocessing_function
        self.prompt_postprocessing_function = prompt_postprocessing_function or self.prompt_postprocessing_function
        self.max_send_tokens = max_send_tokens or self.max_send_tokens
        self.metadata = metadata or self.metadata
        self.prompt = Prompt.from_components(
            prompt_prefix=self.prompt_prefix,
            prompt_suffix=self.prompt_suffix,
            name=self.name,
            goals=self.goals,
            examples=self.examples,
            anti_examples=self.anti_examples,
            context=self.context,
            input=self.input,
            output=self.output,
            output_format=self.prompt_output_format,
            output_constraints=self.prompt_output_constraints,
            max_send_tokens=self.max_send_tokens,
            metadata=self.metadata,
            advice=self.advice,
            constraints=self.constraints,
        )

    def generate_prompt(self):
        self.prompt = Prompt.from_components(
            name=self.name,
            role=self.role,
            advice=self.advice,
            goals=self.goals,
            constraints=self.constraints,
            prompt_prefix=self.prompt_prefix,
            prompt_suffix=self.prompt_suffix,
            examples=self.examples,
            anti_examples=self.anti_examples,
            context=self.context,
            input=self.input,
            output_format=self.prompt_output_format,
            output_constraints=self.prompt_output_constraints,
            max_send_tokens=self.max_send_tokens,
            metadata=self.metadata,
        )
        return self.prompt

    def set_metadata(self, metadata):
        self.metadata.update(metadata)

    def set_max_send_tokens(self, max_send_tokens):
        self.max_send_tokens = max_send_tokens

    def set_prompt_preprocessing_function(self, prompt_preprocessing_function):
        self.prompt_preprocessing_function = prompt_preprocessing_function

    def set_prompt_postprocessing_function(self, prompt_postprocessing_function):
        self.prompt_postprocessing_function = prompt_postprocessing_function

    def set_prompt_output_format(self, prompt_output_format):
        self.prompt_output_format = prompt_output_format

    def set_prompt_output_constraints(self, prompt_output_constraints):
        self.prompt_output_constraints = prompt_output_constraints

    def set_output(self, output):
        self.output = output

    def set_name(self, name):
        self.name = name

    def set_role(self, role):
        self.role = role

    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_prompt_prefix(self, prompt_prefix):
        self.prompt_prefix = prompt_prefix

    def set_prompt_suffix(self, prompt_suffix):
        self.prompt_suffix = prompt_suffix

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

    def add_example(self, example: Union[str, PromptExample]):
        if isinstance(example, str):
            self.examples.append(example)
        else:
            raise ValueError("example must be a string or PromptExample")

    def add_examples(self, examples: List[Union[str, PromptExample]]):
        if isinstance(examples, list):
            for e in examples:
                self.add_example(e)
        else:
            raise ValueError("examples must be a list of strings or PromptExample")

    def add_anti_example(self, anti_example):
        if isinstance(anti_example, str):
            self.anti_examples.append(anti_example)
        else:
            raise ValueError("anti_example must be a string")

    def add_anti_examples(self, anti_examples):
        if isinstance(anti_examples, list):
            for a in anti_examples:
                self.add_anti_example(a)
        else:
            raise ValueError("anti_examples must be a list of strings")

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

    def __str__(self):
        return f"LLM(input_schema={self.input_schema}, output_schema={self.output_schema}, prompt={self.prompt}, foundation_model={self.foundation_model})"

    def __repr__(self):
        return self.__str__()
