from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query as SAQuery

from database import get_db
from models import ActionItem, Meeting, Project, ProjectMember, User
from routers.auth import get_current_user, require_login_page
from schemas.task import (ActionItemResponse,
                          ActionItemStatusUpdate, ActionItemUpdate)
from services import calendar_service

# templates 객체 정의 (경로는 프로젝트 구조에 맞게 수정)
templates = Jinja2Templates(directory="templates")

# 이 라우터의 JSON API 는 모두 로그인이 필요하고,
# 본인 프로젝트의 회의에 속한 업무만 접근할 수 있습니다.
router = APIRouter(prefix="/tasks", tags=["tasks"])


# ------------------------------------------------------------
# 소유자 범위 쿼리 헬퍼
# ------------------------------------------------------------
def _owned_meetings(db: Session, user: User) -> SAQuery:
    return (
        db.query(Meeting)
        .join(Project, Meeting.project_id == Project.id)
        .filter(Project.owner_id == user.id)
    )


def _readable_meetings(db: Session, user: User) -> SAQuery:

    """본인이 소유하거나 공유받은 프로젝트의 회의 조회"""

    from sqlalchemy import or_



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

                Project.id.in_(shared_ids)

            )

        )

    )





def _owned_tasks(db: Session, user: User) -> SAQuery:
    """내 프로젝트 → 내 회의에 속한 업무만 (Meeting 이 조인되어 있음)"""
    return (
        db.query(ActionItem)
        .join(Meeting, ActionItem.meeting_id == Meeting.id)
        .join(Project, Meeting.project_id == Project.id)
        .filter(Project.owner_id == user.id)
    )




def _readable_tasks(db: Session, user: User) -> SAQuery:

    """소유하거나 공유받은 프로젝트의 업무 조회"""

    from models import ProjectMember

    from sqlalchemy import or_



    shared_ids = (

        db.query(ProjectMember.project_id)

        .filter(ProjectMember.user_id == user.id)

    )



    return (

        db.query(ActionItem)

        .join(Meeting, ActionItem.meeting_id == Meeting.id)

        .join(Project, Meeting.project_id == Project.id)

        .filter(

            or_(

                Project.owner_id == user.id,

                Project.id.in_(shared_ids)

            )

        )

    )





def _get_item_or_404(db: Session, task_id: int, user: User) -> ActionItem:
    # 남의 업무는 403 이 아니라 404 로 응답해 존재 여부를 노출하지 않습니다.
    item = _owned_tasks(db, user).filter(ActionItem.id == task_id).first()
    if not item:
        raise HTTPException(404, "업무를 찾을 수 없습니다.")
    return item


def _filtered_query(db: Session, user: User, project_id, meeting_id, assignee_name, status_filter, overdue):
    q = _readable_tasks(db, user)
    if project_id:
        q = q.filter(Meeting.project_id == project_id)
    if meeting_id:
        q = q.filter(ActionItem.meeting_id == meeting_id)
    if assignee_name:
        q = q.filter(ActionItem.assignee_name == assignee_name)
    if status_filter:
        q = q.filter(ActionItem.status == status_filter)
    if overdue:
        q = q.filter(ActionItem.due_date < date.today(), ActionItem.status != "completed")
    return q


