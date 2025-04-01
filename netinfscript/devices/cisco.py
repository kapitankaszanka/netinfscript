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


import logging
from netinfscript.devices.base_device import BaseDevice


class Cisco(BaseDevice):
    """Cisco device object."""

    def __init__(
        self,
        ip: str,
        port: int,
        name: str,
        vendor: str,
        connection_type: str,
        username: str,
        password: str,
        privilege_cmd: str,
        privilege_password: str,
        key_file: str,
        passphrase: str,
        priv_level_0: str,
        priv_level_1: str,
        priv_level_2: str,
    ) -> "BaseDevice":
        super().__init__(
            ip,
            port,
            name,
            vendor,
            connection_type,
            username,
            password,
            privilege_cmd,
            privilege_password,
            key_file,
            passphrase,
            priv_level_0,
            priv_level_1,
            priv_level_2,
        )
        self.logger: logging = logging.getLogger(
            f"netinfscript.devices.Cisco"
        )
        self.logger.debug("Creatad.")
        self.device_type = "cisco_ios"

    @property
    def priv_level_0(self) -> str:
        """Get the zero privilidge level."""
        self._priv_level_0: str = ">"
        return self._priv_level_0

    @property
    def priv_level_1(self) -> str:
        """Get the first privilidge level."""
        self._priv_level_1: str = "#"
        return self._priv_level_1

    @property
    def priv_level_2(self) -> str:
        """Get the second privilidge level."""
        self._priv_level_2: str = "#"
        return self._priv_level_2

    @property
    def elevate_priv(self) -> str:
        """Get the command to elevate privilidg level."""
        return "enable"

    @property
    def downgrade_priv_level(self) -> str:
        """Get the command to downgrade privilidge level."""
        return "exit"

    @property
    def cmd_show_config(self):
        """Returns a command that display the current configuration"""
        priv_level: int = 1
        command: str = "show running-config view full"
        self.logger.debug(f"{self.ip}:Returning commands to show config.")
        return priv_level, command

    @property
    def cmd_show_config(self):
        """Returns a command that display the current configuration"""
        priv_level: int = 1
        command: str = "show running-config view full"
        self.logger.debug(f"{self.ip}:Returning commands to show config.")
        return priv_level, command

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
