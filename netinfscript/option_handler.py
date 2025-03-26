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
        self, devices_parametrs: Path, configs_dir_path: Path
    ) -> None:
        self.logger: logging = logging.getLogger(
            f"netinfscript.option_handler"
        )
        self._devices_parametrs: Path = devices_parametrs
        self._configs_dir_path: Path = configs_dir_path
        self.setup_parser()
        self.task_handler: TaskHandler = TaskHandler(
            self.devices_parametrs, self.configs_dir_path
        )
        self.logger.debug("OptionHandler object created.")

    @property
    def devices_parametrs(self) -> Path:
        """Get the initialized variables."""
        return self._devices_parametrs

    @property
    def configs_dir_path(self) -> Path:
        """Get the initialized variables."""
        return self._configs_dir_path

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
        self.task_handler.exec_task()


if __name__ == "__main__":
    pass
