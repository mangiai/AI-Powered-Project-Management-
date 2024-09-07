from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class BaselineSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None
    completed: bool = Field(alias="is_completed", description="task completed status")
    status: str | None
    priority: str
    progress: float | None
    StartDate: date
    EndDate: date
    cost: float
    phase: str
  

class RequestBaseline(BaselineSchema):
    pass


class ResponseBaseline(BaseModel):
    code: str
    status: int
    response: str | BaselineSchema = Field(...)


class ListResponseBaseline(BaseModel):
    code: str
    status: int
    response: List[BaselineSchema] = Field(...)