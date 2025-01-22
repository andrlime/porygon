"""
A struct to represent the score state of the game
"""

from dataclasses import dataclass


@dataclass
class Score:
    """
    NOTE: These are based on the "Chinese core values"
    https://carnegieendowment.org/research/2013/11/chinas-traditional-cultural-values-and-national-identity?lang=en

    Each of these are integers from 0-16. Single prompts may affect multiple score values by between -4 and 4.
    As soon as a single score value reaches zero, the player loses. To win, in this game, is to "not lose".
    """

    harmony: int
    benevolence: int
    courtesy: int
    wisdom: int
    honesty: int
    respect: int

    def to_json(self):
        return {
            "harmony": self.harmony,
            "benevolence": self.benevolence,
            "courtesy": self.courtesy,
            "wisdom": self.wisdom,
            "honesty": self.honesty,
            "respect": self.respect,
        }
