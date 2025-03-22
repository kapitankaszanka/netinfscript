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
from pathlib import Path


logger = logging.getLogger("netinfscript.utils")


def get_and_valid_path(path: str) -> Path | None:
    """
    The function check if path or file exist.

    :return: Path or None
    """
    valid_path = Path(path)
    if valid_path.exists():
        return valid_path
    else:
        logger.error(f"{path} doesn't exist.")
        return None


if __name__ == "__main__":
    pass
