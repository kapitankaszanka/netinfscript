#!/usr/bin/env python3
#
# Copyright (C) 2025 Mateusz Krupczyński
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You should have received a copy of the licenses; if not, see
# <http://www.gnu.org/licenses/> for a copy of the GNU General Public License
# License, Version 3.0.

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
                "netinfscript.devices.Devices_Load"
            )
            self._devices_path: Path = path
            self._load_devices_file()
            self._base_devices_set_ssh: set[BaseDevice] = set()
            self._base_devices_set_restconf: set[BaseDevice] = set()
            for device in self.devices_data.items():
                if "ssh" in device[1]["connection_type"]:
                    _tmp_base_dev: BaseDevice = self.create_devices(device)
                    self._base_devices_set_ssh.add(_tmp_base_dev)
                if "restconf" in device[1]["connection_type"]:
                    _tmp_base_dev: BaseDevice = self.create_devices(device)
                    self._base_devices_set_restconf.add(_tmp_base_dev)
        except Exception as e:
            self.logger.critical(
                f"Error ocure when trying load database. Error: {e}"
            )

    @property
    def devices_path(self) -> Path:
        """Get devices path."""
        return self._devices_path

    @property
    def base_devices_set_ssh(self) -> set[BaseDevice]:
        """Get devices list with ssh connection."""
        return self._base_devices_set_ssh

    @property
    def base_devices_set_restconf(self) -> set[BaseDevice]:
        """Get devices list with restconf connection."""
        return self._base_devices_set_restconf

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
        device object.
        """
        self.logger.debug(f"{device[0]}:Creating device objects...")
        try:
            self.logger.debug(
                f"{device[0]}:Setup device_parametrs to create."
            )
            device_parametrs: dict = {
                "ip": device[0],
                "port": 22,
                "name": "",
                "vendor": device[1]["vendor"],
                "connection_type": device[1]["connection_type"],
                "username": device[1]["username"],
                "password": None,
                "privilege_cmd": None,
                "privilege_password": None,
                "key_file": None,
                "passphrase": None,
            }
            # setup password and command for enter privilge level
            self.logger.debug(f"{device[0]}:Check if port exist.")
            if "port" in device[1].keys():
                if isinstance(device[1]["port"], int):
                    device_parametrs["port"] = device[1]["port"]
            self.logger.debug(f"{device[0]}:Check if password exist.")
            if "password" in device[1].keys():
                if isinstance(device[1]["password"], str):
                    device_parametrs["password"] = device[1]["password"]
            self.logger.debug(f"{device[0]}:Check if name exist.")
            if "name" in device[1].keys():
                if isinstance(device[1]["name"], str):
                    device_parametrs["name"] = device[1]["name"]
            self.logger.debug(f"{device[0]}:Check if privilege exist.")
            if "privilege" in device[1].keys():
                if device[1]["privilege"] != None:
                    privilege: list[str | None] | None = device[1][
                        "privilege"
                    ]
                    if isinstance(privilege, list):
                        # if is list, setup command and password to enter
                        # privilge level
                        if privilege[0] != None:
                            device_parametrs["privilege_cmd"] = privilege[0]
                        # if password is not give setup standard
                        # password to entry privilge level
                        if privilege[1] != None:
                            device_parametrs["privilege_password"] = (
                                privilege[1]
                            )
                        else:
                            device_parametrs["privilege_password"] = (
                                device_parametrs["password"]
                            )
                    else:
                        device_parametrs["privilege_password"] = privilege
            self.logger.debug(f"{device[0]}:Check if key file exist.")
            _key_file_exist: bool = False
            if "key_file" in device[1].keys():
                _key_file_exist: bool = True
                if isinstance(device[1]["key_file"], str):
                    if device[1]["key_file"] != None:
                        device_parametrs["key_file"] = get_and_valid_path(
                            device[1]["key_file"]
                        )
            self.logger.debug(f"{device[0]}:Check if passphrase exist.")
            if _key_file_exist:
                if "passphrase" in device[1].keys():
                    if isinstance(device[1]["passphrase"], str):
                        device_parametrs["passphrase"] = device[1][
                            "passphrase"
                        ]
        except KeyError as e:
            self.logger.warning(f"{device[0]}:KeyError in device file: {e}")
            pass
        except Exception as e:
            self.logger.critical(f"Error ocure {e}")
            sys.exit(2)
        # creating objects
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
