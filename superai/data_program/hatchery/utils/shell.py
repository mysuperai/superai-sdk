""" Shell common utility """
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import os
import subprocess
import time


def execute_verbose(command):
    """Execute shell command and print stdout/err to the console"""
    start = time.time()
    os.system(command)
    end = time.time()
    return end - start


def execute(command):
    """Execute shell command with Popen"""
    start = time.time()
    FNULL = open(os.devnull, "w")
    res = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=FNULL)
    res.wait()
    end = time.time()
    logging.debug("pid: {}. Exit code: {}. Message: {}".format(res.pid, res.returncode, res.stdout.read()))
    return end - start


def get_directory_size(path="."):
    """Get directory size

    Implementation suggested from S.O.
    https://stackoverflow.com/questions/12480367/how-to-generate-directory-size-recursively-in-python-like-du-does
    """
    dirs_dict = {}

    # We need to walk the tree from the bottom up so that a directory can have easy
    # access to the size of its subdirectories.
    for root, dirs, files in os.walk(path, topdown=False):
        # Loop through every non directory file in this directory and sum their sizes
        size = sum(os.path.getsize(os.path.join(root, name)) for name in files)

        # Look at all of the subdirectories and add up their sizes from the `dirs_dict`
        subdir_size = sum(dirs_dict[os.path.join(root, d)] for d in dirs)

        # store the size of this directory (plus subdirectories) in a dict so we
        # can access it later
        my_size = dirs_dict[root] = size + subdir_size

        logging.info("{}: {}".format(root, my_size))
        return my_size


def create_python_command(args):
    """Create python shell command with args"""
    return "python {}".format(" ".join(args))


def which(program):
    """Test if program is installed on local machine"""

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
