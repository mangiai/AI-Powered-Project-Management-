from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, ValidationError, root_validator
from datetime import datetime, date

class CostBaseSchema(BaseModel):

    cost_per_hour: Optional[int] = None
    total_hours: Optional[int] = None
    fixed_cost: Optional[int] = None
    actual_hours: Optional[int] = None
    actual_fixed_cost: Optional[int] = None
    
    cost_ftask_id: Optional[int] = None
    cost_user_id: Optional[int] = None
    
    cost_story_id: Optional[int] = None
    location: Optional[int] = None
    
    @root_validator(pre=True)
    def check_cost_combination(cls, values):
        cost_per_hour = values.get('cost_per_hour')
        total_hours = values.get('total_hours')
        fixed_cost = values.get('fixed_cost')
        print(cost_per_hour, total_hours, fixed_cost)
        if fixed_cost and (cost_per_hour or total_hours):
            raise ValueError('Cannot have both fixed_cost and cost_per_hour/total_hours. Choose one.')
        elif not fixed_cost and not (cost_per_hour or total_hours):
            raise ValueError('If not using fixed_cost, both cost_per_hour and total_hours are required.')
        return values

class CostCreateSchema(CostBaseSchema):
    pass

class CostReadSchema(CostBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

class CostUpdateSchema(CostBaseSchema):
    pass

class ResponseCostSchema(BaseModel):
    code: str
    status: int
    response: str | CostReadSchema = Field(...)

class ListResponseCostSchema(BaseModel):
    code: str
    status: int
    response: List[CostReadSchema] = Field(...)

class CostCalculateBaseSchema(BaseModel):
    plannedCost:int
    actualCost:int

class CostCalculateSchema(BaseModel):
    code:str
    status:int
    response: CostCalculateBaseSchema = Field(...)