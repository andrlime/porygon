"""
Helper functions to configure settings
"""

import logging
from typing import Any, Tuple

from yaml import load, Loader

from chimecho.exceptions import ConfigValueError
from chimecho.cli import CLI


class AppConfig(object):
    """
    Singleton AppConfig class to read config from config.yml and
    return a single dictionary with those values
    """

    def __new__(cls) -> "AppConfig":
        if not hasattr(cls, "instance"):
            cls.instance = super(AppConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        if not hasattr(self, "config"):
            yml_config = self.read_yaml_config_file("config.yaml")
            cli_config = CLI()

            self.config = {
                "config": yml_config,
                "cli": cli_config.get_parameters(),
            }
        logging.basicConfig(level=logging.INFO)

    def get_key(self, dict_name: str, key: str, place: str = "config.yaml") -> Any:
        try:
            obj: Any = self.config.get(dict_name)
            if obj is None:
                raise ConfigValueError(f"{dict_name} not set in config")
            return obj.get(key)
        except ValueError as e:
            raise ConfigValueError(f"{key} not set in {place}") from e

    def read_yaml_config_file(self, path: str) -> Any:
        """
        Read config from the config.yml file
        """

        stream = open(path, "r", encoding="utf-8")
        content = load(stream, Loader)
        stream.close()

        return content

    def get_yaml_values(self) -> Tuple[int, int, int, int]:
        time_start = self.get_key("config", "time_start_hour") * 60
        time_end = self.get_key("config", "time_end_hour") * 60
        min_duration = self.get_key("config", "min_duration_minutes")
        default_duration = self.get_key("config", "default_duration_minutes")
        return time_start, time_end, min_duration, default_duration

    def get_selenium_values(self) -> Tuple[int, int]:
        window_width = self.get_key("config", "window_width")
        window_height = self.get_key("config", "window_height")
        return window_width, window_height

    def get_cli_values(self) -> Tuple[str, str, int, str]:
        folder = self.get_key("cli", "folder")
        label = self.get_key("cli", "label")
        container_height = self.get_key("cli", "container_height")
        output = self.get_key("cli", "output_file")
        return folder, label, container_height, output
