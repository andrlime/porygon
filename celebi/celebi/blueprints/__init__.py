"""
All blueprints imported in one module
"""

from flask import Blueprint

from dataclasses import dataclass

from .root.api import bp as root
from .twine.api import bp as twine
from .wildcat.api import bp as wildcat


@dataclass
class BlueprintWrapper:
    path: str
    blueprint: Blueprint


def all_blueprints() -> list[BlueprintWrapper]:
    return [
        BlueprintWrapper(path="", blueprint=root),
        BlueprintWrapper(path="twine", blueprint=twine),
        BlueprintWrapper(path="wildcat", blueprint=wildcat),
    ]
