"""
A class to prompt the OpenAI REST API
"""

from celebi.core.flask.config import AppConfig
from .score import Score
from .prompt_response_pair import PromptResponsePair


class LLMPrompt:
    def __init__(self, game_state: Score, previous_prompt_response: PromptResponsePair):
        self.game_state = game_state
        self.previous_prompt_response = previous_prompt_response
        self.api_key = AppConfig().get_environment_variable("OPENAI_API_KEY")

    def prompt(self):
        openai_prompt = """
insert prompt text here
        """
        return openai_prompt
