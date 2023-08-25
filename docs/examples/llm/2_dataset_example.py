import os

from superai.llm.data_types import Any
from superai.llm.dataset import Data, Dataset
from superai.llm.logger import logger

# Example 1: Creating Data instances and updating them
logger.log(title="Example 1: Creating Data instances and updating them", title_color="green")

data1 = Data(input="Input 1", output="Output 1")
logger.log(title="Data 1:", title_color="cyan", message=data1)

data2 = Data(input="Input 2", output="Output 2")
logger.log(title="Data 2:", title_color="cyan", message=data2)

data1.set_input(value="Updated Input 1")
data1.set_output(value="Updated Output 1")
logger.log(title="Updated Data 1:", title_color="cyan", message=data1)

data1.set_input(url="https://www.corpnet.com/wp-content/uploads/2022/01/Legal-Document.jpg")
data2.set_input(path=os.path.abspath("./local_input_data/Legal-Document.jpg"))
try:
    data1.set_input(
        path=os.path.abspath("./local_input_data/Legal-Document.jpg"),
        url="https://www.corpnet.com/wp-content/uploads/2022/01/Legal-Document.jpg",
    )
    logger.log("Should have thrown an error: ", "red", "You must provide only one of input value, url, or path.")
except ValueError as e:
    logger.log("Error raised successfully as expected: ", "green", e)

data1.set_output(url="https://www.corpnet.com/wp-content/uploads/2022/01/Legal-Document.jpg")
data2.set_output(path=os.path.abspath("./local_input_data/Legal-Document.jpg"))
try:
    data1.set_output(
        path=os.path.abspath("./local_input_data/Legal-Document.jpg"),
        url="https://www.corpnet.com/wp-content/uploads/2022/01/Legal-Document.jpg",
    )
    logger.log("Should have thrown an error: ", "red", "You must provide only one of output value, url, or path.")
except ValueError as e:
    logger.log("Error raised successfully as expected: ", "green", e)

assert isinstance(data1.input, bytes)
assert isinstance(data1.output, bytes)
assert isinstance(data2.input, bytes)
assert isinstance(data2.output, bytes)


# Example 2: Creating a Dataset and adding Data instances
logger.log(title="Example 2: Creating a Dataset and adding Data instances", title_color="green")

input_schema = Any()
output_schema = Any()

dataset = Dataset(input_schema=input_schema, output_schema=output_schema)
dataset.add_data(input="New Input 1", output="New Output 1")
dataset.add_data(input="New Input 2", output="New Output 2")

logger.log(title="Dataset:", title_color="cyan", message=dataset)

# Log the input of the first data point
first_data_point = dataset[0]
logger.log(title="New Prompt Input:", title_color="cyan", message=first_data_point.input)

# Example 3: Updating and deleting data in a Dataset
logger.log(title="Example 3: Updating and deleting data in a Dataset", title_color="green")

dataset.update_data(index=0, input="Updated New Input 1", output="Updated New Output 1")
logger.log(title="Dataset after updating data:", title_color="cyan", message=dataset)

dataset.delete_data(index=1)
logger.log(title="Dataset after deleting data:", title_color="cyan", message=dataset)

# Example 4: Splitting data in a Dataset
logger.log(title="Example 4: Splitting data in a Dataset", title_color="green")

# Add more data to the dataset
for i in range(3, 11):
    dataset.add_data(input=f"New Input {i}", output=f"New Output {i}")

dataset.create_splits(test_size=0.2, train_size=0.7, validation_size=0.1, seed=42)
train_dataset = dataset.get_split("train")
validation_dataset = dataset.get_split("validation")
test_dataset = dataset.get_split("test")

logger.log(title="Train Dataset:", title_color="cyan", message=train_dataset)
logger.log(title="Validation Dataset:", title_color="cyan", message=validation_dataset)
logger.log(title="Test Dataset:", title_color="cyan", message=test_dataset)
