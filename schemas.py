"""
Pydantic request/response schemas for TaskFlow's API.
Author: Jahanzaib Muhammad
"""
from pydantic import BaseModel, Field
from datetime import datetime


class TodoCreatePayload(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Cannot be blank")
    notes: str | None = Field(default="", max_length=500)


class TodoUpdatePayload(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    notes: str | None = Field(default=None, max_length=500)
    done: bool | None = None


class TodoOut(BaseModel):
    id: int
    title: str
    notes: str
    done: bool
    created_at: datetime

    class Config:
        from_attributes = True
