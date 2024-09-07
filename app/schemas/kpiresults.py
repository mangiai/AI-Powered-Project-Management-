from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class KPIResultBaseSchema(BaseModel):
    project_id: Optional[int] = None
    program_id: Optional[int] = None
    portfolio_id: Optional[int] = None
    cost_kpi: Optional[str] = None
    project_kpi: Optional[str] = None
    risk_kpi: Optional[str] = None

class KPIResultCreateSchema(KPIResultBaseSchema):
    pass

class KPIResultReadSchema(KPIResultBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    kpi_id: int

class KPIResultUpdateSchema(KPIResultBaseSchema):
    pass

class ResponseKPIResultSchema(BaseModel):
    code: str
    status: int
    response: str | KPIResultReadSchema = Field(...)

class ListResponseKPIResultSchema(BaseModel):
    code: str
    status: int
    response: List[KPIResultReadSchema] = Field(...)
