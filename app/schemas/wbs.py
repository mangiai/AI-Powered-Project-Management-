from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class WBSSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None
  

class RequestWBS(WBSSchema):
    pass


class ResponseWBS(BaseModel):
    code: str
    status: int
    response: str | WBSSchema = Field(...)


class ListResponseWBS(BaseModel):
    code: str
    status: int
    response: List[WBSSchema] = Field(...)