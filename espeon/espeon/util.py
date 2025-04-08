"""
Some utility functions
"""


def encode_command(command: str, terminator: str = "\r"):
    """
    Encodes a string command into bytes
    """
    return f"{command}{terminator}".encode()
