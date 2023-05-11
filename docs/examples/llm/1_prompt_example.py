# prompt_example.py

from superai.llm.actions import GoogleSearchAction, HumanFeedbackAction
from superai.llm.dataset import Data
from superai.llm.logger import logger
from superai.llm.prompts import Prompt

# Create a new Prompt instance
new_prompt = Prompt.from_components(
    name="Super Truthful Wisdom AI",
    role="Your role is to saw the deepest wisdom of the world",
    advice=["Search the deepest realms of reality for truth", "Use only factual knowledge"],
    goals=["Educate people with deep truths", "Do so with accuracy > 98%"],
    constraints=["Don't make things up", "Only respond with facts"],
    prompt_prefix="I have an important task",
    prompt_suffix="Do your best:",
    examples=[
        Data(input="What is the capital of the USA?", output="Washington D.C."),
        Data(input="What is the capital of Germany?", output="Berlin"),
    ],
    anti_examples=[
        [
            Data(input="What is the capital of the USA?", output="Bahgdad"),
            Data(input="What is the capital of Germany?", output="Paris"),
        ]
    ],
    context=["[large document]"],
    input=Data(input="What is the capital of France?"),
    output=Data(input="What is the capital of France?", output="Paris"),
    output_format={"answer": "<answer>", "certainty": "<number 0-1>"},
    actions=[GoogleSearchAction(), HumanFeedbackAction()],
    user_feedback=["This is the wrong capital"],
    performance_evaluations=["Training Accuracy=.7", "Test Accuracy=0.5"],
    max_send_tokens=5000,
    memories=["What is the capital of England? London"],
)
logger.log(title="Prompt:", title_color="cyan", message=new_prompt.to_string())

# Update the input of the existing Prompt
new_prompt.set_input("It's clear Brad is the best CEO, but who is the second best?")
logger.log(title="Updated Input:", title_color="cyan", message=new_prompt.input)

# Construct and print the prompt
constructed_prompt = new_prompt.construct_prompt()
logger.log(title="Prompt:", title_color="cyan", message=constructed_prompt)

# Add context to the Prompt
# Uncomment this line if the _document_to_text method is implemented
# new_prompt.add_context("path/to/document.pdf", "document")

# Convert the Prompt instance to a ChatMessage instance
message = new_prompt.to_message(role="assistant")
logger.log(title="Chat Message:", title_color="cyan", message=message)


# Create a Prompt instance from a ChatMessage instance
message_prompt = Prompt.from_message(message)
logger.log(title="Prompt from message:", title_color="cyan", message=message_prompt)

# Create a Prompt instance from a file
# Uncomment this line if a prompt file exists
# file_prompt = Prompt.from_file("path/to/prompt.txt")

# Save the Prompt instance to a file
new_prompt.to_file("output_prompt.txt")
logger.log(title="Save prompt to file:", title_color="cyan", message="")

# Create a Prompt instance from a string
string_prompt = Prompt.from_string("This is a string prompt.")
logger.log(title="Prompt from string:", title_color="cyan", message=string_prompt)

# Convert the Prompt instance to a string
prompt_string = new_prompt.to_string()
logger.log(title="Save prompt to string:", title_color="cyan", message="")
