from superai.llm.data_types.message import ChatMessage
from superai.llm.foundation_models import ChatGPT, OpenAIEmbedding
from superai.llm.logger import logger

# Example 1: Use ChatGPT to generate a response based on a single prompt.

# Initialize the ChatGPT instance
chat_gpt = ChatGPT()

# Create a single prompt
prompt = "Tell me a joke."

# Generate a response
response = chat_gpt.predict(prompt)

# Log the input and output
logger.log(title="New Prompt Input:", title_color="cyan", message=prompt)
logger.log(title="Generated Response:", title_color="cyan", message=response)

# Example 2: Use ChatGPT to generate a response based on a list of messages.
# Create a list of messages
messages = [
    ChatMessage(role="system", content="You are an assistant that speaks about animals."),
    ChatMessage(role="user", content="Tell me something interesting about dolphins."),
]

# Generate a response
response = chat_gpt.predict(messages)

# Log the input and output
logger.log(title="New Prompt Input:", title_color="cyan", message=[msg.content for msg in messages])
logger.log(title="Generated Response:", title_color="cyan", message=response)


# Example 3: Use OpenAIEmbedding to get the embeddings of some texts.

# Initialize the OpenAIEmbedding instance
embedding_model = OpenAIEmbedding()

# Create a list of texts to get embeddings for
texts = ["apple", "banana", "orange"]

# Get the embeddings
embeddings = embedding_model.predict(texts)

# Log the input and output
logger.log(title="Texts Input:", title_color="cyan", message=texts)
logger.log(title="Generated Embeddings:", title_color="cyan", message=embeddings)
