from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class FTaskBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    wbs: str
    current_status: int
    Resource: str
    ActualResource: str
    PlannedStartDate: datetime
    PlannedEndDate: datetime
    ActualStartDate: datetime
    ActualEndDate: datetime
    action: Optional[str] = None
    predecessor_successor: Optional[str] = None
    progress: Optional[int] = None

    assigned_to: Optional[int] = None

    proj_id: Optional[int] = None

class FTaskCreateSchema(FTaskBaseSchema):
    pass

class FTaskReadSchema(FTaskBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    wbs: Optional[str] = None
    current_status: Optional[int] = None
    Resource: Optional[str] = None
    ActualResource: Optional[str] = None
    PlannedStartDate: Optional[datetime] = None
    PlannedEndDate: Optional[datetime] = None
    ActualStartDate: Optional[datetime] = None
    ActualEndDate: Optional[datetime] = None


class FTaskUpdateSchema(FTaskBaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    wbs: Optional[str] = None
    current_status: Optional[int] = None
    Resource: Optional[str] = None
    ActualResource: Optional[str] = None
    PlannedEndDate: Optional[datetime] = None
    PlannedStartDate: Optional[datetime] = None
    ActualEndDate: Optional[datetime] = None
    ActualStartDate: Optional[datetime] = None

class ResponseFTaskSchema(BaseModel):
    code: str
    status: int
    response: str | FTaskReadSchema = Field(...)

class ListResponseFTaskSchema(BaseModel):
    code: str
    status: int
    response: List[FTaskReadSchema] = Field(...)