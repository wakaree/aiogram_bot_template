from __future__ import annotations

import ssl
from types import TracebackType
from typing import Optional

import certifi
from aiohttp import ClientSession, TCPConnector

from utils import mjson


class AiohttpClientMixin:
    """
    ``aiohttp.ClientSession`` factory for API wrappers
    """

    _session: Optional[ClientSession]
    _ssl_context: ssl.SSLContext
    _should_reset_connector: bool

    __slots__ = ("_session", "_ssl_context", "_should_reset_connector")

    def __init__(self) -> None:
        self._session = None
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._should_reset_connector = True

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

    async def get_session(self) -> ClientSession:
        if self._should_reset_connector:
            await self.close()

        if self._session is None or self._session.closed:
            self._session = ClientSession(
                connector=TCPConnector(limit=100, ssl=self._ssl_context),
                json_serialize=mjson.encode,
            )
            self._should_reset_connector = False

        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
