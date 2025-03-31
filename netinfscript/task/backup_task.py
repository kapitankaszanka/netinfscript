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
#
import logging
import asyncio
from pathlib import Path
from dulwich import porcelain
from dulwich.repo import Repo
from netinfscript.devices.base_device import BaseDevice
from netinfscript.connections.conn_ssh import ConnSSH


class BackupTask:
    def __init__(
        self, devices: list[BaseDevice], configs_dir_path: Path
    ) -> None:
        self.logger: logging = logging.getLogger(
            f"netinfscript.task.backuptask"
        )
        self._dev_lst: list[BaseDevice] = devices
        self._configs_dir_path: Path = configs_dir_path
        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(100)
        self._queue_files: asyncio.Queue = asyncio.Queue()
        self._ssh_conn: ConnSSH = ConnSSH(self.semaphore, self.queue_files)

    @property
    def dev_lst(self) -> list[BaseDevice]:
        """Get the device object."""
        return self._dev_lst

    @property
    def configs_dir_path(self) -> Path:
        """Get path where the config will be stored."""
        return self._configs_dir_path

    @property
    def config_file_path(self) -> Path:
        """Get path where the config will be stored."""
        return self._config_file_path

    @property
    def semaphore(self) -> asyncio.Semaphore:
        """Get sempahore."""
        return self._semaphore

    @property
    def queue_files(self) -> asyncio.Queue:
        """Get queue for file saving."""
        return self._queue_files

    @property
    def ssh_conn(self) -> ConnSSH:
        """Get object for ssh connections."""
        return self._ssh_conn

    def make_backup_restconf(self) -> bool:
        """
        Not impemented yet.
        """
        self.logger.info(f"{self.dev.ip}:Restconf not implemented yet.")
        return False

    async def make_backup_ssh(self) -> bool:
        """
        The functions is responsible for creating
        the bakup for specific devices.

        :return bool: done or not.
        """
        self.logger.debug("Start save to file queue.")
        asyncio.create_task(self.start_file_operations())
        self.logger.debug("Start ssh connections.")
        await self.start_ssh_conn()

        # send signal to stop queue
        await self.queue_files.put((0xFEFEFEFE, 0xFEFEFEFE, 0xFEFEFEFE))

        return True

    async def start_file_operations(self) -> None:
        """
        The function is stared befeor any connection.
        Is responsible for save output to file.
        Output is from Queue.
        """
        while True:
            await asyncio.sleep(0.1)
            dev_name, dev_ip, output = await self.queue_files.get()
            if dev_name == 0xFEFEFEFE:
                if dev_ip == 0xFEFEFEFE:
                    if output == 0xFEFEFEFE:
                        break
            else:
                config_paths: tuple[Path] = self.setup_config_path(
                    dev_name, dev_ip
                )
                await self.save_to_file(dev_ip, config_paths, output)

    async def start_ssh_conn(self) -> None:
        """
        The function creates corotines for every ssh connection.
        """
        async with asyncio.TaskGroup() as tg:
            for dev in self.dev_lst:
                tg.create_task(self.ssh_conn.get_config(dev))

    def setup_config_path(self, dev_name: str, dev_ip: str) -> tuple[Path]:
        """
        The function is responsible for setting the objects of
        the path in which the configuration will be saved.

        :param dev_name: device name
        :param dev_ip: device ip
        :return tuple: tumple with dir and with file name for speficif device
        """
        if dev_name == None:
            dir_dev_path: Path = self.configs_dir_path / f"{dev_ip}"
            file_dev_path: Path = dir_dev_path / f"{dev_ip}_conf.txt"
        else:
            dir_dev_path: Path = (
                self.configs_dir_path / f"{dev_name}-{dev_ip}"
            )
            file_dev_path: Path = dir_dev_path / f"{dev_ip}_conf.txt"

        return dir_dev_path, file_dev_path

    async def save_to_file(
        self, dev_ip: str, config_paths: tuple[Path], config_string: list[str]
    ) -> bool:
        """
        The function that is responsible for creating and saving
        data to the file.

        :return: bool done or not.
        """
        try:
            self.logger.info(f"{dev_ip}:Saveing the configuration to file.")
            self.logger.debug(f"{dev_ip}:Check if the folder exist.")
            if not config_paths[0].is_dir():
                self.logger.info(
                    f"{dev_ip}:The folder doesn't exist "
                    "or account doesn't have permissions."
                )
                self.logger.info(f"{dev_ip}:Creating a folder.")
                config_paths[0].mkdir()
            try:
                self.logger.debug(f"{dev_ip}:Opening the file.")
                with open(config_paths[1], "w") as f:
                    self.logger.debug(f"{dev_ip}:Writing config.")
                    f.writelines(config_string)
                return True
            except PermissionError:
                self.logger.warning(
                    f"{dev_ip}:The file cannot be opened. Permissions error."
                )
                return False
        except Exception as e:
            self.logger.error(f"{dev_ip}:Error: {e}")
            return False

    async def git_operations(
        self, dev_ip: str, config_paths: tuple[str]
    ) -> bool:
        """
        The function commit changes to git repo.
        """
        try:
            self.logger.debug(f"{dev_ip}:Creating git repo object.")
            repo: Repo = self.git_repo(config_paths[0])
        except:
            self.logger.warning(f"{dev_ip}:Can't creat git repo object.")
            return False

        try:
            self.logger.debug(f"{dev_ip}:Adding file to git repo.")
            self.add_to_git(dev_ip, repo, config_paths[1])
        except Exception as e:
            self.logger.warning(
                f"{dev_ip}:Can't add file to staging. Error: {e}"
            )
            return False
        try:
            status = porcelain.status(repo)

            def commit() -> None:
                self.logger.info(f"{dev_ip}:Commit changes.")
                message: bytes = f"Commit {dev_ip}".encode()
                porcelain.commit(repo, message)

            if len(status.unstaged) != 0:
                print(status.unstaged)
                commit()
            elif (
                len(status.staged["add"]) != 0
                or len(status.staged["delete"]) != 0
                or len(status.staged["modify"]) != 0
            ):
                commit()
            else:
                self.logger.info(f"{dev_ip}:Nothing to commit.")
            return True
        except Exception as e:
            self.logger.warning(
                f"{dev_ip}:Can't commit config file. Error: {e}"
            )
            return False

    def git_repo(self, config_dir_path: str) -> None:
        """
        The funciton creates or opens a repo for work.
        """
        repo_path: Path = config_dir_path / ".git"
        if repo_path.exists():
            return porcelain.open_repo(config_dir_path)
        else:
            return porcelain.init(config_dir_path)

    def add_to_git(
        self, dev_ip: str, repo: Repo, config_file_path: str
    ) -> None:
        """
        The function add to staging file.
        """
        self.logger.debug(f"{dev_ip}:Add config file to git.")
        porcelain.add(repo, config_file_path)


if __name__ == "__main__":
    pass
