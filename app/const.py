from datetime import timezone
from pathlib import Path
from typing import Final

from app.enums.locale import Locale

TIMEZONE: Final[timezone] = timezone.utc
DEFAULT_LOCALE: Final[str] = Locale.EN
ROOT_DIR: Final[Path] = Path(__file__).parent.parent
ENV_FILE: Final[Path] = ROOT_DIR / ".env"
ASSETS_SOURCE_DIR: Final[Path] = ROOT_DIR / "assets"
MESSAGES_SOURCE_DIR: Final[Path] = ASSETS_SOURCE_DIR / "messages"

# Time constants
TIME_1M: Final[int] = 60
TIME_5M: Final[int] = TIME_1M * 5
TIME_10M: Final[int] = TIME_1M * 10
