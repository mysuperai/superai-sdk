from superai.llm.logger import logger
from superai.llm.memory.local import LocalMemory
from superai.llm.memory.pinecone import PineconeMemory

# Create an instance of LocalMemory:
local_memory = LocalMemory()

# Add data to the local_memory:
local_memory.add("The quick brown fox jumps over the lazy dog.")
local_memory.add("The rain in Spain stays mainly in the plain.")
local_memory.add("To be, or not to be: that is the question.")
logger.log(title="Local Memory:", title_color="cyan", message="Data added to Local Memory")

# Get relevant data from the local_memory:
query = "What's the famous phrase about a fox and a dog?"
relevant_data = local_memory.get(query)
logger.log(title="New Prompt Input:", title_color="cyan", message=query)
logger.log(title="Local Memory Result:", title_color="cyan", message=str(relevant_data))

# Create an instance of PineconeMemory:
pinecone_memory = PineconeMemory()

# Add data to the pinecone_memory:
pinecone_memory.add("The quick brown fox jumps over the lazy dog.")
pinecone_memory.add("The rain in Spain stays mainly in the plain.")
pinecone_memory.add("To be, or not to be: that is the question.")
logger.log(title="Pinecone Memory:", title_color="cyan", message="Data added to Pinecone Memory")

# Get relevant data from the pinecone_memory:
query = "What's the famous phrase about a fox and a dog?"
relevant_data = pinecone_memory.get(query)
logger.log(title="New Prompt Input:", title_color="cyan", message=query)
logger.log(title="Pinecone Memory Result:", title_color="cyan", message=str(relevant_data))
