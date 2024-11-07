#!/usr/bin/env python3.10

"""
Base device object with all necessary parameters and functions.
"""


class BaseDevice:
    """
    Main device object. Assigns all necessary information.
    Returns appropriate variables when the object's child
    does not support the given module.
    """

    devices_lst = []

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
    ) -> None:
        self._name = name
        self._vendor = vendor
        self._ip = ip
        self._username = username
        self._port = port
        self._connection = connection
        self._passphrase = passphrase
        self._key_file = key_file
        self._password = password
        self._privilege_cmd = privilege_cmd
        self._privilege_password = privilege_password
        # Add device instance to the devices list via a class method.
        BaseDevice.devices_lst.append(self)

    @property
    def name(self) -> str:
        """Get the device's name."""
        return self._name

    @property
    def vendor(self) -> str:
        """Get the device's vendor."""
        return self._vendor

    @property
    def ip(self) -> str:
        """Get the device's IP address."""
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
    def connection(self) -> str:
        """Get the type of connection for the device."""
        return self._connection

    @property
    def passphrase(self) -> str:
        """Get the passphrase for the device's key file."""
        return self._passphrase

    @property
    def key_file(self) -> str:
        """Get the path to the device's key file."""
        return self._key_file

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

    # Class method to add a device to the devices list
    @classmethod
    def add_device(cls, device) -> None:
        """Add a device to the devices list."""
        cls.devices_lst.append(device)

    # Class method to retrieve all devices
    @classmethod
    def get_all_devices(cls) -> list:
        """Return a list of all devices."""
        return cls.devices_lst

    def config_filternig(self, config):
        """
        Support for not supported devices.
        """
        return config


if __name__ == "__main__":
    pass
