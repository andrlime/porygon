"""
A struct to represent the score state of the game
"""

from dataclasses import dataclass


@dataclass
class PromptResponsePair:
    previous_msg: str
    previous_response: str

    def to_json(self):
        return {
            "previous_msg": self.previous_msg,
            "previous_response": self.previous_response,
        }
