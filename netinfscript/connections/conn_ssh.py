#!/usr/bin/env python3.10
"""
SSH connection object with all necesery parametrs and funcitons.
"""

import logging
from netmiko import (
    ConnectHandler,
    NetmikoBaseException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)
from netinfscript.devices.base_device import BaseDevice

"""

                "host": self.ip,
                "username": self.username,
                "port": self.port,
                "device_type": self.device_type,
                "password": self.password,
                "secret": self.privilege_password,
                "key_file": self.key_file,
                "passphrase": self.passphrase,
"""


class ConnSSH:
    """
    An object responsible for SSH connections and their validation.
    """

    def __init__(self, dev: BaseDevice, commands: str | list[str]) -> None:
        self.logger = logging.getLogger(
            f"netscriptbackup.connections.conn_ssh"
        )
        self._ip: str = dev.ip
        self._username: str = dev.username
        self._port: int = dev.port
        self._device_type: str = dev.device_type
        self._password: str = dev.password
        self._passphrase: str = dev.passphrase
        self._key_file: str = dev.key_file
        self._secret: str = dev.privilege_password
        self._mode_cmd: str = dev.privilege_cmd
        if isinstance(commands, list):
            self._commands: list[str] = commands
        elif isinstance(commands, str):
            self._commands: list = list()
            self._commands.append(commands)
        else:
            self.logger.debug(f"{self.ip}:Wrong commands variable.")
            return None

    @property
    def ip(self) -> str:
        """Get the device's name."""
        return self._ip

    @property
    def username(self) -> str:
        """Get the username for the device connection."""
        return self._username

    @property
    def port(self) -> int:
        """Get the port for the device connection."""
        return self._port

    @property
    def device_type(self) -> int:
        """Get the port for the device connection."""
        return self._device_type

    @property
    def passphrase(self) -> str:
        """Get the passphrase for the device's key file."""
        return self._passphrase

    @property
    def key_file(self) -> str:
        """Get the path to the device's key file."""
        return self._key_file

    @property
    def secret(self) -> str:
        """Get the path to the device's key file."""
        return self._secret

    @property
    def password(self) -> str:
        """Get the password for the device connection."""
        return self._password

    @property
    def privilege_cmd(self) -> str:
        """Get the privilege command for device access."""
        return self._privilege_cmd

    @property
    def privilege_password(self) -> str:
        """Get the privilege password for elevated access."""
        return self._privilege_password

    @property
    def commands(self) -> list[str]:
        """Get the privilege password for elevated access."""
        return self._commands

    def _set_privilege(self) -> None:
        """
        This function change privilge level if device support it.

        :param _connection: netmiko connection object.
        """
        self.logger.debug(f"{self.ip}:Check privilege mode.")
        if not self._connection.check_enable_mode():
            self.logger.debug(f"{self.ip}:Change privilege mode.")
            if len(self.mode_cmd) > 0:
                self._connection.enable(cmd=self.mode_cmd)

    def _send_command(self, command: str) -> object:
        """
        This function send command to device.

        :param _connection: netmiko connection object.
        :param command_lst: command to send.
        """
        self.logger.debug(f"{self.ip}:Sending command.")
        output: str = self._connection.send_command(
            command_string=command, read_timeout=60
        )
        return output

    def _send(self) -> str:
        """
        the function decide how send commands.

        :param _connection: netmiko connection object.
        :param command_lst: str or list of command(s) to send.
        """
        stdout_lst = []
        for command in self.commands:
            stdout: str = self._send_command(command)
            stdout_lst.append(stdout)
        output = "".join(stdout_lst)
        return output

    def _get_conection_and_send(self) -> str | bool:
        """
        the function connects to the device. If necessary, determines
        the appropriate level of permissions. It then executes functions
        that send commands.

        :param commands: commands list or string,
        :return: interable netmiko object.
        """
        self.logger.debug(f"{self.ip}:Set connection parametrs.")
        try:
            conn_parametrs = {
                "host": self.ip,
                "username": self.username,
                "port": self.port,
                "device_type": self.device_type,
                "password": self.password,
                "secret": self.secret,
                "key_file": self.key_file,
                "passphrase": self.passphrase,
            }
        except Exception as e:
            self.logger.warning(
                f"{self.ip}:Can't setup connection parametrs."
            )
        try:
            self.logger.info(
                f"{self.ip}:Trying download " "configuration from the device."
            )
            if conn_parametrs["key_file"] != None:
                self.logger.debug(f"{self.ip}:Connecting with public key.")
                with ConnectHandler(
                    **conn_parametrs,
                    use_keys=True,
                    ssh_strict=True,
                    system_host_keys=True,
                ) as self._connection:
                    self.logger.debug(f"{self.ip}:Connection created.")
                    self._set_privilege()
                    output = self._send()
            else:
                self.logger.debug(
                    f"{self.ip}:Attempting " "connect with password."
                )
                with ConnectHandler(
                    **conn_parametrs, ssh_strict=True, system_host_keys=True
                ) as self._connection:
                    self.logger.debug(f"{self.ip}:Connection created.")
                    self._set_privilege()
                    output = self._send()
            self.logger.debug(f"{self.ip}:Connection completend sucessfully.")
            return output
        except NetmikoTimeoutException as e:
            if "known_hosts" in str(e):
                self.logger.warning(
                    f"{self.ip}:Can't connect. Device not found."
                )
                return False
            else:
                self.logger.warning(
                    f"{self.ip}:Can't connect. TCP connection to device failed."
                )
                return False
        except NetmikoBaseException as e:
            self.logger.warning(f"{self.ip}:Can't connect.")
            self.logger.warning(f"{self.ip}:Error {e}")
            return False
        except NetmikoAuthenticationException as e:
            self.logger.warning(f"{self.ip}:Can't connect.")
            self.logger.warning(f"{self.ip}:Error {e}")
            return False
        except ValueError as e:
            if "enable mode" in str(e):
                self.logger.warning(
                    f"{self.ip}:Failed enter enable mode. Check password."
                )
                return False
            else:
                self.logger.warning(f"{self.ip}:Unsuported device type.")
                return False
        except Exception as e:
            self.logger.error(f"{self.ip}:Exceptation - {e}")
            return False

    def get_config(self) -> str:
        """
        The function retrieves the necessary commands
        and returns the device configuration.

        :return: filtered device configuration.
        """
        self.logger.debug(f"{self.ip}:Get command.")
        self.logger.debug(f"{self.ip}:Trying download config.")
        output: str = self._get_conection_and_send()
        print(output)
        if not output:
            self.logger.warning(f"{self.ip}:No output config.")
            return None
        return output


if __name__ == "__main__":
    pass
