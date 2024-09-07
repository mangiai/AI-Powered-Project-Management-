from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class MsgBaseSchema(BaseModel):
    chat_id: Optional[int] = None
    content: Optional[str] = None
    msg_type: Optional[int] = None

class MsgCreateSchema(MsgBaseSchema):
    pass

class MsgReadSchema(MsgBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    msg_id: int

class MsgUpdateSchema(MsgBaseSchema):
    pass

class ResponseMsgSchema(BaseModel):
    code: str
    status: int
    response: str | MsgReadSchema = Field(...)

class ListResponseMsgSchema(BaseModel):
    code: str
    status: int
    response: List[MsgReadSchema] = Field(...)
