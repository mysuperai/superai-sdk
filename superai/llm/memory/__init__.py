from superai.llm.configuration import Configuration
from superai.llm.memory.base import Memory
from superai.llm.memory.local import LocalMemory
from superai.llm.memory.no_memory import NoMemory

config = Configuration()

# List of supported memory backends
# Add a backend to this list if the import attempt is successful
supported_memory = ["local", "no_memory"]

try:
    from superai.llm.memory.pinecone import PineconeMemory

    supported_memory.append("pinecone")
except ImportError:
    # print("Pinecone not installed. Skipping import.")
    PineconeMemory = None


def get_memory(memory_backend, init=False):
    memory = None
    if memory_backend == "pinecone":
        if not PineconeMemory:
            print("Error: Pinecone is not installed. Please install pinecone" " to use Pinecone as a memory backend.")
        else:
            memory = PineconeMemory()
            if init:
                memory.clear()

    if memory is None:
        memory = LocalMemory(memory_name=config.memory_index, overwrite=True)
        if init:
            memory.clear()
    return memory


def get_supported_memory_backends():
    return supported_memory


__all__ = [
    "Memory",
    "LocalMemory",
    "PineconeMemory",
    "NoMemory",
    "get_memory",
    "get_supported_memory_backends",
]
