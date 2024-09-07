from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class UserQueryBaseSchema(BaseModel):
    user_id: Optional[int] = None
    project_id: Optional[int] = None
    program_id: Optional[int] = None
    portfolio_id: Optional[int] = None
    query_text: Optional[str] = None

class UserQueryCreateSchema(UserQueryBaseSchema):
    pass

class UserQueryReadSchema(UserQueryBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    query_id: int

class UserQueryUpdateSchema(UserQueryBaseSchema):
    pass

class ResponseUserQuerySchema(BaseModel):
    code: str
    status: int
    response: str | UserQueryReadSchema = Field(...)

class ListResponseUserQuerySchema(BaseModel):
    code: str
    status: int
    response: List[UserQueryReadSchema] = Field(...)
