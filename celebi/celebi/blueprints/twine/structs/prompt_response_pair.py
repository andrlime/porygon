"""
A struct to represent the score state of the game
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class PromptResponsePair:
    message: Optional[str]
    response: Optional[str]

    def to_json(self) -> dict[Optional[str], Optional[str]]:
        return {
            "previous_msg": self.message,
            "previous_response": self.response,
        }
