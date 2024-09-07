from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class UserLoginSchema(BaseModel):
    email: str
    password: str
    
class UserBaseSchema(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    is_system_admin: Optional[bool] = False  # Assuming default as False
    is_fte: Optional[bool] = False  # Assuming default as False
    is_business_steward: Optional[bool] = False  # Assuming default as False
    is_resource: Optional[bool] = False  # Assuming default as False
    is_onshore: Optional[bool] = False  # Assuming default as False
    access_level: Optional[int] = 1  # Assuming default as 1

class UserCreateSchema(UserBaseSchema):
    pass

class UserReadSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserUpdateSchema(UserBaseSchema):
    pass

class ResponseUserSchema(BaseModel):
    code: str
    status: int
    response: str | UserReadSchema = Field(...)

class ListResponseUserSchema(BaseModel):
    code: str
    status: int
    response: List[UserReadSchema] = Field(...)