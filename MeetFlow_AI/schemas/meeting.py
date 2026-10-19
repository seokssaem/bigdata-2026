from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from schemas.task import ActionItemResponse


class MeetingCreate(BaseModel):
    project_id: int
    title: str = Field(..., min_length=1, max_length=200)
    meeting_date: date
    attendees: Optional[str] = Field(None, max_length=255)  # "홍길동, 김철수" 처럼 쉼표로 구분
    transcript: Optional[str] = None
    attendee_ids: List[int] = Field(default_factory=list)


class MeetingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    meeting_date: Optional[date] = None
    attendees: Optional[str] = Field(None, max_length=255)
    transcript: Optional[str] = None
    summary: Optional[str] = None


class DecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    content: str


class MeetingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    title: str
    meeting_date: date
    attendees: Optional[str] = None
    audio_path: Optional[str] = None
    transcript: Optional[str] = None
    summary: Optional[str] = None
    created_at: Optional[datetime] = None
    decisions: List[DecisionResponse] = []
    action_items: List[ActionItemResponse] = []


# ---- AI 분석 결과 (DB 저장 전 형태) ----
class ActionItemDraft(BaseModel):
    task: str
    assignee_name: Optional[str] = None
    due_date: Optional[str] = None  # YYYY-MM-DD


class MeetingAnalysis(BaseModel):
    summary: str
    key_points: List[str] = []
    decisions: List[str] = []
    action_items: List[ActionItemDraft] = []


class AnalyzeResponse(BaseModel):
    meeting: MeetingResponse
    analysis: MeetingAnalysis