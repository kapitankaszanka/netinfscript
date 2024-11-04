#!/usr/bin/env python3.10

from devices.base_device import BaseDevice
from .backup_task import BackupTask


def task_handler(exe_func: str):
    if exe_func == "backup":
        for dev in BaseDevice.devices_lst:
            backup = BackupTask(dev)
            backup.make_backup_ssh()


if __name__ == "__main__":
    pass
