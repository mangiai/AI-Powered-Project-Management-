from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class ReleaseBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None
    StartDate: date
    EndDate: date
    release_lifecycle_id: Optional[int] = None
    product_id: Optional[int] = None

class ReleaseCreateSchema(ReleaseBaseSchema):
    pass

class ReleaseReadSchema(ReleaseBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
class ReleaseUpdateSchema(ReleaseBaseSchema):
    pass

class ResponseReleaseSchema(BaseModel):
    code: str
    status: int
    response: str | ReleaseReadSchema = Field(...)

class ListResponseReleaseSchema(BaseModel):
    code: str
    status: int
    response: List[ReleaseReadSchema] = Field(...)