from typing import Optional

from fastapi import HTTPException
from starlette import status

from app.errors.base import AppError


class HTTPError(HTTPException, AppError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal Server Error"

    def __init__(self, msg: Optional[str] = None) -> None:
        super().__init__(status_code=self.status_code, detail=msg or self.detail)
