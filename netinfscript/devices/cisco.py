#!/usr/bin/env python3.10

"""
Cisco object with all necessary parameters and functions.
"""

import logging
from netinfscript.devices.base_device import BaseDevice
from netinfscript.connections.conn_ssh import ConnSSH


class Cisco(BaseDevice):
    """Cisco device object."""

    def __init__(
        self,
        ip: str,
        port: int,
        name: str,
        vendor: str,
        connection: str,
        username: str,
        password: str,
        privilege_cmd: str,
        privilege_password: str,
        key_file: str,
        passphrase: str,
    ) -> "BaseDevice":
        super().__init__(
            ip,
            port,
            name,
            vendor,
            connection,
            username,
            password,
            privilege_cmd,
            privilege_password,
            key_file,
            passphrase,
        )
        self.logger: logging = logging.getLogger(
            f"netinfscript.devices.Cisco"
        )
        self.logger.debug("Creatad.")
        self.device_type = "cisco_ios"

    def get_command_show_config(self):
        """Returns a command that display the current configuration"""
        self.logger.debug(f"{self.ip}:Returning commands.")
        return "show running-config view full"

    def config_filternig(self, config):
        """Filters config from unnecessary information"""
        self.logger.debug(f"{self.ip}:Configuration filtering.")
        _tmp_config: list = []
        config: str = config.splitlines()
        add_enter: bool = True
        for line in config:
            if "!" in line:
                if add_enter == True:
                    self.logger.debug(f"{self.ip}:Skiping '!'.")
                    _tmp_config.append("")
                    add_enter = False
                continue
            elif "Building configuration" in line:
                self.logger.debug(f"{self.ip}:Skiping line '{line}'.")
                continue
            elif "Current configuration" in line:
                self.logger.debug(f"{self.ip}:Skiping line '{line}'.")
                continue
            elif len(line) == 0:
                self.logger.debug(f"{self.ip}:Skiping empty line for.")
                continue
            else:
                _tmp_config.append(line)
                add_enter: bool = True
        config_to_return: str = "\n".join(_tmp_config)
        return config_to_return


if __name__ == "__main__":
    pass
