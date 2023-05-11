from superai.llm.agents import Agent
from superai.llm.configuration import Configuration
from superai.llm.data_types import DataType
from superai.llm.dataset import Dataset
from superai.llm.evaluate import Evaluator
from superai.llm.memory import LocalMemory

config = Configuration()

input_format = {
    "name": "SUPER 1 FOODS 617",
    "address": "1500 N TRENTON ST RUSTON LA 71270",
}
output_format = {
    "name": "SUPER 1 FOODS",
    "address": "1500 N TRENTON ST RUSTON LA 71270",
    "corporate_name": "Brookshire Grocery Company",
    "corporate_address": "1250 N Hwy, Colville, Washington, 99114",
    "phone": "(318) 254-1445",
    "url": "https://www.super1foods.com/",
}

my_agent = Agent(
    input_schema=DataType.from_dict(input_format),
    output_schema=DataType.from_dict(output_format),
    name="Business Finder",
    memory=LocalMemory(memory_name=config.memory_index, overwrite=True),
)

my_agent.add_role()
my_agent.add_goals()
my_agent.add_plan()
my_agent.add_constraints()
my_agent.add_tools()
my_agent.add_performance_evaluations()
my_agent.add_context()
my_agent.add_memories()
my_agent.add_exmaples()

my_dataset = Dataset.load("tests/data/structured.json")

# this will open command line or UI depending on the agent configuration
output = my_agent.run(input=my_dataset)

score = Evaluator(metrics="exact_match").run(predictions=output, ground_truth=my_dataset)
