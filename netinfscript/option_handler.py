#!/usr/bin/env python3.10
import logging
import argparse
from netinfscript.task.task_handler import task_handler
from netinfscript.agent.init_system import InitSystem

PARSER_SETUP = {
    "prog": "NetInfScript",
    "description": """
Network Infrastructure Script
Program to creat backup configuration network devices
and manage network devices.
""",
}

PARAMETERS = {
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

    def __init__(self, initialized_system: InitSystem) -> None:
        self.logger = logging.getLogger(f"netscriptbackup.option_handler")
        self._initialized_system = initialized_system
        self.setup_parser()
        self.logger.debug("OptionHandler object created.")

    @property
    def initialized_system(self) -> InitSystem:
        """Get the initialized variables."""
        return self._initialized_system

    def setup_parser(self) -> None:
        self.option_handler = argparse.ArgumentParser(**PARSER_SETUP)
        self.logger.debug("Parsing the arguments")
        for flags, params in PARAMETERS.items():
            self.option_handler.add_argument(*flags, **params)
        self.args = self.option_handler.parse_args()

    def execute_program(self):
        """The function run tasks based on paramters."""
        self.logger.debug("Parsing the arguments")
        if self.args.backup:
            self.start_backup()

    def start_backup(self):
        """
        The fuction that start creating backups.
        """
        self.logger.info(f"Start creating backup for devices.")
        return task_handler(self.initialized_system, "backup")


if __name__ == "__main__":
    pass
