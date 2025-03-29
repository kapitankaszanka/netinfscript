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
import sys
import asyncio
from pathlib import Path
from netinfscript.devices.base_device import BaseDevice
from netinfscript.task.backup_task import BackupTask
from netinfscript.agent.devices_load import Devices_Load


class TaskHandler:
    """
    An object respnsible for manage tasks.
    """

    def __init__(
        self, devices_config_file: Path, configs_dir_path: Path
    ) -> None:
        self.logger: logging = logging.getLogger(f"netinfscript.TaskHandler")
        self._devices_config_file: Path = devices_config_file
        self._configs_dir_path: Path = configs_dir_path
        self._exe_func: None | str = None

    @property
    def devices_config_file(self) -> Path:
        """Get the agent object."""
        return self._devices_config_file

    @property
    def configs_dir_path(self) -> Path:
        """Get the initialized variables."""
        return self._configs_dir_path

    @property
    def exe_func(self) -> str:
        """Get the task that need to be executed."""
        return self._exe_func

    @exe_func.setter
    def exe_func(self, task: str) -> None:
        """Set the task that need to be executed."""
        self._exe_func: str = task

    def exec_task(self) -> None:
        """
        Fuction that will optmalize execution of code with
        multithreading. Also is resposible for load devices from file.
        """
        self.logger.debug(f"Trying load devices from database.")
        # load devices
        try:
            self.device_database_load()
        except Exception as e:
            self.logger.error(f"Can't load devices from database.")
            sys.exit(10)
        # ececute script
        self.execute_task()
        self.logger.info(f"{self.exe_func.capitalize} task is done")

    def device_database_load(self) -> None:
        """
        The function that start creating devices objects,
        and set devices set to list
        """
        _dev_load: Devices_Load = Devices_Load(self.devices_config_file)
        self.devices_by_ssh: set[BaseDevice] = _dev_load.base_devices_set_ssh
        self.devices_by_restconf: set[BaseDevice] = (
            _dev_load.base_devices_set_restconf
        )

    def execute_task(self) -> None:
        """The function that will execute task without multithreading."""
        if self.exe_func == "backup":
            self.logger.debug("Execut backup task.")
            self.devices_backup()

    def devices_backup(self) -> None:
        """The function that execute backup task."""
        self.logger.debug("Execut backup task.")
        if self.devices_by_restconf:
            # not implemented
            backup: BackupTask = BackupTask(
                self.devices_by_restconf, self.configs_dir_path
            )
            backup_done: bool = asyncio.run(backup.make_backup_restconf())
            if backup_done:
                return True
            else:
                return True
        if self.devices_by_ssh:
            backup: BackupTask = BackupTask(
                self.devices_by_ssh, self.configs_dir_path
            )
            backup_done: bool = asyncio.run(backup.make_backup_ssh())
            if backup_done:
                return True
            else:
                return False
        else:
            self.logger.error(
                "Something goes wrong while trying create config backup."
            )


if __name__ == "__main__":
    pass
