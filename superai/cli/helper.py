import functools

import click


def pass_client(f):
    """Decorator to pass client object when needed in the Click context.
    Will add the first function argument as the client object."""

    @functools.wraps(f)
    @click.pass_context
    def wrapper(*args, **kwargs):
        ctx = args[0]
        return f(ctx.obj["client"], *args[1:], **kwargs)

    return wrapper


def common_params(func):
    @click.option("--verbose", "-v", is_flag=True, help="Verbose output")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
