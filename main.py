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
from netinfscript.agent.init_system import InitSystem
from netinfscript.option_handler import OptionHandler


def main() -> None:
    """Start application."""
    try:
        initialized_system = InitSystem()
        option_handler = OptionHandler(
            initialized_system.devices_path, initialized_system.configs_path
        )
        option_handler.execute_program()
    except Exception as e:
        logging.error(f"Error ocure: {e}")


if __name__ == "__main__":
    main()
