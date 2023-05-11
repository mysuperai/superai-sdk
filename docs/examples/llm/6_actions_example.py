from superai.llm.actions import (
    BingSearchAction,
    CompleteAction,
    DuckDuckGoSearchAction,
    GoogleSearchAction,
    HumanFeedbackAction,
    SerperSearchAction,
    SerpSearchAction,
    WikipediaSearchAction,
    WolframAlphaAction,
)
from superai.llm.logger import logger

# Example 1: Google Search Action
google_search = GoogleSearchAction()
query = "What is the tallest building in the world?"
result = google_search.run(query)
logger.log(title="Google Search Result:", title_color="cyan", message=result)

# # Example 2: Choose Examples Action
# choose_examples = ChooseExamplesAction()
# result = choose_examples.run(input={"examples": ["Example 1", "Example 2", "Example 3", "Example 4", "Example 5"]})
# logger.log(title="Choose Examples Result:", title_color="cyan", message=result)

# Example 3: Human Feedback Action
human_feedback = HumanFeedbackAction()
question = "What can we do to reduce plastic waste?"
result = human_feedback.run(question)
logger.log(title="Human Feedback Result:", title_color="cyan", message=result)

# Example 4: Serper Search Action
serper_search = SerperSearchAction()
query = "How many species of birds are there?"
result = serper_search.run(query)
logger.log(title="Serper Search Result:", title_color="cyan", message=result)

# Example 5: Bing Search Action
bing_search = BingSearchAction()
query = "What is the tallest building in the world?"
result = bing_search.run(query)
logger.log(title="Bing Search Result:", title_color="cyan", message=result)

# Example 6: Duck Duck Go Search Action
duck_duck_go_search = DuckDuckGoSearchAction()
query = "What is the tallest building in the world?"
result = duck_duck_go_search.run(query)
logger.log(title="Duck Duck Go Search Result:", title_color="cyan", message=result)

# Example 7: Serp Search Action
serp_search = SerpSearchAction()
query = "What is the tallest building in the world?"
result = serp_search.run(query)
logger.log(title="Serp Search Result:", title_color="cyan", message=result)

# Example 8: Wikipedia Search Action
wikipedia_search = WikipediaSearchAction()
query = "What is the tallest building in the world?"
result = wikipedia_search.run(query)
logger.log(title="Wikipedia Search Result:", title_color="cyan", message=result)

# Example 9: Wolfram Alpha Search Action
wolfram_alpha_search = WolframAlphaAction()
query = "What is the tallest building in the world?"
result = wolfram_alpha_search.run(query)
logger.log(title="Wolfram Alpha Search Result:", title_color="cyan", message=result)

# Example 10: Complete Action
complete = CompleteAction()
reason_for_completing = "I've finished the output your requested"
result = complete.run(reason_for_completing)
logger.log(title="Complete Result:", title_color="cyan", message=result)
