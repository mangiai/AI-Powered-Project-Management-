from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class GeneratedSqlBaseSchema(BaseModel):
    query_id: Optional[int] = None
    sql_text: Optional[str] = None

class GeneratedSqlCreateSchema(GeneratedSqlBaseSchema):
    pass

class GeneratedSqlReadSchema(GeneratedSqlBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    sql_id: int

class GeneratedSqlUpdateSchema(GeneratedSqlBaseSchema):
    pass

class ResponseGeneratedSqlSchema(BaseModel):
    code: str
    status: int
    response: str | GeneratedSqlReadSchema = Field(...)

class ListResponseGeneratedSqlSchema(BaseModel):
    code: str
    status: int
    response: List[GeneratedSqlReadSchema] = Field(...)
