from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class SprintBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None
    retro: Optional[str] = None
    completed: Optional[bool] = Field(alias="is_completed", description="completed status", default=False)
    StartDate: Optional[date] = None
    EndDate: Optional[date] = None
    
    release_id: Optional[int] = None
    sprint_lifecycle_id: Optional[int] = None
     

class SprintCreateSchema(SprintBaseSchema):
    pass

class SprintReadSchema(SprintBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
class SprintUpdateSchema(SprintBaseSchema):
    pass

class ResponseSprintSchema(BaseModel):
    code: str
    status: int
    response: str | SprintReadSchema = Field(...)

class ListResponseSprintSchema(BaseModel):
    code: str
    status: int
    response: List[SprintReadSchema] = Field(...)