from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from database import get_db
from routers.auth import get_current_user
from schemas.project import ProjectCreate,  ProjectUpdate, ProjectResponse


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)

def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    from sqlalchemy import or_

    shared_project_ids = (
        db.query(models.ProjectMember.project_id)
        .filter(models.ProjectMember.user_id == current_user.id)
    )

    projects = (
        db.query(models.Project)
        .filter(
            or_(
                models.Project.owner_id == current_user.id,
                models.Project.id.in_(shared_project_ids)
            )
        )
        .all()
    )

    return projects

@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            (
                (models.Project.owner_id == current_user.id)
                |
                models.Project.id.in_(
                    db.query(models.ProjectMember.project_id).filter(
                        models.ProjectMember.user_id == current_user.id
                    )
                )
            )
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="프로젝트를 찾을 수 없습니다."
        )

    return project

@router.put(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id,
            models.Project.owner_id == current_user.id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="프로젝트를 찾을 수 없습니다."
        )

    project.name = project_update.name
    project.description = project_update.description

    db.commit()
    db.refresh(project)

    return project

# 프로젝트 참여자 초대
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError


class ProjectInviteRequest(BaseModel):
    email: EmailStr


@router.post("/{project_id}/members", status_code=201)
def invite_project_member(
    project_id: int,
    data: ProjectInviteRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 프로젝트 소유자만 초대 가능
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="프로젝트가 없거나 초대 권한이 없습니다."
        )

    # 이메일로 가입 사용자 검색
    invited_user = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if not invited_user:
        raise HTTPException(
            status_code=404,
            detail="가입되지 않은 사용자입니다."
        )

    if invited_user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="프로젝트 소유자는 초대할 필요가 없습니다."
        )

    # 중복 참여 확인
    existing = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.user_id == invited_user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="이미 프로젝트에 참여 중인 사용자입니다."
        )

    member = models.ProjectMember(
        project_id=project_id,
        user_id=invited_user.id,
        role="viewer"
    )

    db.add(member)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="이미 프로젝트에 참여 중인 사용자입니다."
        )

    return {
        "message": "프로젝트 참여자로 등록되었습니다.",
        "project_id": project_id,
        "user_id": invited_user.id,
        "role": "viewer"
    }
