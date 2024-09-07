from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class StewardSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_name: str
    asset_type: str 
    asset_stage: str
    description: str
    calculation_method: str
    calculation_value: float
    sor: bool
    dashboard_name: str
    business_steward_name: str
    it_custodian_name: str
    value_statement: str
    project_rank: int

class RequestSteward(StewardSchema):
    pass


class ResponseSteward(BaseModel):
    code: str
    status: int
    response: str | StewardSchema = Field(...)


class ListResponseSteward(BaseModel):
    code: str
    status: int
    response: List[StewardSchema] = Field(...)