"""
All blueprints imported in one module
"""

from celebi.blueprints.root.api import bp as root
from celebi.blueprints.twine.api import bp as twine
from celebi.blueprints.wildcat.api import bp as wildcat


def all_blueprints():
    return [("", root), ("twine", twine), ("wildcat", wildcat)]
