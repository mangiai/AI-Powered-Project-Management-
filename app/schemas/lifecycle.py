from typing import List
from pydantic import BaseModel, Field, ConfigDict, UUID4
from datetime import datetime, date


class LifecycleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phase: str
    description: str | None

class RequestLifecycle(LifecycleSchema):
    pass


class ResponseLifecycle(BaseModel):
    code: str
    status: int
    response: str | LifecycleSchema = Field(...)


class ListResponseLifecycle(BaseModel):
    code: str
    status: int
    response: List[LifecycleSchema] = Field(...)