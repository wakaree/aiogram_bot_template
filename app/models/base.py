from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, PrivateAttr


class PydanticModel(_BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        from_attributes=True,
        populate_by_name=True,
    )


class ActiveRecordModel(PydanticModel):
    __updated: dict[str, Any] = PrivateAttr(default_factory=dict)

    @property
    def model_state(self) -> dict[str, Any]:
        return self.__updated

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self.__updated[name] = value
