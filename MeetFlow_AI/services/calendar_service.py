"""캘린더 연동: 회의/업무 마감일을 .ics(종일 일정)로 생성 - Google/Apple/Outlook에서 가져오기 가능"""
from datetime import date, datetime, timedelta, timezone
from typing import Iterable, Optional


def _esc(text: Optional[str]) -> str:
    if not text:
        return ""
    return (
        text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
        .replace("\r\n", "\\n").replace("\n", "\\n")
    )


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _all_day(uid: str, day: date, summary: str, description: str = "") -> list[str]:
    return [
        "BEGIN:VEVENT",
        f"UID:{uid}@meetflow.ai",
        f"DTSTAMP:{_stamp()}",
        f"DTSTART;VALUE=DATE:{day.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{(day + timedelta(days=1)).strftime('%Y%m%d')}",
        f"SUMMARY:{_esc(summary)}",
        f"DESCRIPTION:{_esc(description)}",
        "END:VEVENT",
    ]


def _wrap(body: list[str]) -> str:
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//MeetFlow AI//KO", "CALSCALE:GREGORIAN", *body, "END:VCALENDAR"]
    return "\r\n".join(lines) + "\r\n"


def build_meeting_ics(meeting) -> str:
    desc_parts = []
    if meeting.attendees:
        desc_parts.append(f"참석자: {meeting.attendees}")
    if meeting.summary:
        desc_parts.append(meeting.summary)
    return _wrap(_all_day(f"meeting-{meeting.id}", meeting.meeting_date, meeting.title, "\n\n".join(desc_parts)))


def build_action_items_ics(items: Iterable) -> str:
    body: list[str] = []
    for it in items:
        if not it.due_date:
            continue
        title = it.task if len(it.task) <= 60 else it.task[:57] + "..."
        desc = f"담당: {it.assignee_name}\n\n{it.task}" if it.assignee_name else it.task
        body += _all_day(f"task-{it.id}", it.due_date, f"[업무] {title}", desc)
    return _wrap(body)