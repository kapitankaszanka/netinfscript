#!/usr/bin/env python3.10
import logging
from netinfscript.agent.init_system import InitSystem
from netinfscript.option_handler import OptionHandler


def main() -> None:
    """Start application."""
    try:
        initialized_system = InitSystem()
        option_handler = OptionHandler()
        option_handler.execute_program(initialized_system)
    except Exception as e:
        logging.error(f"Error ocure: {e}")


if __name__ == "__main__":
    main()
