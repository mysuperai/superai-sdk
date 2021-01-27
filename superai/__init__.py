from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "0.1.0.alpha1.build2"

# Client comes first
from .client import *

from superai.config import settings
from superai.data_program import Task, Worker
from superai.data_program.template import Template
from superai.data_program.instance import SuperAI
