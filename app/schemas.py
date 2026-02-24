from datetime import date
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(default="", max_length=5000)
    priority: str = Field(default="MEDIUM")
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=5000)
    priority: str | None = None
    due_date: date | None = None
    status: str | None = None


class CommentCreate(BaseModel):
    author: str = Field(default="Student", max_length=80)
    content: str = Field(min_length=1, max_length=5000)