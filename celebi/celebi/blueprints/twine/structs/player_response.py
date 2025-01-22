"""
A struct for the player's response
"""

from dataclasses import dataclass

from .score import Score


@dataclass
class PlayerResponse:
    msg: str
    score: Score
