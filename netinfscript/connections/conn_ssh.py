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
import asyncio
import asyncssh
from netinfscript.devices.base_device import BaseDevice


class ConnSSH:
    """
    An object responsible for SSH connections and their validation.
    """

    def __init__(
        self, semaphore: asyncio.Semaphore, queue_files: asyncio.Queue
    ) -> None:
        self.logger = logging.getLogger(f"netinfscript.connections.conn_ssh")
        self._semaphore = semaphore
        self._queue_files = queue_files

    @property
    def semaphore(self) -> asyncio.Semaphore:
        """Get sempahore."""
        return self._semaphore

    @property
    def queue_files(self) -> asyncio.Queue:
        """Get queue for file saving."""
        return self._queue_files

    async def get_config(self, dev: BaseDevice) -> str:
        """
        The function responsible for connect to device and get config.

        :param dev: device object
        :return str: outpout or error
        """
        try:
            conn_param = await self.setup_conn_parametrs(dev)
            async with self.semaphore:
                async with asyncssh.connect(**conn_param) as conn:
                    try:
                        self.logger.debug(
                            f"{dev.ip}:Trying connect to device."
                        )
                        result: asyncssh.process.SSHCompletedProcess = (
                            await conn.run(dev.cmd_show_config)
                        )
                        output: list[str] | None = result.stdout.split("\n")
                        self.logger.debug(f"{dev.ip}:Put output to queue.")
                        await self.queue_files.put((dev.name, dev.ip, output))
                    except Exception as e:
                        self.logger.warning(
                            f"{dev.ip}:Problem with connection {e}"
                        )
        except Exception as e:
            print(f"Error Con: {e}")

    async def setup_conn_parametrs(self, dev: BaseDevice) -> dict[str, str]:
        """
        The function is resposible for setingup connection
        parametrs base on what device settings.
        :param dev: BaseDevice object
        :return: connection prametrs
        """
        conn_param: dict[str, str | int] = {
            "host": dev.ip,
            "port": dev.port,
            "username": dev.username,
            "connect_timeout": 60,
        }
        if dev.password != None:
            conn_param["password"] = dev.password
        if dev.key_file != None:
            conn_param["client_keys"] = dev.key_file
        if dev.passphrase != None:
            conn_param["passphrase"] = dev.passphrase
        if dev.key_file != None:
            conn_param["client_keys"] = dev.key_file
        if dev.key_file != None:
            conn_param["client_keys"] = dev.key_file
        return conn_param


if __name__ == "__main__":
    pass
