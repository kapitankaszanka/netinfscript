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


class BaseDevice:
    """
    Main device object. Assigns all necessary information.
    Returns appropriate variables when the object's child
    does not support the given module.
    """

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
    ) -> None:
        self._name = name
        self._vendor = vendor
        self._ip = ip
        self._username = username
        self._port = port
        self._connection_type = connection_type
        self._passphrase = passphrase
        self._key_file = key_file
        self._password = password
        self._privilege_cmd = privilege_cmd
        self._privilege_password = privilege_password

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
    def connection_type(self) -> str:
        """Get the type of connection_type for the device."""
        return self._connection_type

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

    @property
    def cmd_show_config(self) -> str:
        """Support for not supported devices."""
        self.logger.debug(f"{self.ip}:Returning commands.")
        return "show config"

    @property
    def priv_level_0(self) -> str:
        """Get the zero privilidge level."""
        return ""

    @property
    def priv_level_1(self) -> str:
        """Get the first privilidge level."""
        return ""

    @property
    def elevate_priv(self) -> str:
        """Get the command to elevate privilidg level."""
        return ""

    @property
    def downgrade_priv_level(self) -> str:
        """Get the command to downgrade privilidge level."""
        return ""

    def config_filternig(self, config):
        """Support for not supported devices."""
        return config


if __name__ == "__main__":
    pass
