from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class StoryBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: str
    typeofstory: Optional[int] = None
    name: str
    iwantto: Optional[str]=None
    solcan: Optional[str] = None
    acceptancecriteria: Optional[str] = None
    priority:Optional[int] = None

    assigned: Optional[int] = Field(alias="assigned_to", description="Assignee id",default=None)
    completed: Optional[bool] = Field(alias="is_completed", description="completed status", default=False)
    
    current_status: Optional[int] = None
    velocityPoints: Optional[int] = None
    sprint: Optional[float] = None
    taskDuration: Optional[int] = None

    resource: Optional[str] = None
    actualResource: Optional[str] = None
    
    actualStartDate: Optional[date] = None
    actualEndDate: Optional[date] = None
    
    plannedStartDate: Optional[date] = None
    plannedEndDate: Optional[date] = None

    sprint_id: Optional[int] = None
    epic_id: Optional[int] = None

class StoryCreateSchema(StoryBaseSchema):
    pass

class StoryReadSchema(StoryBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
class StoryUpdateSchema(StoryBaseSchema):
    pass

class ResponseStorySchema(BaseModel):
    code: str
    status: int
    response: str | StoryReadSchema = Field(...)

class ListResponseStorySchema(BaseModel):
    code: str
    status: int
    response: List[StoryReadSchema] = Field(...)