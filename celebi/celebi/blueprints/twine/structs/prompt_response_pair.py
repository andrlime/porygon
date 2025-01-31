"""
A struct to represent the score state of the game
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class PromptResponsePair:
    message: Optional[str]
    response: Optional[str]

    def to_json(self):
        return {
            "previous_msg": self.previous_msg,
            "previous_response": self.previous_response,
        }
