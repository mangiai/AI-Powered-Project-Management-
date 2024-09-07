from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class EpicBaseSchema(BaseModel):
    themename: Optional[str] = None

class EpicCreateSchema(EpicBaseSchema):
    pass

class EpicReadSchema(EpicBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
class EpicUpdateSchema(EpicBaseSchema):
    pass

class ResponseEpicSchema(BaseModel):
    code: str
    status: int
    response: str | EpicReadSchema = Field(...)

class ListResponseEpicSchema(BaseModel):
    code: str
    status: int
    response: List[EpicReadSchema] = Field(...)