#!/usr/bin/env python3.10
import logging
import sys
from pathlib import Path
from netinfscript.agent.config_load import Config_Load

## dodaj try except do ładownia urzadzen


class InitSystem:
    """
    The class responsible for initialize all nedded functions
    param _devices_path: sets path where app can find devices parametrs
    param _config_path: sets path where backup config will be stored
    param _logging_path: sets path where logs will be stored
    param _logging_level: sets logging level
    """

    def __init__(self) -> None:
        try:
            self._config_loaded = Config_Load()
            ## init function for setup logging
            self._devices_path: Path = self._config_loaded.devices_path
            self._configs_path: Path = self._config_loaded.configs_path
            self._logging_path: Path = self._config_loaded.logging_path
            self._logging_level: Path = self._config_loaded.logging_level
            self.set_logging()
        except Exception as e:
            logging.error(f"Error ocure: {e}")
            sys.exit(1)

    @property
    def devices_path(self) -> Path:
        """Return the path to the devices file."""
        return self._devices_path

    @property
    def configs_path(self) -> Path:
        """Return the path to the configuration storage directory."""
        return self._configs_path

    @property
    def logging_path(self) -> Path:
        """Return the path to the logging directory."""
        return self._logging_path

    def set_logging(self) -> None:
        """
        The function responsible for setting the logging system to do
        """
        logger: logging = logging.getLogger("netinfscript")
        if self._logging_level.lower() == "debug":
            logger.setLevel(logging.DEBUG)
        elif self._logging_level.lower() == "info":
            logger.setLevel(logging.INFO)
        elif self._logging_level.lower() == "warning":
            logger.setLevel(logging.WARNING)
        elif self._logging_level.lower() == "error":
            logger.setLevel(logging.ERROR)
        elif self._logging_level.lower() == "critical":
            logger.setLevel(logging.CRITICAL)
        file_handler = logging.FileHandler(self.logging_path)
        if self._logging_level.lower() == "debug":
            file_handler.setLevel(logging.DEBUG)
        elif self._logging_level.lower() == "info":
            file_handler.setLevel(logging.INFO)
        elif self._logging_level.lower() == "warning":
            file_handler.setLevel(logging.WARNING)
        elif self._logging_level.lower() == "error":
            file_handler.setLevel(logging.ERROR)
        elif self._logging_level.lower() == "critical":
            file_handler.setLevel(logging.CRITICAL)
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger


if __name__ == "__main__":
    pass
