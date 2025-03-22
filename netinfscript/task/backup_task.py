#!/usr/bin/env python3.10
import logging
from pathlib import Path
from dulwich import porcelain
from dulwich.repo import Repo
from netinfscript.devices.base_device import BaseDevice
from netinfscript.connections.conn_ssh import ConnSSH


class BackupTask:
    def __init__(self, dev: BaseDevice, configs_dir_path: Path) -> None:
        self.logger = logging.getLogger(f"netinfscript.task.backuptask")
        self._dev: BaseDevice = dev
        if self._dev.name == None:
            self._config_dir_path: Path = configs_dir_path / f"{self._dev.ip}"
            self._config_file_path: Path = (
                self._config_dir_path / f"{self._dev.ip}_conf.txt"
            )
        else:
            self._config_dir_path: Path = (
                configs_dir_path / f"{self._dev.name}-{self._dev.ip}"
            )
            self._config_file_path: Path = (
                self._config_dir_path / f"{self._dev.ip}_conf.txt"
            )

    @property
    def dev(self) -> BaseDevice:
        """Get the device object."""
        return self._dev

    @property
    def config_dir_path(self) -> Path:
        """Get path where the config will be stored."""
        return self._config_dir_path

    @property
    def config_file_path(self) -> Path:
        """Get path where the config will be stored."""
        return self._config_file_path

    def make_backup(self) -> bool:  ## to do
        """Some day... Decide how make backup."""
        if "ssh" in self.dev.connection:
            return self.make_backup_ssh()
        elif "restconf" in self.dev.connection:
            return self.make_backup_restconf()
        else:
            self.logger(f"{self.dev.ip}:No connection defined.")
            return False

    def make_backup_ssh(self) -> bool:
        """
        The functions is responsible for creating
        the bakup for specific devices.

        :return bool: done or not.
        """
        self.logger.info(f"{self.dev.ip}:Attempting to create a backup.")
        ssh_connection: ConnSSH = ConnSSH(
            self.dev, self.dev.get_command_show_config()
        )
        output: str | None = ssh_connection.get_config()

        if output is not None:
            self.logger.debug(f"{self.dev.ip}:Filtering config file.")
            self.config_string: str = self.dev.config_filternig(output)
            _backup_created: bool = self.make_file_operations()
            if _backup_created:
                self.logger.info(f"{self.dev.ip}:Backup created.")
                return True
            else:
                self.logger.warning(f"{self.dev.ip}:Unable to create backup.")
                return False
        else:
            self.logger.warning(f"{self.dev.ip}:Unable to connect to device.")
            return False

    def make_backup_restconf(self) -> bool:
        """
        Not impemented yet.
        """
        self.logger.info(f"{self.dev.ip}:Restconf not implemented yet.")
        return False

    def make_file_operations(self) -> bool:
        """
        The function is responsible for save
        output to file and make git commit.
        """
        self.logger.debug(
            f"{self.dev.ip}:Saving the configuration to a file."
        )

        file_save: bool = self.save_to_file()
        git_save: bool = self.commit_to_git()

        if file_save and git_save:
            self.logger.debug(
                f"{self.dev.ip}:File operations completed. Commited to git."
            )
            return True
        elif file_save and not git_save:
            self.logger.warning(
                f"{self.dev.ip}:File operations completed. "
                "Can't commited to git."
            )
            return True
        else:
            self.logger.error(f"{self.dev.ip}:Can't save config to file.")
            return False

    def save_to_file(self) -> bool:
        """
        The function that is responsible for creating and saving
        data to the file.

        :return: bool done or not.
        """
        try:
            self.logger.info(
                f"{self.dev.ip}:Saveing the configuration to file."
            )
            self.logger.debug(f"{self.dev.ip}:Check if the folder exist.")
            if not self.config_dir_path.is_dir():
                self.logger.info(
                    f"{self.dev.ip}:The folder doesn't exist "
                    "or account doesn't have permissions."
                )
                self.logger.info(f"{self.dev.ip}:Creating a folder.")
                self.config_dir_path.mkdir()
            try:
                self.logger.debug(f"{self.dev.ip}:Opening the file.")
                with open(self.config_file_path, "w") as f:
                    self.logger.debug(f"{self.dev.ip}:Writing config.")
                    f.writelines(self.config_string)
                return True
            except PermissionError:
                self.logger.warning(
                    f"{self.dev.ip}:The file cannot be opened. Permissions error."
                )
                return False
        except Exception as e:
            self.logger.error(f"{self.dev.ip}:Error: {e}")
            return False

    def git_repo(self) -> None:
        """
        The funciton creates or opens a repo for work.
        """
        repo_path = self.config_dir_path / ".git"
        if repo_path.exists():
            self.git_repo: Repo = porcelain.open_repo(self.config_dir_path)
        else:
            self.git_repo: Repo = porcelain.init(self.config_dir_path)

    def add_to_git(self) -> None:
        """
        The function add to staging file.
        """
        porcelain.add(self.git_repo, self.config_file_path)

    def commit_to_git(self) -> bool:
        """
        The function commit changes to git repo.
        """
        try:
            self.logger.debug(f"{self.dev.ip}:Creating git repo object.")
            self.git_repo()
        except:
            self.logger.warning(f"{self.dev.ip}:Can't creat git repo object.")
            return False

        try:
            self.logger.debug(f"{self.dev.ip}:Adding file to git repo.")
            self.add_to_git()
        except Exception as e:
            self.logger.warning(
                f"{self.dev.ip}:Can't add file to staging. Error: {e}"
            )
            return False
        try:
            status = porcelain.status(self.git_repo)

            def commit():
                self.logger.debug(f"{self.dev.ip}:Commit changes.")
                message: bytes = (
                    f"Commit {self.dev.name}-{self.dev.ip}".encode()
                )
                porcelain.commit(self.git_repo, message)

            if len(status.unstaged) != 0:
                commit()
            elif all(len(v) == 0 for v in status.staged.values()):
                commit()
            else:
                self.logger.debug(f"{self.dev.ip}:Nothing to commit.")
            return True
        except Exception as e:
            self.logger.warning(
                f"{self.dev.ip}:Can't commit config file. Error: {e}"
            )
            return False


if __name__ == "__main__":
    pass