# ------------------------------------------------------------
# 고정 경로 (반드시 "/{task_id}" 보다 위에 선언)
# ------------------------------------------------------------
@router.post("", response_model=ActionItemResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        data = await request.json()
    except Exception:
        data = dict(await request.form())

    # 1. 업무명 및 필드값 추출
    task_text = data.get("task") or data.get("title") or data.get("content") or "신규 업무"
    assignee_name = data.get("assignee_name") or None
    due_date = data.get("due_date") or None

    # 2. meeting_id 처리 (내 회의만 허용)
    meeting_id = data.get("meeting_id")
    valid_meeting = None
    if meeting_id and str(meeting_id).isdigit():
        valid_meeting = (
            _owned_meetings(db, current_user)
            .filter(Meeting.id == int(meeting_id))
            .first()
        )

    if not valid_meeting:
        # 유효한 회의가 지정되지 않으면 내 첫 번째 회의에 연결
        valid_meeting = _owned_meetings(db, current_user).order_by(Meeting.id).first()

    if not valid_meeting:
        raise HTTPException(400, "업무를 등록하려면 먼저 회의를 만들어야 합니다.")

    # 3. DB 저장
    item = ActionItem(
        meeting_id=valid_meeting.id,
        task=task_text,
        assignee_name=assignee_name,
        due_date=due_date,
        status="pending"
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    # 4. Form 제출 시 JSON 응답 대신 업무 화면으로 리다이렉트
    content_type = request.headers.get("content-type", "")
    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        return RedirectResponse(url="/tasks/calendar-view", status_code=status.HTTP_303_SEE_OTHER)

    return item


@router.get("/dashboard")
def get_dashboard_data(
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. 총 회의 수 (내 회의만)
    meetings_query = _readable_meetings(db, current_user)
    if project_id:
        meetings_query = meetings_query.filter(Meeting.project_id == project_id)
    total_meetings = meetings_query.count()

    # 2. 업무 현황 집계 (내 업무만)
    tasks_query = _filtered_query(db, current_user, project_id, None, None, None, False)
    all_tasks = tasks_query.all()

    completed = 0
    in_progress = 0
    pending = 0
    delayed = 0
    urgent = 0

    today = date.today()

    for t in all_tasks:
        # 업무 제목(task 또는 content) 및 상태 추출
        title = str(getattr(t, 'task', '') or getattr(t, 'content', '') or getattr(t, 'title', '') or '')
        raw_status = str(t.status.value if hasattr(t.status, 'value') else t.status or '').lower()

        # 1. 제목에 '완료'가 있거나 status가 completed이면 완료
        if '완료' in title or raw_status == "completed":
            completed += 1
        # 2. 지연 처리 (마감일이 오늘 이전인 경우)
        elif t.due_date and t.due_date < today:
            delayed += 1
        # 3. 완료/지연이 아닌 건은 '진행중'으로 처리 (업무·일정 페이지 기준과 일치)
        else:
            in_progress += 1

        # 긴급(마감 임박) 카운트
        if '완료' not in title and raw_status != "completed":
            if t.due_date and (t.due_date - today).days <= 1:
                urgent += 1

    return {
        "total_meetings": total_meetings,
        "tasks": {
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "delayed": delayed,
            "urgent": urgent
        }
    }


@router.get("", response_model=List[ActionItemResponse])
def list_tasks(
    project_id: Optional[int] = None,
    meeting_id: Optional[int] = None,
    assignee_name: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    overdue: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = _filtered_query(db, current_user, project_id, meeting_id, assignee_name, status_filter, overdue)
    return q.order_by(ActionItem.due_date.asc().nulls_last(), ActionItem.id.desc()).offset(skip).limit(min(limit, 200)).all()


@router.get("/calendar.ics")
def tasks_calendar(
    project_id: Optional[int] = None,
    assignee_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = _filtered_query(db, current_user, project_id, None, assignee_name, None, False)
    q = q.filter(ActionItem.due_date.isnot(None), ActionItem.status != "completed")
    return Response(
        content=calendar_service.build_action_items_ics(q.all()),
        media_type="text/calendar; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="tasks.ics"'},
    )


@router.get("/calendar")
def get_calendar_tasks(
    project_id: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """캘린더 화면에서 월별/프로젝트별 업무 목록을 안전하게 조회합니다."""
    try:
        # 내 업무 + 회의 제목 (Meeting 은 _owned_tasks 에서 이미 조인됨)
        tasks = (
            _readable_tasks(db, current_user)
            .add_columns(Meeting.title.label("meeting_title"))
            .filter(ActionItem.due_date.isnot(None))
            .all()
        )

        result = []
        for t, meeting_title in tasks:
            # content 또는 task 속성 안전 추출
            title_text = getattr(t, 'content', None) or getattr(t, 'task', None) or "업무"

            result.append({
                "id": t.id,
                "title": title_text,
                "due_date": str(t.due_date) if t.due_date else None,
                "status": t.status.value if hasattr(t.status, 'value') else str(t.status),
                "assignee_name": t.assignee_name or "미정",
                "meeting_title": meeting_title or "일반 업무",
                "meeting_id": t.meeting_id
            })

        return result
    except Exception as e:
        print(f"[ERROR] calendar fetch failed: {e}")
        return []


@router.get("/calendar-view")
def calendar_view_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_login_page),
):
    # 1. 내 회의 중 가장 최근 등록된 회의
    latest_meeting = (

        db.query(Meeting)

        .join(Project, Meeting.project_id == Project.id)

        .filter(

            (Project.owner_id == current_user.id)

            | Project.id.in_(

                db.query(ProjectMember.project_id)

                .filter(ProjectMember.user_id == current_user.id)

            )

        )

        .order_by(Meeting.id.desc())

        .first()

    )

    # 2. 해당 회의의 액션 아이템 수 계산
    task_count = 0
    if latest_meeting:
        task_count = (
            _readable_tasks(db, current_user)
            .filter(ActionItem.meeting_id == latest_meeting.id)
            .count()
        )

    # 3. 내 업무 목록 조회
    tasks = _readable_tasks(db, current_user).all()

    # 4. 템플릿으로 전달
    return templates.TemplateResponse(request, "calendar.html", {
        "request": request,
        "user": current_user,
        "latest_meeting": latest_meeting,
        "task_count": task_count,
        "tasks": tasks,
        "active_tab": "calendar"
    })


@router.get("/latest-meeting-info")
def get_latest_meeting_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    latest_meeting = (

        db.query(Meeting)

        .join(Project, Meeting.project_id == Project.id)

        .filter(

            (Project.owner_id == current_user.id)

            |

            Project.id.in_(

                db.query(ProjectMember.project_id)

                .filter(ProjectMember.user_id == current_user.id)

            )

        )

    ).order_by(Meeting.id.desc()).first()

    if not latest_meeting:
        return {"title": None, "task_count": 0}

    task_count = (
        _readable_tasks(db, current_user)
        .filter(ActionItem.meeting_id == latest_meeting.id)
        .count()
    )

    return {
        "title": latest_meeting.title,
        "task_count": task_count
    }


# ------------------------------------------------------------
# 개별 업무 ("/{task_id}")
# ------------------------------------------------------------
@router.get("/{task_id}", response_model=ActionItemResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (

        _readable_tasks(db, current_user)

        .filter(ActionItem.id == task_id)

        .first()

    )



    if not item:

        raise HTTPException(404, "업무를 찾을 수 없습니다.")



    return item


@router.put("/{task_id}", response_model=ActionItemResponse)
def update_task(
    task_id: int,
    data: ActionItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = _get_item_or_404(db, task_id, current_user)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{task_id}/status", response_model=ActionItemResponse)
def update_task_status(
    task_id: int,
    data: ActionItemStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = _get_item_or_404(db, task_id, current_user)
    item.status = data.status
    db.commit()
    db.refresh(item)
    return item


@router.post("/{task_id}/toggle", response_model=ActionItemResponse)
def toggle_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """완료 ↔ 대기 전환 (캘린더/대시보드의 체크 버튼용)"""
    item = _get_item_or_404(db, task_id, current_user)
    item.status = "pending" if item.status == "completed" else "completed"
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = _get_item_or_404(db, task_id, current_user)
    db.delete(item)
    db.commit()
