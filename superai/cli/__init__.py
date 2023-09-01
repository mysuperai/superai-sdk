"""Main entrypoint for the CLI.
The actual commands and groups are defined in the other modules in this package."""
import signal
import sys

import click

from superai.cli.ai import ai_group
from superai.cli.config import config, env, info, login, login_sso, logout
from superai.cli.misc import api_client
from superai.log import logger

log = logger.get_logger(__name__)


def _signal_handler(s, f):
    sys.exit(1)


@click.group()
def cli():
    pass


# To add a new command, create a new file in the cli folder and import it here
# define a new command or group with @click.command() or @click.group()
# and add it to this cli group with cli.add_command()
commands = [ai_group, api_client, info, env, config, login, login_sso, logout]
for command in commands:
    cli.add_command(command)


def main():
    """Entrypoint"""
    signal.signal(signal.SIGINT, _signal_handler)
    sys.exit(cli())


if __name__ == "__main__":
    main()
