"""
A class to prompt the OpenAI REST API
"""

import time

import numpy as np
from openai import OpenAI, RateLimitError

from mesprit.config import AppConfig


class PapalLLMEngine:
    """
    Can be passed around to prompt the LLM
    """

    def __init__(self, model: str, system_prompt: str):
        self.model = model
        api = AppConfig().get_environment_variable("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api)
        self.system_prompt = system_prompt

    def prompt(self, msg: str) -> str:
        """
        Prompts the LLM and returns the response
        """
        try:
            chat_response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": msg},
                ],
                model=self.model,
            )

            if not chat_response.choices[0].message.content:
                return ""

            return chat_response.choices[0].message.content
        except RateLimitError as e:
            print(f"Hit rate limit!")
            time.sleep(2)
            return self.prompt(msg)
