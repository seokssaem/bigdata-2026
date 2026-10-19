from datetime import date

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import get_db
from routers.auth import require_login_page

router = APIRouter(prefix="/views", tags=["views"])
templates = Jinja2Templates(directory="templates")


# 로그인 페이지
@router.get("/login")
def login_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"active_tab": "login"}
    )


# 회원가입 페이지
@router.get("/register")
def register_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"active_tab": "login"}
    )


# 계정 관리 페이지
@router.get("/account")
def account_view(
    request: Request,
    user: models.User = Depends(require_login_page)
):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"active_tab": "dashboard", "user": user, "current_user": user}
    )


# =========================================================
# 1. 대시보드
# =========================================================
@router.get("/dashboard")
def dashboard_view(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_login_page)
):
    # 회의 목록 조회
    try:
        meetings = (
            db.query(models.Meeting)
            .join(models.Project)
            .filter(

                (models.Project.owner_id == current_user.id)

                |

                models.Project.id.in_(

                    db.query(models.ProjectMember.project_id)

                    .filter(

                        models.ProjectMember.user_id == current_user.id

                    )

                )
                |
                models.Meeting.id.in_(
                    db.query(models.MeetingParticipant.meeting_id)
                    .filter(models.MeetingParticipant.user_id == current_user.id)
                )

            )
            .order_by(models.Meeting.id.desc())
            .all()
        )
    except Exception:
        meetings = []

    # 긴급/지연/마감임박 ActionItem 추출
    today = date.today()
    urgent_action_items = []
    try:
        all_tasks = (
            db.query(models.ActionItem)
            .join(models.Meeting)
            .join(models.Project)
            .filter(models.Project.owner_id == current_user.id)
            .all()
        )
        for t in all_tasks:
            title = str(getattr(t, 'task', '') or getattr(t, 'content', '') or getattr(t, 'title', '') or '')
            raw_status = str(t.status.value if hasattr(t.status, 'value') else t.status or '').lower()

            # 완료되지 않은 업무 중 지연 및 마감임박(2일 이내) 건 추출
            if '완료' not in title and raw_status != 'completed':
                if t.due_date:
                    diff = (t.due_date - today).days
                    if diff < 0:
                        t.d_day = f"D+{abs(diff)} (지연)"
                        urgent_action_items.append(t)
                    elif diff <= 2:
                        t.d_day = "오늘마감!" if diff == 0 else f"D-{diff}"
                        urgent_action_items.append(t)
    except Exception as e:
        print(f"[ERROR] urgent_action_items fetch failed: {e}")

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "active_tab": "dashboard",
            "meetings": meetings,
            "user": current_user,
            "current_user": current_user,
            "urgent_action_items": urgent_action_items
        }
    )


# 2. 회의록 목록
@router.get("/meetings")
def meetings_view(
    request: Request,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_login_page)
):
    try:
        meetings = (
            db.query(models.Meeting)
            .join(models.Project)
            .filter(

                (models.Project.owner_id == user.id)

                |

                models.Project.id.in_(

                    db.query(models.ProjectMember.project_id)

                    .filter(models.ProjectMember.user_id == user.id)

                )
                |
                models.Meeting.id.in_(
                    db.query(models.MeetingParticipant.meeting_id)
                    .filter(models.MeetingParticipant.user_id == user.id)
                )

            )
            .order_by(models.Meeting.id.desc())
            .all()
        )
    except Exception:
        meetings = []

    return templates.TemplateResponse(
        request=request,
        name="meetings.html",
        context={"active_tab": "meetings", "meetings": meetings, "user": user}
    )


# 3. 새 회의 등록
@router.get("/meetings/new")
def new_meeting_view(
    request: Request,
    user: models.User = Depends(require_login_page)
):
    return templates.TemplateResponse(
        request=request,
        name="new_meeting.html",
        context={"active_tab": "new_meeting", "user": user}
    )


# 4. 캘린더/업무 일정
@router.get("/calendar")
def calendar_view(
    request: Request,
    user: models.User = Depends(require_login_page)
):
    return templates.TemplateResponse(
        request=request,
        name="calendar.html",
        context={"active_tab": "calendar", "user": user}
    )


# 5. 회의 상세 보기
@router.get("/meetings/{meeting_id}")
def meeting_detail_view(
    meeting_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_login_page)
):
    meeting = (
        db.query(models.Meeting)
        .join(models.Project)
        .filter(
            models.Meeting.id == meeting_id,
            (
                (models.Project.owner_id == user.id)
                |
                models.Project.id.in_(
                    db.query(models.ProjectMember.project_id)
                    .filter(models.ProjectMember.user_id == user.id)
                )
                |
                models.Meeting.id.in_(
                    db.query(models.MeetingParticipant.meeting_id)
                    .filter(models.MeetingParticipant.user_id == user.id)
                )
            )
        )
        .first()
    )
    if not meeting:
        raise HTTPException(status_code=404, detail="회의를 찾을 수 없습니다.")

    return templates.TemplateResponse(
        request=request,
        name="meeting_detail.html",
        context={"active_tab": "meetings", "meeting": meeting, "user": user}
    )


# 업무 등록 페이지
@router.get("/tasks/new")
def new_task_view(
    request: Request,
    user: models.User = Depends(require_login_page)
):
    return templates.TemplateResponse(
        request=request,
        name="new_task.html",
        context={"active_tab": "calendar", "user": user}
    )
