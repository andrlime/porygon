"""
Interface for a single command for RS232
"""

from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


class CommandChain:
    """
    A sequence of ESP300 commands joined by semicolons
    """

    def __init__(self, command, terminator: str = "\r"):
        self.commands = [command]
        self.terminator = terminator

    def push_back(self, command) -> None:
        self.commands.append(command)

    def to_string(self) -> str:
        return "; ".join(cmd.to_string() for cmd in self.commands).strip()

    def encode(self) -> bytes:
        return (self.to_string() + self.terminator).encode()


@dataclass
class Command:
    """
    A single ESP300 command in the form:
    <prefix><command><postfix>

    Notes:
    1. Spaces are optional but cost memory
    2. Semicolons can be used to chain commands
    3. Commands are executed after a flush with "\r"
    """

    command: str
    prefix: str = None
    postfix: str = None
    terminator: str = "\r"

    def to_string(self) -> str:
        cmd = ""
        assert self.command is not None, "Command is required"

        if self.prefix is not None:
            cmd += f"{self.prefix} "
        cmd += self.command
        if self.postfix is not None:
            cmd += f" {self.postfix}"

        return cmd.strip()

    def encode(self) -> bytes:
        return (self.to_string() + self.terminator).encode()
