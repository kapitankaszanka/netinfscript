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
import re
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
        )
        self.logger: logging = logging.getLogger(
            f"netinfscript.devices.Cisco"
        )
        self.device_type = "cisco_ios"

    @property
    def prompt_lv0(self) -> str:
        """Get the zero promptilidge level."""
        return r">"

    @property
    def pattern_prompt_lv0(self) -> str:
        """Get the first privilidge level."""
        return re.compile(self.prompt_lv0)

    @property
    def prompt_lv1(self) -> str:
        """Get the zero promptilidge level."""
        return r"#"

    @property
    def pattern_prompt_lv1(self) -> str:
        """Get the first privilidge level."""
        return re.compile(self.prompt_lv1)

    @property
    def elevate_priv_lv(self) -> str:
        """Get the command to elevate privilidg level."""
        return "enable"

    @property
    def downgrade_priv_lv(self) -> str:
        """Get the command to downgrade privilidge level."""
        return "exit"

    @property
    def cmd_show_config(self) -> tuple[int, str]:
        """Returns a command that display the current configuration"""
        priv_lv: int = 1
        command: str = "show running-config"
        self.logger.debug(f"{self.ip}:Returning commands to show config.")
        return priv_lv, command

    def config_filternig(self, config) -> str:
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
