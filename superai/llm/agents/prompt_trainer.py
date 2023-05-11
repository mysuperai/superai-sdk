import json
import random
import time

from superai.llm.agents import Agent
from superai.llm.configuration import Configuration
from superai.llm.data_types.message import ChatMessage
from superai.llm.logger import Spinner, logger, print_ai_output
from superai.llm.utilities import generate_ordered_list
from superai.llm.utilities.parser_utils import Parser

config = Configuration()


from colorama import Fore, Style


def get_user_feedback(command_name, arguments):
    print(
        f"NEXT ACTION: COMMAND = {Fore.CYAN}{command_name}{Style.RESET_ALL}  "
        f"ARGUMENTS = {Fore.CYAN}{arguments}{Style.RESET_ALL}"
    )
    print("Enter 'y' to authorize the command, 'n' to reject, or any other input to provide feedback:", flush=True)
    user_feedback = input(Fore.MAGENTA + "Input: " + Style.RESET_ALL).strip().lower()

    if user_feedback in ["y", "yes"]:
        return "GENERATE NEXT COMMAND JSON"
    elif user_feedback in ["n", "no"]:
        return "EXIT"
    else:
        return user_feedback


class PromptTrainerAgent(Agent):
    def run(self, input, ground_truth=None):
        self.input = input
        self.output = None

        user_feedback = input
        command = None
        loop_count = 0

        while True:
            loop_count += 1

            # check if we should stop
            if self.stop_criteria_met(loop_count, command):
                break

            # consult foundation model what to do next
            with Spinner("Super.AI is processing..."):
                prompt = self.generate_prompt(user_feedback=user_feedback)
                response = self.foundation_model.predict(prompt)

            # parse ai response
            output_parser = Parser(
                use_ai=False,
                prompt=prompt,
                prompt_output_format=self.prompt_output_format,
                output_schema=self.output_schema.dict(),
            )
            valid_response = output_parser.to_dict(response)

            # parse command from response
            command = output_parser.get_command(response)

            # parse output from response (which are the prompt candidates)
            self.output = output_parser.get_output(response)

            # calculate scores for each prompt candidate
            self.evaluate_output(self.output, ground_truth)

            # # update score
            # self.evaluations.append(score)
            # self.prompt_history.append({'prompt':prompt, 'score':score, 'loop_count':loop_count})

            print_ai_output(name=self.name, response=valid_response, command=command, output=self.output)

            # get user input on what to do next
            user_feedback = get_user_feedback(command["name"], command["args"])

            if user_feedback == "GENERATE NEXT COMMAND JSON":
                logger.log("-=-=-=-=-=-=-= COMMAND AUTHORISED BY USER -=-=-=-=-=-=-=", Fore.MAGENTA, "")
                # execute command that AI suggested
                command_output = execute_command(**command)
                # command_output = execute_command(**command)
                # update prompt components based on command output
                # self.update_prompt_components(command_output)
            elif user_feedback == "EXIT":
                logger.log("-=-=-=-=-=-=-= COMMAND REJECTED BY USER -=-=-=-=-=-=-=", Fore.MAGENTA, "")
                break
            else:
                logger.log("-=-=-=-=-=-=-= USER PROVIDED FEEDBACK -=-=-=-=-=-=-=", Fore.MAGENTA, "")
                command = {"name": "human_feedback", "args": {}}
                command_output = f"Human feedback: {user_feedback}"

            # update database of memories
            memory_to_add = (
                f"AI Reply: {valid_response} "
                f"\nResult: {command_output} "
                f"\nHuman Feedback: {user_feedback} "
                f"\nPrompt History: {self.prompt_history} "
            )
            self.database.add(memory_to_add)

            # update message history
            # TODO store this in a database
            if user_feedback is not None:
                self.message_history.append(ChatMessage(content=json.dumps(user_feedback), role="user"))
            if valid_response is not None:
                self.message_history.append(ChatMessage(content=json.dumps(valid_response), role="assistant"))
            if command_output is not None:
                self.message_history.append(ChatMessage(content=command_output, role="system"))
            else:
                self.message_history.append(ChatMessage(content="Unable to execute command", role="system"))

        # create final response in line with output schema
        # TODO: check that it validates against output schema if not fix it
        return json.loads(response)["output"]

    def stop_criteria_met(self, loop_count, command):
        # TODO: loop through all stop criteria and return true if any are met
        if loop_count > config.autonomous_limit:
            if config.debug:
                logger.debug("Stop criteria met with `autonomous_limit` being reached command")
            return True
        if command is not None:
            if command["name"] in ["task_complete", "exit", "quit", "do_nothing"]:
                if config.debug:
                    logger.debug("Stop criteria met with `task_complete` command")
                return True

        if config.debug:
            logger.debug("Stop criteria not yet met")
        return False

    def generate_system_prompt(
        self,
        name: str = None,
        role: str = None,
        prompt_prefix: str = None,
        prompt_suffix: str = None,
        goals: list = None,
        advice: list = None,
        constraints: list = None,
        output_schema: dict = None,
        actions: list = None,
        output=None,
    ):
        system_prompt = ""

        if prompt_prefix is None:
            system_prompt += f"{prompt_prefix}"
        if name is not None:
            system_prompt += f"\n\nYou are {name}"
            if role is not None:
                system_prompt += f", {role}"
        else:
            if role is not None:
                system_prompt += f"\n\nYour role is {role}."

        if goals:
            system_prompt += f"\n\nGoals:\n{generate_ordered_list(goals)}"
        if advice:
            system_prompt += f"\n\nAdvice:\n{generate_ordered_list(advice)}"
        if constraints:
            system_prompt += f"\n\nConstraints:\n{generate_ordered_list(constraints)}"
        if actions:
            system_prompt += f"\n\Actions:\n{generate_ordered_list(actions, item_type='action')}"
        # if context:
        #     system_prompt += f"\n\nContext:\n{generate_ordered_list(context)}"
        # if examples:
        #     system_prompt += f"\n\nExamples:\n{generate_ordered_list(examples)}"

        # add overall goal
        system_prompt += f"""\n\nMaster Goal:\nYour overall goal is to generate an output that can validate against the following JSON schema:\n{output_schema.to_text()}"""
        system_prompt += f"\n\nThis is the output you have so far:\n{output}"
        system_prompt += f"\nWhen you have filled out the entire output, you need to complete your task."

        if not self.prompt_output_format:
            prompt_output_format = {
                "thoughts": {
                    "text": "thought",
                    "reasoning": "reasoning",
                    "plan": "- short bulleted\n- list that conveys\n- long-term plan",
                    "criticism": "constructive self-criticism",
                    "speak": "thoughts summary to say to user",
                },
                "command": {"name": "command name", "args": {}},
                "output": {},
            }
        formatted_response_format = json.dumps(prompt_output_format, indent=4)
        system_prompt += f"\n\nYou should only respond in JSON format as described below \nResponse Format:\n{formatted_response_format}\nEnsure the response can be parsed by Python json.loads"
        if prompt_suffix is None:
            system_prompt += f"\n\n{prompt_suffix}"

        return ChatMessage(content=system_prompt, role="system")

    def evaluate_output(self, outputs, ground_truth):
        return {
            "accuracy": random.random(),
            "f1": random.random(),
            "precision": random.random(),
            "recall": random.random(),
        }

    def generate_prompt(self, user_feedback=None, max_send_tokens=None):

        # add prompt prefix

        # generate system prompt

        # add prompt suffix

        if user_feedback is None:
            user_feedback = ""
        if max_send_tokens is not None:
            self.max_send_tokens = max_send_tokens
        else:
            self.max_send_tokens = self.foundation_model.token_limit - 1000

        messages = []  # messages to send to LLM

        # construct main system prompt for LLM which is everything it needs to know to acheive its goals
        system_prompt = self.generate_system_prompt()
        messages.append(system_prompt)

        # add the current date for context
        messages.append(ChatMessage(content=f"The current time and date is {time.strftime('%c')}", role="system"))

        # add relevant memories to prompt if they exist
        if self.message_history:
            relevant_memories = self.get_relevant_memories(data=self.message_history[-9:], n=9)
            if relevant_memories:
                messages.append(
                    ChatMessage(
                        content=f"This reminds you of these events from your past:\n{relevant_memories}\n\n",
                        role="system",
                    )
                )

        if self.evaluations:
            messages.append(
                ChatMessage(
                    content=f"Your performance so far has been evaluated as:\n{generate_ordered_list(self.evaluations)}",
                    role="system",
                )
            )
        # add the most recent messages (as much that fit into max_send_tokens)
        # TODO: implement while true loop
        if self.message_history:
            messages.append(self.message_history[-1])

        if self.prompt_history:
            n = 3
            sorted_prompt_history = sorted(self.prompt_history, key=lambda x: x["score"], reverse=True)
            messages.append(
                ChatMessage(
                    content=f"These are the best {n} prompts so far:\n{generate_ordered_list(sorted_prompt_history[-n:])}",
                    role="user",
                )
            )

        # add user input to messages
        if user_feedback:
            user_feedback_content = f"\n\nUser Feedback:\n{user_feedback}"
            messages.append(ChatMessage(content=user_feedback_content, role="user"))

        # add triggering prompt to help AI stay on track with its goal
        if self.triggering_prompt is not None:
            messages.append(ChatMessage(content=self.triggering_prompt, role="user"))

        self.prompt = messages
        return self.prompt

    def _generate_similar_prompts(self, prompt, max_prompt_size, reduce_prompt_size):
        # Generate similar prompts
        pass

    def _generate_prompt(self, max_prompt_size, reduce_prompt_size):
        # Generate a new prompt
        pass

    def _score_candidate_prompts(self, candidate_prompts, data=None):
        # Score candidate prompts
        pass

    def _stop_criteria_met(self, output_prompts, stop_criteria):
        # Check if the stop criteria is met
        pass

    def _evaluate_criteria(self, candidate_prompts, constraints):
        # Evaluate prompts based on criteria
        pass

    def score(self, data=None):
        # Implement the scoring function here based on your foundation_model and problem type
        raise

    def _improve_prompt(
        self, prompt, goals=["improve examples", "improve instructions", "improve context", "improve chain of thought"]
    ):
        for goal in goals:
            if goal == "improve examples":
                # Improve examples
                pass
            elif goal == "improve instructions":
                # Improve instructions
                pass
            elif goal == "improve context":
                # Improve context
                pass
            elif goal == "improve chain of thought":
                # Improve chain of thought
                pass
        return prompt

    def _reduce_prompt_size(self, prompt, max_prompt_size):
        while len(prompt) > max_prompt_size:
            # Reduce examples
            # Remove punctuation
            # Summarize examples
            # Summarize instructions
            # Convert examples to chain of thought
            pass
        return prompt

    def _generate_candidate_prompts(
        self, prompts, n=10, n_resample=1, max_prompt_size=None, reduce_prompt_size=False, improve_prompt=False
    ):
        raise NotImplementedError
