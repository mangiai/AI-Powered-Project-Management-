from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class ProductBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str] = None
    StartDate: Optional[date] = None
    EndDate: Optional[date] = None
    product_lifecycle_id: Optional[int] = None

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductReadSchema(ProductBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id:int

class ProductUpdateSchema(ProductBaseSchema):
    pass

class ResponseProductSchema(BaseModel):
    code: str
    status: int
    response: str | ProductReadSchema = Field(...)

class ListResponseProductSchema(BaseModel):
    code: str
    status: int
    response: List[ProductReadSchema] = Field(...)