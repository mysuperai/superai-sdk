from superai.llm.ai import LLM
from superai.llm.data_types import Any
from superai.llm.dataset import Data, Dataset
from superai.llm.logger import logger

input_schema = Any()
output_schema = Any()

llm = LLM(input_schema=input_schema, output_schema=output_schema, name="Capital Finder")

# Example 1: Creating an LLM instance and setting components
llm.set_components(
    role="Your role is to figure out the capital of a country.",
    goals=["Be accurate"],
    prompt_output_format='{"capital": "<Answer>", "certainty": "<number 0-1>"}',
    advice=["Please be concise and accurate in your responses."],
    constraints=["Do not provide false information."],
    prompt_prefix="I have a question: ",
    prompt_suffix="Please provide the answer to my question with only the format of the output.",
)

# logger.log(title="LLM Instance:", title_color="cyan", message=llm)

# # Example 2: Generating a prompt and making a single prediction
# input_data = Data(input="What is the capital of France?")
# data = llm.predict(input_data)

# logger.log(title="New Prompt Input:", title_color="cyan", message=input_data)
# logger.log(title="Prediction Output:", title_color="cyan", message=data.output)

# # Example 3: Making multiple predictions
# input_data_list = [
#     "What is the capital of the United States?",
#     "What is the capital of China?",
#     "What is the capital of Russia?",
# ]

# input_data = Dataset(input_schema=Any(), output_schema=Any()).from_list(data_list=input_data_list)

# data_results = llm.predict(input_data, parallelize=True)

# for index, data in enumerate(data_results):
#     logger.log(title=f"Input {index + 1}:", title_color="cyan", message=input_data_list[index])
#     logger.log(title=f"Output {index + 1}:", title_color="cyan", message=data.output)


# # Example 4: Adding examples, anti-examples, and context to the LLM instance
# llm.add_examples([
#     "What is the capital of France? The capital of France is Paris.",
#     "What is the capital of Germany? The capital of Germany is Berlin.",
# ])

# llm.add_anti_examples([
#     "What is the capital of France? The capital of France is Rome.",
# ])

# # TODO: uncomment this line if the context inclucing _document_to_text method is implemented
# # llm.add_context([
# #     "In this assistant, you should provide accurate information about countries and their capitals.",
# # ])

input_data = Dataset(input_schema=Any(), output_schema=Any(), data=[Data(input="What is the capital of Italy?")])
output_dataset = llm.predict(input_data)

logger.log(title="New Prompt Input with Examples and Context:", title_color="cyan", message=llm.prompt)
logger.log(title="Prediction Output with Examples and Context:", title_color="cyan", message=output_dataset)

# Example 5: Training the LLM instance
