from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class ProgramBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None
    StartDate: date
    EndDate: date
    program_lifecycle_id: Optional[int] = None
    portfolio_id: Optional[int] = None

class ProgramCreateSchema(ProgramBaseSchema):
    pass

class ProgramReadSchema(ProgramBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
class ProgramUpdateSchema(ProgramBaseSchema):
    pass

class ResponseProgramSchema(BaseModel):
    code: str
    status: int
    response: str | ProgramReadSchema = Field(...)

class ListResponseProgramSchema(BaseModel):
    code: str
    status: int
    response: List[ProgramReadSchema] = Field(...)