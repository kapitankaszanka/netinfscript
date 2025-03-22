#!/usr/bin/env python3.10

"""
juniper object with all necessary parameters and functions.
"""

import logging
<<<<<<< HEAD:modules/devices/juniper.py
from devices.base_device import BaseDevice
from connections.conn_ssh import ConnSSH


class Juniper(BaseDevice, ConnSSH):
    """juniper device object."""
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
            passphrase: str
            ) -> "BaseDevice":
=======
from netinfscript.devices.base_device import BaseDevice
from netinfscript.connections.conn_ssh import ConnSSH


class Juniper(BaseDevice):
    """Juniper device object."""

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
>>>>>>> rebuild_v2:netinfscript/devices/juniper.py
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
        self.logger = logging.getLogger(f"netinfscript.devices.juniper")
        self.logger.debug(f"{self.ip}:Creatad.")
        self.device_type = "juniper"

    def get_command_show_config(self):
<<<<<<< HEAD:modules/devices/juniper.py
        """returns a command that display the current configuration"""
=======
        """Returns a command that display the current configuration"""
>>>>>>> rebuild_v2:netinfscript/devices/juniper.py
        self.logger.debug(f"{self.ip}:Returning commands.")
        return "show config | display set"

    def config_filternig(self, config):
<<<<<<< HEAD:modules/devices/juniper.py
        """filters config from unnecessary information"""
=======
        """Filters config from unnecessary information"""
>>>>>>> rebuild_v2:netinfscript/devices/juniper.py
        self.logger.debug(f"{self.ip}:Configuration filtering.")
        _tmp_config: list = []
        config: str = config.splitlines()
        for line in config:
            if "#" in line:
                self.logger.debug(f"{self.ip}:Skiping line '{line}'.")
                continue
            _tmp_config.append(line)
        config_to_return: str = "\n".join(_tmp_config)
        return config_to_return


if __name__ == "__main__":
    pass
