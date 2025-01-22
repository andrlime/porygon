"""
A class to prompt the OpenAI REST API
"""

from .score import Score


class TwinePrompt:
    def __init__(self, msg, game_state: Score):
        self.msg = msg
        self.game_state = game_state
        self.api_key = 0  # TODO

    def prompt(self):
        openai_prompt = """
insert prompt text here
        """
        return openai_prompt
