import os
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Query, Session

from database import get_db
from models import ActionItem, Decision, Meeting, MeetingParticipant, Project, User
from routers.auth import get_current_user
from schemas.meeting import AnalyzeResponse, MeetingCreate, MeetingResponse, MeetingUpdate
from services import ai_service, calendar_service, stt_service

# 이 라우터의 모든 엔드포인트는 로그인이 필요하고,
# 본인 프로젝트에 속한 회의만 접근할 수 있습니다.
router = APIRouter(prefix="/meetings", tags=["meetings"])


def _owned_meetings(db: Session, user: User) -> Query:
    """현재 사용자가 소유한 프로젝트의 회의만 조회하는 쿼리"""
    return (
        db.query(Meeting)
        .join(Project, Meeting.project_id == Project.id)
        .filter(Project.owner_id == user.id)
    )



def _readable_meetings(db: Session, user: User) -> Query:
    """소유하거나 공유받은 프로젝트의 회의 조회"""
    from sqlalchemy import or_
    from models import ProjectMember

    shared_ids = (
        db.query(ProjectMember.project_id)
        .filter(ProjectMember.user_id == user.id)
    )

    return (
        db.query(Meeting)
        .join(Project, Meeting.project_id == Project.id)
        .filter(
            or_(
                Project.owner_id == user.id,
                Project.id.in_(shared_ids),
                Meeting.id.in_(db.query(MeetingParticipant.meeting_id).filter(MeetingParticipant.user_id == user.id))
            )
        )
    )


def _get_meeting_or_404(db: Session, meeting_id: int, user: User) -> Meeting:
    # 남의 회의는 403 이 아니라 404 로 응답해 존재 여부를 노출하지 않습니다.
    meeting = _owned_meetings(db, user).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(404, "회의를 찾을 수 없습니다.")
    return meeting


@router.post("", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
def create_meeting(
    data: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == data.project_id, Project.owner_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(404, "프로젝트를 찾을 수 없습니다.")
    meeting = Meeting(**data.model_dump(exclude={"attendee_ids"}))
    db.add(meeting)
    db.flush()
    attendee_ids = list(dict.fromkeys(data.attendee_ids))
    for user_id in attendee_ids:
        if not db.query(User).filter(User.id == user_id).first():
            db.rollback()
            raise HTTPException(422, "Invalid attendee user ID")
        db.add(MeetingParticipant(meeting_id=meeting.id, user_id=user_id))
    db.commit()
    db.refresh(meeting)
    return meeting


@router.get("", response_model=List[MeetingResponse])
def list_meetings(
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = _readable_meetings(db, current_user)
    if project_id:
        q = q.filter(Meeting.project_id == project_id)
    return q.order_by(Meeting.meeting_date.desc(), Meeting.id.desc()).offset(skip).limit(min(limit, 100)).all()


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = (
        _readable_meetings(db, current_user)
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if not meeting:
        raise HTTPException(404, "회의를 찾을 수 없습니다.")

    return meeting


@router.put("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(
    meeting_id: int,
    data: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = _get_meeting_or_404(db, meeting_id, current_user)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(meeting, k, v)
    db.commit()
    db.refresh(meeting)
    return meeting


@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = _get_meeting_or_404(db, meeting_id, current_user)
    stt_service.delete_audio_file(meeting.audio_path)
    # models.py에 cascade 설정이 없어서 자식 데이터를 먼저 삭제
    db.query(Decision).filter(Decision.meeting_id == meeting.id).delete(synchronize_session=False)
    db.query(ActionItem).filter(ActionItem.meeting_id == meeting.id).delete(synchronize_session=False)
    db.delete(meeting)
    db.commit()


@router.post("/{meeting_id}/audio", response_model=MeetingResponse)
def upload_audio(
    meeting_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """오디오 업로드 → STT 변환 → transcript 저장"""
    meeting = _get_meeting_or_404(db, meeting_id, current_user)

    old_path = meeting.audio_path
    path = stt_service.save_audio_file(file)
    try:
        transcript = stt_service.transcribe_audio(path)
    except Exception:
        stt_service.delete_audio_file(path)
        raise

    stt_service.delete_audio_file(old_path)
    meeting.audio_path = path
    meeting.transcript = transcript
    db.commit()
    db.refresh(meeting)
    return meeting


@router.get("/{meeting_id}/audio")
def get_audio(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """회의 녹음 파일 재생/다운로드 (소유자만 가능)

    녹음 파일은 /uploads 정적 경로로 공개하지 않고 이 엔드포인트로만 제공합니다.
    """
    meeting = _get_meeting_or_404(db, meeting_id, current_user)
    if not meeting.audio_path or not os.path.isfile(meeting.audio_path):
        raise HTTPException(404, "오디오 파일을 찾을 수 없습니다.")
    return FileResponse(meeting.audio_path)


@router.post("/{meeting_id}/analyze", response_model=AnalyzeResponse)
def analyze_meeting(
    meeting_id: int,
    replace: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """전사본 AI 분석 → 요약 저장, 결정사항(Decision)과 액션 아이템(ActionItem) 생성.

    replace=True 이면 기존 결정사항과 '대기(pending)' 상태 액션 아이템만 지우고 다시 만듭니다.
    진행중/완료된 업무는 유지됩니다.
    """
    meeting = _get_meeting_or_404(db, meeting_id, current_user)
    attendees = [a.strip() for a in (meeting.attendees or "").split(",") if a.strip()]

    analysis = ai_service.analyze_meeting(meeting.transcript or "", meeting.title, attendees)

    summary = analysis.summary
    if analysis.key_points:
        summary += "\n\n[핵심 논의]\n" + "\n".join(f"- {p}" for p in analysis.key_points)
    meeting.summary = summary

    if replace:
        db.query(Decision).filter(Decision.meeting_id == meeting.id).delete(synchronize_session=False)
        db.query(ActionItem).filter(
            ActionItem.meeting_id == meeting.id, ActionItem.status == "pending"
        ).delete(synchronize_session=False)

    for content in analysis.decisions:
        db.add(Decision(meeting_id=meeting.id, content=content))

    for item in analysis.action_items:
        due = None
        if item.due_date:
            try:
                due = date.fromisoformat(item.due_date)
            except ValueError:
                due = None
        db.add(ActionItem(
            meeting_id=meeting.id,
            task=item.task,
            assignee_name=((item.assignee_name or "")[:50] or None),
            due_date=due,
            status="pending",
        ))

    db.commit()
    db.refresh(meeting)
    return AnalyzeResponse(meeting=meeting, analysis=analysis)


@router.get("/{meeting_id}/calendar.ics")
def download_calendar(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    meeting = _get_meeting_or_404(db, meeting_id, current_user)
    return Response(
        content=calendar_service.build_meeting_ics(meeting),
        media_type="text/calendar; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="meeting-{meeting.id}.ics"'},
    )
