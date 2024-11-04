#!/usr/bin/env python3.10

from netinfscript.agent.init_system import InitSystem
from netinfscript.option_handler import OptionHandler


def main()-> None:

    InitSystem()
    OptionHandler()


if __name__ == "__main__":
    main()
