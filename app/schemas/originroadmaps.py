from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class RoadmapSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str

class RequestRoadmap(RoadmapSchema):
    pass


class ResponseRoadmap(BaseModel):
    code: str
    status: int
    response: str | RoadmapSchema = Field(...)


class ListResponseRoadmap(BaseModel):
    code: str
    status: int
    response: List[RoadmapSchema] = Field(...)