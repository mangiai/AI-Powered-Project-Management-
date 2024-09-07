from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from schemas.projects import ProjectBaseSchema

class RoadmapBaseSchema(BaseModel):
    name: str
    description: str
    project_id: Optional[int] = None
    program_id: Optional[int] = None
    portfolio_id: Optional[int] = None
    
class RoadmapCreateSchema(RoadmapBaseSchema):
    pass

class RoadmapBaseReadSchema(RoadmapBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    
class RoadmapReadSchema(RoadmapBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    project: Optional[ProjectBaseSchema] = Field(None, alias='proj_roadmap_name')
    is_active: Optional[bool]
    
class RoadmapUpdateSchema(RoadmapBaseSchema):
    name: Optional[str] = None

class ResponseRoadmapBaseSchema(BaseModel):
    code: str
    status: int
    response: str | RoadmapBaseReadSchema = Field(...)

class ResponseRoadmapSchema(BaseModel):
    code: str
    status: int
    response: str | RoadmapReadSchema = Field(...)

class ListResponseRoadmapSchema(BaseModel):
    code: str
    status: int
    response: List[RoadmapReadSchema] = Field(...)