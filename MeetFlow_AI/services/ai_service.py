"""회의록 AI 분석 (요약 / 결정사항 / 액션 아이템 추출) - Gemini"""
import json
import os
from datetime import date

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI

from schemas.meeting import MeetingAnalysis

load_dotenv()

AI_MODEL = os.getenv("OPENAI_AI_MODEL", "gpt-4.1-mini")
MAX_TRANSCRIPT_CHARS = 200_000

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise HTTPException(
                500, "OPENAI_API_KEY가 설정되지 않았습니다."
            )
        _client = OpenAI(api_key=api_key)
    return _client


def _build_prompt(transcript: str, title: str, attendees: list[str]) -> str:
    today = date.today().isoformat()
    names = ", ".join(attendees) if attendees else "알 수 없음"
    return f"""당신은 회의록을 분석하는 전문 비서입니다.
오늘 날짜: {today}
회의 제목: {title}
참석자: {names}

아래 회의 전사본을 분석해 JSON으로만 답하세요. 스키마:
{{
  "summary": "3~5문장 요약",
  "key_points": ["핵심 논의 사항", ...],
  "decisions": ["확정된 결정 사항", ...],
  "action_items": [
    {{
      "task": "해야 할 일 (구체적으로 한 문장)",
      "assignee_name": "담당자 이름 (참석자 중 일치하는 이름, 없으면 null)",
      "due_date": "YYYY-MM-DD 또는 null ('다음 주 금요일' 같은 표현은 오늘 날짜 기준으로 계산)"
    }}
  ]
}}
규칙: 전사본에 없는 내용을 지어내지 말 것. 모든 값은 한국어.

--- 전사본 ---
{transcript}
"""


def analyze_meeting(transcript: str, title: str = "", attendees: list[str] | None = None) -> MeetingAnalysis:
    if not transcript or not transcript.strip():
        raise HTTPException(400, "분석할 전사 텍스트가 없습니다. 먼저 음성을 업로드하세요.")
    if len(transcript) > MAX_TRANSCRIPT_CHARS:
        raise HTTPException(413, "전사본이 너무 깁니다.")

    client = _get_client()
    try:
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "회의록을 정확히 분석하고 JSON으로만 답하세요."
                },
                {
                    "role": "user",
                    "content": _build_prompt(transcript, title, attendees or [])
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        raw = (response.choices[0].message.content or "").strip()
        raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(raw)
        for key in ("key_points", "decisions", "action_items"):
            data[key] = data.get(key) or []
        data["summary"] = data.get("summary") or ""
        return MeetingAnalysis(**data)
    except json.JSONDecodeError:
        raise HTTPException(502, "AI 응답을 해석하지 못했습니다. 다시 시도해 주세요.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"AI 분석 중 오류가 발생했습니다: {e}")