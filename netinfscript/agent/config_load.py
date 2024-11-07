#!/usr/bin/env python3.10
import sys
from configparser import ConfigParser
from netinfscript.utils import get_and_valid_path
from pathlib import Path


class Config_Load:
    """
    An object that has the necessary functions
    to load config.ini and validate it.
    """

    def __init__(self) -> None:
        self._config: ConfigParser = ConfigParser()
        try:
            self._config.read("config.ini")
            self.load_config()
        except Exception as e:
            print("Can't read config.ini file...")
            print(e)
            sys.exit(1)

    def _load_devices_path(self) -> None:
        """
        Load the path to the file with device parameters.
        """
        try:
            _tmp_path = self._valid_path_and_create(
                self._config["Application_Setup"]["Devices_Path"],
                "file",
                False,
            )
            if _tmp_path == None:
                print("Path to devices file doesn't exits.")
                sys.exit(1)
            self.devices_path = _tmp_path
        except KeyError as e:
            print(
                "Loading mandatory parametrs failed. "
                f"Not allowed atribute: {e}"
            )
            sys.exit(1)
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    def _load_configs_path(self) -> None:
        """Load the path to the folder where the backups will be stored."""
        try:
            self.config_path = self._valid_path_and_create(
                self._config["Application_Setup"]["Configs_Path"], "dir", True
            )
        except KeyError as e:
            print(
                "Loading mandatory parametrs faild. "
                f"Not allowed atribute: {e}"
            )
            sys.exit(1)
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    def _load_logging_path(self) -> None:
        """Load the path to the folder where the logs will be stored."""
        try:
            self.logging_path = self._valid_path_and_create(
                self._config["Logging"]["File_Path"], "file", True
            )
        except KeyError as e:
            print(f"Key error: {e}. Creating default log file.")
            self.logging_path = "netscriptbackup.log"
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    def _load_logging_level(self) -> None:
        """Load the selected login level."""
        try:
            _logging_lv_lst: list[str] = [
                "debug",
                "info",
                "warning",
                "error",
                "critical",
            ]
            _logging_level: str = self._config["Logging"]["Level"].lower()
            if _logging_level not in _logging_lv_lst:
                print("Not allowed loggin level.")
                sys.exit(1)
            else:
                self.logging_level: str = _logging_level
        except KeyError as e:
            self.logging_level: str = "info"
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    @staticmethod
    def _valid_path_and_create(
        path: str, file_type: str, create: bool
    ) -> Path | None:
        """
        The function verifies the path to the file whether it exists,
        if not, it creates the necessary files and folder.

        :param path: str path to file/folder
        :param file_type: str the type of file that will be eventualy created.
        :param create: bool create or not create

        :return: none | Path Path if file exist or was created.
                        None if file not exist and wasn't created.
        """
        _tmp_path: Path | None = get_and_valid_path(path)
        if _tmp_path == None and create == True:
            if file_type == "dir":
                _tmp_path = Path(path)
                _tmp_path.mkdir(parents=True, exist_ok=True)
            elif file_type == "file":
                _tmp_path = Path(path)
                _tmp_path.parent.mkdir(parents=True, exist_ok=True)
                _tmp_path.touch(exist_ok=True)
            else:
                return None
        return _tmp_path

    def load_config(self) -> None:
        """
        The function is responsible for executing functions that
        load configuration from the 'config.ini' file.
        """
        self._load_devices_path()
        self._load_configs_path()
        self._load_logging_path()
        self._load_logging_level()


if __name__ == "__main__":
    pass
