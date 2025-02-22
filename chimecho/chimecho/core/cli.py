"""
CLI class that reads all arguments and returns a dict for use by any class
"""

from typing import AnyStr

import argparse
import os
import sys
import pathlib

from chimecho.core.exceptions import CLIValueError


class CLI:
    """
    CLI instance to read arguments from an array of strings
    """

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            prog="chimecho",
            description="""
Parses Markdown template schedules into a weekly schedule PNG
            """,
        )

        parser.add_argument(
            "-f",
            "--folder",
            help="Folder where templates are located",
            type=pathlib.Path,
            required=True,
        )
        parser.add_argument(
            "-l",
            "--label",
            help="The label for your calendar",
            type=str,
            required=True,
        )
        parser.add_argument(
            "-c",
            "--container-height",
            help="How high the display screen is in pixels",
            type=int,
            required=True,
        )
        parser.add_argument(
            "-o",
            "--output-file",
            help="File name to output to, both output.html and output.png",
            type=str,
            required=True,
        )

        self.args = parser.parse_args(sys.argv[1:])
        self.lint()

    def lint(self) -> None:
        arguments = self.args

        if not os.path.isdir(os.path.abspath(arguments.folder)):
            raise CLIValueError(f"Invalid path to folder {arguments.folder}")
        if not isinstance(arguments.label, str):
            raise CLIValueError(f"Invalid label for calendar {arguments.label}")
        if not isinstance(arguments.container_height, int):
            raise CLIValueError(
                f"Invalid container height for calendar {arguments.container_height}"
            )
        if not isinstance(arguments.output_file, str):
            raise CLIValueError(
                """
Invalid output_file for calendar {arguments.output_file}
(if this input was intentional, wrap it with "...")
                """
            )

    def get_parameters(self) -> dict[str, str]:
        return vars(self.args)

    def get_parameter_by_key(self, key: AnyStr) -> str:
        try:
            key_str = str(key)
            return str(vars(self.args)[key_str])
        except ValueError as e:
            raise CLIValueError(f"CLI does not contain key {str(key)}") from e

    def get_path_by_key(self, key: AnyStr) -> str:
        path = self.get_parameter_by_key(key)
        return os.path.abspath(path)
