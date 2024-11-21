#!/usr/bin/env python3.10
import logging
from netinfscript.task.git_operations import Git
from netinfscript.utils import save_to_file
from netinfscript.devices.base_device import BaseDevice
from netinfscript.connections.conn_ssh import ConnSSH


class BackupTask:
    def __init__(self, dev: BaseDevice) -> None:
        self.logger = logging.getLogger(f"netscriptbackup.task.backuptask")
        self.dev = dev

    def make_backup(self) -> False:  ## to do
        """To implement, don't work correctly"""
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
        config_string: str | None = ssh_connection.get_config()

        if config_string is not None:
            self.logger.debug(
                f"{self.dev.ip}:Saving the configuration to a file."
            )
            is_done: bool = save_to_file(
                self.backup_files_path,
                self.dev.ip,
                self.dev.name,
                config_string,
            )
            if is_done:
                self.logger.info(
                    f"{self.dev.ip}:Operating on the Git repository."
                )
                _git = Git(self.dev.ip, self.dev.name, self.backup_files_path)
                is_done = _git.git_execute()
                if is_done:
                    self.logger.info(f"{self.dev.ip}:Backup created.")
                    return True
                else:
                    self.logger.warning(
                        f"{self.dev.ip}:Unable to create backup."
                    )
                    return False
            else:
                self.logger.warning(f"{self.dev.ip}:Unable to create backup.")
                return False
        else:
            self.logger.warning(f"{self.dev.ip}:Unable to connect to device.")
            return False

    def make_backup_restconf(self) -> bool:
        self.logger.info(f"{self.dev.ip}:Restconf not implemented yet.")
        return False


if __name__ == "__main__":
    pass
