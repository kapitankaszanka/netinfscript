#!/usr/bin/env python3.10
import logging
import json
import sys
from pathlib import Path
from netinfscript.utils import get_and_valid_path
from netinfscript.devices.base_device import BaseDevice
from netinfscript.devices.cisco import Cisco
from netinfscript.devices.mikrotik import Mikrotik
from netinfscript.devices.juniper import Juniper


class Devices_Load:
    """
    An object that collects all the functions
    needed to create device objects.
    """

    def __init__(self, path: Path) -> None:
        try:
            self.logger: logging = logging.getLogger(
                "netscriptbackup.devices.Devices_Load"
            )
            self.devices_path: Path = path
            self._load_devices_file()
        except Exception as e:
            self.logger.critical(
                f"Error ocure when trying load database. Error: {e}"
            )

    def _load_devices_file(self) -> None:
        """
        This function loads devices from device.json file.
        Loading is based on self.device_path variable.
        """
        try:
            self.logger.debug("Loading basic devices list.")
            with open(self.devices_path, "r") as f:
                _loaded_devices: dict[dict] = json.load(f)
            self.devices_data: dict[dict] = _loaded_devices
            del _loaded_devices
        except FileNotFoundError as e:
            self.logger.critical(f"Loading devices error: {e}")
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            self.logger.critical(f"Loading devices error: {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.critical(f"{e}")
            sys.exit(2)

    def create_devices(self, device: tuple[str, dict]) -> BaseDevice:
        """
        The function is responsible for creating
        device based.
        """
        self.logger.info(f"{device[0]}:Creating device objects...")
        try:
            self.logger.debug(
                f"{device[0]}:Setup device_parametrs to create."
            )
            device_parametrs: dict = {
                "ip": device[0],
                "port": device[1]["port"],
                "name": device[1]["name"],
                "vendor": device[1]["vendor"],
                "connection": device[1]["connection"],
                "username": device[1]["username"],
                "password": device[1]["password"],
                "privilege_cmd": "",
                "privilege_password": None,
                "key_file": None,
                "passphrase": None,
            }
            # setup password and command for enter privilge level
            self.logger.debug(
                f"{device[0]}:Checking additional privilege parametrs."
            )
            if device[1]["privilege"] != None:
                privilege: list[str | None] = device[1]["privilege"]
                # if is list setup command and password to enter
                # privilge level
                if isinstance(privilege, list):
                    if privilege[0] != None:
                        device_parametrs["privilege_cmd"] = privilege[0]
                    # if password is not give setup standard password to entry
                    # privilge level
                    if privilege[1] != None:
                        device_parametrs["privilege_password"] = privilege[1]
                    else:
                        device_parametrs["privilege_password"] = (
                            device_parametrs["password"]
                        )
                else:
                    device_parametrs["privilege_password"] = privilege
            self.logger.debug(
                f"{device[0]}:Checking additional key file parametrs."
            )
            if device[1]["key_file"] != None:
                device_parametrs["key_file"] = get_and_valid_path(
                    device[1]["key_file"]
                )
                device_parametrs["passphrase"] = device[1]["passphrase"]
        except KeyError as e:
            self.logger.warning(f"{device[0]}:KeyError in device file: {e}")
            pass
        except Exception as e:
            self.logger.critical(f"Error ocure {e}")
            sys.exit(2)
        try:
            self.logger.debug(f"{device[0]}:Creating device object.")
            if device[1]["vendor"] == "cisco":
                return Cisco(**device_parametrs)
            elif device[1]["vendor"] == "mikrotik":
                return Mikrotik(**device_parametrs)
            elif device[1]["vendor"] == "juniper":
                return Juniper(**device_parametrs)
            else:
                self.logger.warning(f"{device[0]}:Device is not supported.")
                pass
        except Exception as e:
            self.logger.warning(
                f"{device[0]}:Error when creating device object: {e}"
            )


if __name__ == "__main__":
    pass
