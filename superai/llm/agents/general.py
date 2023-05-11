import json
import time

from superai.llm.agents import Agent
from superai.llm.configuration import Configuration
from superai.llm.data_types.message import ChatMessage
from superai.llm.logger import Spinner, logger, print_ai_output
from superai.llm.prompts import Prompt
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


class GeneralAgent(Agent):
    def run(self, input):
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
            # parse output from response
            self.output = output_parser.get_output(response)

            print_ai_output(name=self.name, response=valid_response, command=command, output=self.output)

            # get user input on what to do next
            user_feedback = get_user_feedback(command["name"], command["params"])

            if user_feedback == "GENERATE NEXT COMMAND JSON":
                logger.log("-=-=-=-=-=-=-= COMMAND AUTHORISED BY USER -=-=-=-=-=-=-=", Fore.MAGENTA, "")
                # execute command that AI suggested
                command_output = execute_command(**command)
            elif user_feedback == "EXIT":
                logger.log("-=-=-=-=-=-=-= COMMAND REJECTED BY USER -=-=-=-=-=-=-=", Fore.MAGENTA, "")
                break
            else:
                logger.log("-=-=-=-=-=-=-= USER PROVIDED FEEDBACK -=-=-=-=-=-=-=", Fore.MAGENTA, "")
                command = {"name": "human_feedback", "params": {}}
                command_output = f"Human feedback: {user_feedback}"

            # update database of memories
            memory_to_add = (
                f"AI Reply: {valid_response} " f"\nResult: {command_output} " f"\nHuman Feedback: {user_feedback} "
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

    def generate_prompt(self, user_feedback=None, max_send_tokens=None):
        if user_feedback is None:
            user_feedback = ""
        if max_send_tokens is not None:
            self.max_send_tokens = max_send_tokens
        else:
            self.max_send_tokens = self.foundation_model.token_limit - 1000
        if self.message_history:
            self.memories = self.get_relevant_memories(data=self.message_history[-9:], n=9)

        messages = []  # messages to send to LLM

        # add the current date for context
        messages.append(ChatMessage(content=f"The current time and date is {time.strftime('%c')}", role="system"))

        # construct main system prompt for LLM which is everything it needs to know to acheive its goals
        system_prompt = Prompt.from_components(
            name=self.name,
            role=self.role,
            goals=self.goals,
            advice=self.adice,
            constraints=self.constraints,
            actions=self.actions,
            context=self.context,
            examples=self.examples,
            input=self.input,
            output=self.output,
            output_format=self.prompt_output_format,
            memories=self.memories,
            user_feedback=user_feedback,
            performance_evaluations=self.performance_evaluations,
        )

        messages.append(ChatMessage(content=system_prompt.to_string(), role="system"))

        self.prompt = messages
        return self.prompt
