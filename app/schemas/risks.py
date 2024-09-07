from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date

class RiskBaseSchema(BaseModel):
    type:str
    name: str
    description: str
    mitigation: Optional[str] = None
    assigned_to: Optional[int] = None
    is_completed: Optional[int]
    risk_impact: Optional[int]
    risk_probablitly: Optional[int]
    DueDate: Optional[date] = None

    risk_proj_id: Optional[int] = None
    risk_prog_id: Optional[int] = None
    risk_port_id: Optional[int] = None
    
class RiskCreateSchema(RiskBaseSchema):
    pass

class RiskReadSchema(RiskBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type:str
    name: str
    description: str
    mitigation: Optional[str] = None
    assigned_to: Optional[int] = None
    is_completed: Optional[int]
    risk_impact: Optional[int]
    risk_probablitly: Optional[int]
    DueDate: Optional[date] = None
    
    risk_proj_id: Optional[int] = None
    risk_prog_id: Optional[int] = None
    risk_port_id: Optional[int] = None
    is_active: Optional[bool]
    
class RiskUpdateSchema(RiskBaseSchema):
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

class ResponseRiskSchema(BaseModel):
    code: str
    status: int
    response: str | RiskReadSchema = Field(...)

class ListResponseRiskSchema(BaseModel):
    code: str
    status: int
    response: List[RiskReadSchema] = Field(...)