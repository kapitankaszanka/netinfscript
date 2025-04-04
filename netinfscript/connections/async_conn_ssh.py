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


class AsyncConnSSH:
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

    async def get_config(
        self, dev: BaseDevice, command: tuple[int, str]
    ) -> str:
        """
        The function responsible for connect to device and get config.

        :param dev: device object
        :return str: outpout or error
        """
        try:
            conn_param = await self.setup_conn_parametrs(dev)
            async with self.semaphore:
                self.logger.debug(f"{dev.ip}:Trying connect to device.")
                try:
                    async with asyncssh.connect(**conn_param) as conn:
                        prompt_status: bool = await self.check_prompt(
                            conn, dev, command[0]
                        )
                        if not prompt_status:
                            self.logger.warning(
                                f"{dev.ip}:Cannot execute commadn."
                            )
                            return
                        result: asyncssh.process.SSHCompletedProcess = (
                            await conn.run(command[1])
                        )
                        output: list[str] | None = result.stdout.split("\n")
                        self.logger.debug(f"{dev.ip}:Put output to queue.")
                        await self.queue_files.put((dev.name, dev.ip, output))
                except Exception as e:
                    self.logger.warning(
                        f"{dev.ip}:Problem with connection. {e}"
                    )
        except Exception as e:
            self.logger.warning(f"{dev.ip}:Problem with connection. {e}")

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
            "connect_timeout": 30,
        }
        self.logger.debug(
            f"{dev.ip}:Checking if the password exists for the device."
        )
        if dev.password != None:
            conn_param["password"] = dev.password
        self.logger.debug(
            f"{dev.ip}:Checking if the key file exists for the device."
        )
        if dev.key_file != None:
            conn_param["client_keys"] = [dev.key_file]
            conn_param["agent_path"] = None
            self.logger.debug(
                f"{dev.ip}:Checking if the passphrase for "
                "key file exists for the device."
            )
            if dev.passphrase != None:
                conn_param["passphrase"] = dev.passphrase
        return conn_param

    async def check_prompt(
        self,
        conn: asyncssh.connection.SSHClientConnection,
        dev: BaseDevice,
        needed_priv_lv: int,
    ) -> bool:
        """
        Checks the prompt after connecting to the device and elevates
        privileges if the current level is not as required.
        """

        async def get_priv_level() -> str:
            """
            The function get privilidge level.
            """
            self.logger.debug(f"{dev.ip}:Checking privilidged level.")
            shell.stdin.write("\n")
            prompt = await shell.readuntil(
                dev.pattern_prompt_all, datatype=None
            )
            actual_level: int = 0
            if prompt.strip().endswith(dev.prompt_lv0):
                self.logger.debug(f"{dev.ip}:Privilegend level 0.")
            if prompt.strip().endswith(dev.prompt_lv1):
                self.logger.debug(f"{dev.ip}:Privilegend level 1.")
                actual_level: int = 1
            return actual_level

        async def elevate_privilidge(actual_level: int) -> None:
            """
            The function reduces or increases the permissions.
            """
            if actual_level == 0 and needed_priv_lv > actual_level:
                self.logger.debug(f"{dev.ip}:Raising priv level to 1.")
                shell.stdin.writelines(["\n", dev.elevate_priv_lv, "\n"])
                await shell.readuntil(":", datatype=None)
            elif actual_level == 1 and needed_priv_lv > actual_level:
                self.logger.debug(f"{dev.ip}:Downgrading priv level to 0.")
                shell.stdin.writelines(["\n", dev.downgrade_priv_lv, "\n"])

        async def check_priv_level(needed_priv_lv: int, counter: int) -> bool:
            """
            Recursive function responsible for
            setting the appropriate level of privilidge.
            """
            counter += 1
            if counter > 3:
                self.logger.warning(
                    f"{dev.ip}:The level of privileges cannot be raised"
                )
                return False
            actual_level = await get_priv_level()
            if needed_priv_lv == actual_level:
                return True
            else:
                self.logger.debug(
                    f"{dev.ip}:Change privilidge level. Attempt: {counter}"
                )
                await elevate_privilidge(actual_level)
                return await check_priv_level(needed_priv_lv, counter)

        try:
            self.logger.debug(f"{dev.ip}:Start checking prompt.")
            shell = await conn.create_process(term_type="ansi")
            counter: int = 0
            status: bool = await check_priv_level(needed_priv_lv, counter)
            return status
        except Exception as e:
            self.logger.warning(
                f"{dev.ip}:Unable to determine the prompt. {e}"
            )
            return False


if __name__ == "__main__":
    pass
