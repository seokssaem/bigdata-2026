"""업무(ActionItem, 테이블명 tasks) 스키마"""
from datetime import date, datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

TaskStatus = Literal["pending", "in_progress", "completed"]


class ActionItemCreate(BaseModel):
    meeting_id: Optional[int] = None
    task: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    assignee_name: Optional[str] = Field(None, max_length=50)
    due_date: Optional[date] = None


class ActionItemUpdate(BaseModel):
    task: Optional[str] = Field(None, min_length=1)
    assignee_name: Optional[str] = Field(None, max_length=50)
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None


class ActionItemStatusUpdate(BaseModel):
    status: TaskStatus


class ActionItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: Optional[int] = None
    task: Optional[str] = None
    assignee_name: Optional[str] = None
    status: str
    due_date: Optional[date] = None
    created_at: Optional[datetime] = None
    