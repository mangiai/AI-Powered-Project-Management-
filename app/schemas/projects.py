from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class ProjectBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str | None
    retro: Optional[str] = None
    completed: Optional[bool] = Field(alias="is_completed", description="completed status", default=False)
    StartDate: Optional[date] = None
    EndDate: Optional[date] = None
    program_id: Optional[int] = None
    project_lifecycle_id: Optional[int] = None
     

class ProjectCreateSchema(ProjectBaseSchema):
    pass

class ProjectReadSchema(ProjectBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
class ProjectUpdateSchema(ProjectBaseSchema):
    pass

class ResponseProjectSchema(BaseModel):
    code: str
    status: int
    response: str | ProjectReadSchema = Field(...)

class ListResponseProjectSchema(BaseModel):
    code: str
    status: int
    response: List[ProjectReadSchema] = Field(...)