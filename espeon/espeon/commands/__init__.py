"""
Command interface
"""

import os
import importlib
import inspect
import logging

from enum import Enum
from types import SimpleNamespace

from .command import Command, CommandChain


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


# LLM Generated
command_namespace = {}

module = importlib.import_module(f".commands", package=__name__)
for name, obj in inspect.getmembers(module):
    if inspect.isclass(obj) and issubclass(obj, Command) and obj is not Command:
        logger.info(f"Imported command {name}")
        command_namespace[name] = obj

CommandList = SimpleNamespace(**command_namespace)
