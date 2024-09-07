from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class BotBaseSchema(BaseModel):
    bot_name: Optional[str] = None
    bot_description: Optional[str] = None

class BotCreateSchema(BotBaseSchema):
    pass

class BotReadSchema(BotBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    bot_id: int

class BotUpdateSchema(BotBaseSchema):
    pass

class ResponseBotSchema(BaseModel):
    code: str
    status: int
    response: str | BotReadSchema = Field(...)

class ListResponseBotSchema(BaseModel):
    code: str
    status: int
    response: List[BotReadSchema] = Field(...)
