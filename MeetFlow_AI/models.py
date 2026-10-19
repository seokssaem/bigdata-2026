from datetime import datetime, date

from sqlalchemy import String, Text, DateTime, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from enum import Enum

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )
    password: Mapped[str] = mapped_column(String(255))
    # 프로필 사진 URL (예: /uploads/profile/xxxx.png)
    profile_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100)
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # 프로젝트를 생성한 사용자
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    # Project → User 관계
    owner: Mapped["User"] = relationship()



class ProjectMember(Base):
    __tablename__ = "project_members"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "user_id",
            name="uq_project_member"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="viewer",
        nullable=False
    )





class MeetingParticipant(Base):

    __tablename__ = "meeting_participants"



    __table_args__ = (

        UniqueConstraint(

            "meeting_id",

            "user_id",

            name="uq_meeting_participant"

        ),

    )



    id: Mapped[int] = mapped_column(primary_key=True)



    meeting_id: Mapped[int] = mapped_column(

        ForeignKey("meetings.id", ondelete="CASCADE"),

        nullable=False

    )



    user_id: Mapped[int] = mapped_column(

        ForeignKey("users.id"),

        nullable=False

    )




class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String(200))
    meeting_date: Mapped[date] = mapped_column(Date)
    attendees: Mapped[str | None] = mapped_column(String(255), nullable=True) # 추가
    audio_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    project: Mapped["Project"] = relationship()

    decisions: Mapped[list["Decision"]] = relationship(lazy="selectin")
    action_items: Mapped[list["ActionItem"]] = relationship(lazy="selectin", back_populates="meeting")

# Decision 모델이 필요한 경우 정의 추가
class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"))
    content: Mapped[str] = mapped_column(Text)

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ActionItem(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # 어떤 회의(Meeting)에서 나온 액션 아이템인지 연결
    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id")
    )
    
    # 할 일 내용 및 상태 정의
    assignee_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    task: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, in_progress, completed 등
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    # ActionItem → Meeting 관계 설정 (필요시)
    meeting: Mapped["Meeting"] = relationship(back_populates="action_items")