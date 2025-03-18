### Config files

#### Script setup
###### Information about where script can find the files, and where it should save it:
- **Devices path** - The path to the file where the script can find information about how to log in to the device, IP addresses, etc. In the future, the ability to encrypt this file will be added. Best stored together with the script files or in a created folder in /etc/. The file will contain passwords and other things needed to connect to the device, so it's worth keeping it secure.
- **Configs path** - The path to the directory where the script will save configuration file.

###### Login level settings. The staging area will be rebuilt in the future:
- **Level** - Login level. Possible choices: debug, info, warning, error, critical. I recommend setting it to 'info' or 'warring'.
- **File path** - File path where logs will be saved
