import itertools
import logging
import os
import random
import re
import sys
import threading
import time
from logging import LogRecord

from colorama import Back, Fore, Style

from superai.llm.configuration import Configuration, Singleton
from superai.llm.utilities.prompt_utils import generate_ordered_list

config = Configuration()

COLOR_MAP = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "blue": Fore.BLUE,
    "white": Fore.WHITE,
    "yellow": Fore.YELLOW,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
}


class CustomLogger(metaclass=Singleton):
    def __init__(self):
        log_directory = os.path.join(os.path.dirname(__file__), "../logs")
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        activity_log = "activity.log"
        error_log = "error.log"

        console_format = FormatterWithColor("%(title_color)s %(message)s")

        self.typing_handler = Handler()
        self.typing_handler.setLevel(logging.INFO)
        self.typing_handler.setFormatter(console_format)

        self.console_handler = ConsoleHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(console_format)

        self.file_handler = logging.FileHandler(os.path.join(log_directory, activity_log), "a", "utf-8")
        self.file_handler.setLevel(logging.DEBUG)
        info_format = FormatterWithColor("%(asctime)s %(levelname)s %(title)s %(message_no_color)s")
        self.file_handler.setFormatter(info_format)

        error_handler = logging.FileHandler(os.path.join(log_directory, error_log), "a", "utf-8")
        error_handler.setLevel(logging.ERROR)
        error_format = FormatterWithColor(
            "%(asctime)s %(levelname)s %(module)s:%(funcName)s:%(lineno)d %(title)s" " %(message_no_color)s"
        )
        error_handler.setFormatter(error_format)

        self.logger = logging.getLogger("super.logger")
        self.logger.addHandler(self.typing_handler)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(error_handler)
        self.logger.setLevel(logging.DEBUG)

    def log(self, title="", title_color="", message="", level=logging.INFO):
        if message:
            if isinstance(message, list):
                message = " ".join(str(x) for x in message)
            elif not isinstance(message, str):
                message = str(message)
        else:
            message = ""

        if isinstance(title_color, str):
            color = COLOR_MAP.get(title_color.lower(), None)
            if color:
                title_color = color

        self.logger.log(level, message, extra={"title": title, "color": title_color})

    def debug(self, message, title="DEBUG: "):
        self._log(title, Fore.CYAN, message, logging.INFO)

    def info(self, message, title="INFO: "):
        self._log(title, Fore.GREEN, message, logging.INFO)

    def warn(self, message, title="WARNING: "):
        self._log(title, Fore.YELLOW, message, logging.WARN)

    def error(self, message, title="ERROR: "):
        self._log(title, Fore.RED, message, logging.ERROR)

    def critical(self, message, title="CRITICAL: "):
        self._log(title, Fore.RED + Back.WHITE, message, logging.ERROR)

    def _log(self, title="", title_color="", message="", level=logging.INFO):
        if message:
            if isinstance(message, list):
                message = " ".join(message)
        self.logger.log(level, message, extra={"title": title, "color": title_color})

    def set_level(self, level):
        self.logger.setLevel(level)


class Handler(logging.StreamHandler):
    def emit(self, record):
        min_speed = 0.05
        max_speed = 0.01

        msg = self.format(record)
        try:
            words = msg.split()
            for i, word in enumerate(words):
                print(word, end="", flush=True)
                if i < len(words) - 1:
                    print(" ", end="", flush=True)
                typing_speed = random.uniform(min_speed, max_speed)
                time.sleep(typing_speed)
                min_speed = min_speed * 0.95
                max_speed = max_speed * 0.95
            print()
        except Exception:
            self.handleError(record)


class ConsoleHandler(logging.StreamHandler):
    def emit(self, record) -> None:
        msg = self.format(record)
        try:
            print(msg)
        except Exception:
            self.handleError(record)


class FormatterWithColor(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        if hasattr(record, "color"):
            record.title_color = getattr(record, "color") + getattr(record, "title") + " " + Style.RESET_ALL
        else:
            record.title_color = getattr(record, "title")
        if hasattr(record, "msg"):
            record.message_no_color = remove_color_codes(getattr(record, "msg"))
        else:
            record.message_no_color = ""
        return super().format(record)


def remove_color_codes(s: str) -> str:
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", s)


logger = CustomLogger()


class Spinner:
    """A simple spinner class"""

    def __init__(self, message: str = "Loading...", delay: float = 0.1) -> None:
        """Initialize the spinner class
        Args:
            message (str): The message to display.
            delay (float): The delay between each spinner update.
        """
        self.spinner = itertools.cycle(["-", "/", "|", "\\"])
        self.delay = delay
        self.message = message
        self.running = False
        self.spinner_thread = None

    def spin(self) -> None:
        """Spin the spinner"""
        while self.running:
            sys.stdout.write(f"{next(self.spinner)} {self.message}\r")
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write(f"\r{' ' * (len(self.message) + 2)}\r")

    def __enter__(self):
        """Start the spinner"""
        self.running = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        """Stop the spinner
        Args:
            exc_type (Exception): The exception type.
            exc_value (Exception): The exception value.
            exc_traceback (Exception): The exception traceback.
        """
        self.running = False
        if self.spinner_thread is not None:
            self.spinner_thread.join()
        sys.stdout.write(f"\r{' ' * (len(self.message) + 2)}\r")
        sys.stdout.flush()

    def update_message(self, new_message, delay=0.1):
        """Update the spinner message
        Args:
            new_message (str): New message to display
            delay: Delay in seconds before updating the message
        """
        time.sleep(delay)
        sys.stdout.write(f"\r{' ' * (len(self.message) + 2)}\r")  # Clear the current message
        sys.stdout.flush()
        self.message = new_message


if __name__ == "__main__":
    logger.info("You are in info mode" "Hi")
    logger.warn("You are in warn mode" "Hi")
    logger.debug("You are in debug mode" "Hi")
    logger.error("You are in error mode" "Hi")
    logger.critical("You are in critical mode" "Hi")
    logger.log(title="Hello, ", title_color=Fore.CYAN, message="World!")


def print_ai_output(name: str, response: dict, command=None, output=None) -> None:
    thoughts = response.get("thoughts", {})
    if thoughts:
        thoughts_reasoning = thoughts.get("reasoning")
        thoughts_plan = thoughts.get("plan")
        thoughts_criticism = thoughts.get("criticism")

        thoughts_text = thoughts.get("text")
        if thoughts_text:
            logger.log(f"{name.upper()} THOUGHTS:", Fore.YELLOW, f"{thoughts_text}")

        if thoughts_reasoning:
            logger.log("REASONING:", Fore.YELLOW, f"{thoughts_reasoning}")
        if thoughts_plan:
            logger.log("PLAN:", Fore.YELLOW, "")
            if isinstance(thoughts_plan, list):
                thoughts_plan = generate_ordered_list(thoughts_plan)
            elif isinstance(thoughts_plan, dict):
                thoughts_plan = str(thoughts_plan)
            logger.log("", Fore.YELLOW, f"{thoughts_plan}")
        if thoughts_criticism:
            logger.log("CRITICISM:", Fore.YELLOW, f"{thoughts_criticism}")

    if command is not None:
        logger.log(f"COMMAND:", Fore.YELLOW, f"{command}")

    if output is not None:
        logger.log(f"CURRENT OUTPUT:", Fore.YELLOW, f"{output}")
