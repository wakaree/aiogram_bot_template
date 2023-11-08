from __future__ import annotations

import logging
import ssl
from types import TracebackType
from typing import Optional

import certifi
from aiohttp import ClientSession, TCPConnector

from utils import mjson

log = logging.getLogger(__name__)


class AiohttpClientMixin:
    _session: Optional[ClientSession]
    _ssl_context: ssl.SSLContext

    def __init__(self) -> None:
        self._session = None
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())

    async def __aenter__(self) -> AiohttpClientMixin:
        await self.get_session()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def get_new_session(self) -> ClientSession:
        return ClientSession(
            connector=TCPConnector(limit=100, ssl=self._ssl_context),
            json_serialize=mjson.encode,
        )

    async def get_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = await self.get_new_session()

        if not self._session._loop.is_running():  # noqa: SLF001
            await self._session.close()
            self._session = await self.get_new_session()

        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
