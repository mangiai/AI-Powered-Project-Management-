from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ChatBaseSchema(BaseModel):
    bot_id: Optional[int] = None
    user_id: Optional[int] = None

class ChatCreateSchema(ChatBaseSchema):
    pass

class ChatReadSchema(ChatBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    chat_id: int

class ChatUpdateSchema(ChatBaseSchema):
    pass

class ResponseChatSchema(BaseModel):
    code: str
    status: int
    response: str | ChatReadSchema = Field(...)

class ListResponseChatSchema(BaseModel):
    code: str
    status: int
    response: List[ChatReadSchema] = Field(...)
