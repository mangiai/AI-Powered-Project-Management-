from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class PortfolioBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None
    StartDate: date
    EndDate: date  

class PortfolioCreateSchema(PortfolioBaseSchema):
    pass

class PortfolioReadSchema(PortfolioBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id:int

class PortfolioUpdateSchema(PortfolioBaseSchema):
    pass

class ResponsePortfolioSchema(BaseModel):
    code: str
    status: int
    response: str | PortfolioReadSchema = Field(...)

class ListResponsePortfolioSchema(BaseModel):
    code: str
    status: int
    response: List[PortfolioReadSchema] = Field(...)