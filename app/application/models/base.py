from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class PydanticModel(_BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        from_attributes=True,
        populate_by_name=True,
    )
