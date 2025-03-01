"""
Error class for when a CLI value has an error
"""

import logging
import os


class CLIValueError(ValueError):
    def __init__(self, message: str):
        logging.error(message)
        os._exit(1)
        # super().__init__(message)
