#!/usr/bin/env python3.10
import logging
import argparse
from pathlib import Path
from netinfscript.task.task_handler import TaskHandler

PARSER_SETUP: dict[str:str] = {
    "prog": "NetInfScript",
    "description": """
Network Infrastructure Script
Program to creat backup configuration network devices
and manage network devices.
""",
}

PARAMETERS: dict[tuple[str] : dict[str:str]] = {
    ("-b", "--backup"): {
        "action": "store_true",
        "help": "The option start creating backups.",
    }
}


class OptionHandler:
    """
    An object that collects functions that manage
    the correct execution of the script.
    """

    def __init__(
        self, devices_parametrs: Path, devices_config_store: Path
    ) -> None:
        self.logger: logging = logging.getLogger(
            f"netscriptbackup.option_handler"
        )
        self._devices_parametrs: Path = devices_parametrs
        self._devices_config_store: Path = devices_config_store
        self.setup_parser()
        self.task_handler: TaskHandler = TaskHandler(
            self.devices_parametrs, self.devices_config_store
        )
        self.logger.debug("OptionHandler object created.")

    @property
    def devices_parametrs(self) -> Path:
        """Get the initialized variables."""
        return self._devices_parametrs

    @property
    def devices_config_store(self) -> Path:
        """Get the initialized variables."""
        return self._devices_config_store

    def setup_parser(self) -> None:
        """The function setup arguments."""
        self.option_handler: argparse.ArgumentParser = (
            argparse.ArgumentParser(**PARSER_SETUP)
        )
        self.logger.debug("Parsing the arguments")
        for flags, params in PARAMETERS.items():
            self.option_handler.add_argument(*flags, **params)
        self.args = self.option_handler.parse_args()

    def execute_program(self) -> None:
        """The function run tasks based on paramters."""
        self.logger.debug("Parsing the arguments")
        if self.args.backup:
            self.start_backup()

    def start_backup(self) -> None:
        """The fuction that start creating backups."""
        self.logger.info(f"Start creating backup for devices.")
        self.task_handler.exe_func = "backup"
        self.task_handler.task_handler()


if __name__ == "__main__":
    pass
