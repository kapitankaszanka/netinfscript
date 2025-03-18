#!/usr/bin/env python3.10
import logging
from pathlib import Path


logger = logging.getLogger("netinfscript.utils")


def get_and_valid_path(path: str) -> Path | None:
    """
    The function check if path or file exist.

    :return: Path or None
    """
    valid_path = Path(path)
    if valid_path.exists():
        return valid_path
    else:
        logger.error(f"{path} doesn't exist.")
        return None


if __name__ == "__main__":
    pass
