#!/usr/bin/env python3.10
import logging
import argparse
from task.task_handler import task_handler

PARSER_SETUP = {
    "prog": "NetInfScript",
    "description": """
Network Infrastructure Script
Program to creat backup configuration network devices
and manage network devices.
""",
}


class OptionHandler:
    """
    An object that collects functions that manage
    the correct execution of the script.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"netscriptbackup.option_handler")
        option_handler = argparse.ArgumentParser(**PARSER_SETUP)
        option_handler.add_argument(
            "-b",
            "--backup",
            action="start_backup",
            help="The option start creating backups.",
        )


def start_backup(self):
    """
    The fuction that start creating backups.
    """
    self.logger.info(f"Start creating backup for devices.")
    task_handler("backup")


if __name__ == "__main__":
    pass
