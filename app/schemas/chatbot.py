# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional


class QueryRequest(BaseModel):
    question: str
