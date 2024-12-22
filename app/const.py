from datetime import timezone
from pathlib import Path
from typing import Final

from .enums import Locale

TIMEZONE: Final[timezone] = timezone.utc
DEFAULT_LOCALE: Final[str] = Locale.EN
ROOT_DIR: Final[Path] = Path(__file__).parent.parent
ENV_FILE: Final[Path] = ROOT_DIR / ".env"
ASSETS_SOURCE_DIR: Final[Path] = ROOT_DIR / "assets"
MESSAGES_SOURCE_DIR: Final[Path] = ASSETS_SOURCE_DIR / "messages"
