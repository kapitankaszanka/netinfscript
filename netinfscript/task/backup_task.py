#!/usr/bin/env python3.10
import logging
from pathlib import Path
from netinfscript.utils import save_to_file
from netinfscript.devices.base_device import BaseDevice
from netinfscript.connections.conn_ssh import ConnSSH


class BackupTask:
    def __init__(self, dev: BaseDevice, device_config_store: Path) -> None:
        self.logger = logging.getLogger(f"netscriptbackup.task.backuptask")
        self._dev: BaseDevice = dev
        self._device_config_store: Path = device_config_store

    @property
    def dev(self) -> BaseDevice:
        """Get the device object."""
        return self._dev

    @property
    def device_config_store(self) -> Path:
        """Get path where the config will be stored."""
        return self._device_config_store

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
        ssh_connection = ConnSSH(self.dev, self.dev.get_command_show_config())
        output: str | None = ssh_connection.get_config()

        if output is not None:
            self.logger.debug(f"{self.dev.ip}:Filtering config file.")
            config_string: str = self.dev.config_filternig(output)
            backup_created: bool = self.make_file_operations(config_string)
            if backup_created:
                self.logger.info(f"{self.dev.ip}:Backup created.")
                return True
            else:
                self.logger.warning(f"{self.dev.ip}:Unable to create backup.")
                return False
        else:
            self.logger.warning(f"{self.dev.ip}:Unable to connect to device.")
            return False

    def make_backup_restconf(self) -> bool:
        """Not impemented yet."""
        self.logger.info(f"{self.dev.ip}:Restconf not implemented yet.")
        return False

    def make_file_operations(self, data_to_save: str | dict) -> bool:
        """
        The function is responsible for save
        output to file and make git commit.
        """
        self.logger.debug(
            f"{self.dev.ip}:Saving the configuration to a file."
        )
        file_save: bool = save_to_file(
            self.device_config_store,
            self.dev.ip,
            self.dev.name,
            data_to_save,
        )

        # to do
        git_save: bool = True

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


if __name__ == "__main__":
    pass
