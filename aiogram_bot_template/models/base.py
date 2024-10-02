from pydantic import BaseModel, ConfigDict


class FromAttributesModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
