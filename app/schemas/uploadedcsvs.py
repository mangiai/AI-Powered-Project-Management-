from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class UploadedCSVBaseSchema(BaseModel):
    user_id: Optional[int] = None
    project_id: Optional[int] = None
    program_id: Optional[int] = None
    portfolio_id: Optional[int] = None
    file_path: Optional[str] = None

class UploadedCSVCreateSchema(UploadedCSVBaseSchema):
    pass

class UploadedCSVReadSchema(UploadedCSVBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    csv_id: int

class UploadedCSVUpdateSchema(UploadedCSVBaseSchema):
    pass

class ResponseUploadedCSVSchema(BaseModel):
    code: str
    status: int
    response: str | UploadedCSVReadSchema = Field(...)

class ListResponseUploadedCSVSchema(BaseModel):
    code: str
    status: int
    response: List[UploadedCSVReadSchema] = Field(...)
