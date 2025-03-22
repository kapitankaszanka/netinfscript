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

import sys
import logging
from configparser import ConfigParser
from pathlib import Path
from netinfscript.utils import get_and_valid_path


class Config_Load:
    """
    An object that has the necessary functions
    to load config.ini and validate it.
    """

    def __init__(self) -> None:
        self.logger: logging = logging.getLogger("netinfscript.Confgi_Load")
        self._config: ConfigParser = ConfigParser()
        try:
            self._config.read("config.ini")
            self.load_config()
        except Exception as e:
            self.logger.critical(f"Can't read config.ini file. Error: {e}")
            sys.exit(1)

    def _load_devices_path(self) -> None:
        """
        Load the path to the file with device parameters.
        """
        try:
            path_string: str = self._config["Application_Setup"][
                "Devices_Path"
            ]
            self.devices_path: Path | None = get_and_valid_path(path_string)
        except KeyError as e:
            self.logger.critical(
                "Can't load devices database file."
                f"Not allowed atribute: {e}"
            )
            sys.exit(1)
        except Exception as e:
            self.logger.critical(f"Some error ocure: {e}")
            sys.exit(2)

    def _load_configs_path(self) -> None:
        """Load the path to the folder where the backups will be stored."""
        try:
            path_string: str = self._config["Application_Setup"][
                "Configs_Path"
            ]
            self._configs_path: Path | None = get_and_valid_path(path_string)
            if self._configs_path == None:
                self.configs_path = self._create_file(path_string, "dir")
                return
            self.configs_path = self._configs_path
        except KeyError as e:
            self.logger.critical(
                "Loading mandatory parametrs faild. "
                f"Not allowed atribute: {e}"
            )
            sys.exit(1)
        except Exception as e:
            self.logger.critical(f"Some error ocure: {e}")
            sys.exit(2)

    def _load_logging_path(self) -> None:
        """Load the path to the folder where the logs will be stored."""
        try:
            path_string: str = self._config["Logging"]["File_Path"]
            self._logging_path: Path | None = get_and_valid_path(path_string)
            if self._logging_path == None:
                self.logging_path: Path = self._create_file(
                    path_string, "file"
                )
                return
            self.logging_path: Path = self._logging_path
        except KeyError as e:
            self.logger.warning(f"Key error: {e}. Creating default log file.")
            self.logging_path: str = "netinfscript.log"
        except Exception as e:
            self.logger.critical(f"Some error ocure: {e}")
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
                self.logger.warning("Not allowed loggin level.")
                self.logging_level: str = "info"
            else:
                self.logging_level: str = _logging_level
        except KeyError as e:
            self.logging_level: str = "info"
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    def _create_file(self, path_str: str, file_type: str) -> Path:
        """
        The function will create folder or file and return Path object.
        """
        if file_type == "dir":
            try:
                path: Path = Path(path_str)
                path.mkdir(parents=True, exist_ok=True)
                return path
            except Exception as e:
                self.logger.error(
                    f"Can't create folder {path_str}. Error: {e}"
                )
                sys.exit(2)
        elif file_type == "file":
            try:
                path: Path = Path(path_str)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch(exist_ok=True)
                return path
            except Exception as e:
                self.logger.error(f"Can't create file {path_str}. Error: {e}")
                sys.exit(2)
        else:
            self.logger.warning(f"Can't create {path_str}, wrong arguments.")
            sys.exit(2)

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
