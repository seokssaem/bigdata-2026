import json
from unittest.mock import MagicMock, patch

from services.ai_service import analyze_meeting


def test_process_meeting_ai():
    # 1. 테스트용 회의 내용
    sample_text = (
        "테스트 회의입니다. "
        "PostgreSQL을 데이터베이스로 사용하기로 결정했습니다."
    )

    # 2. Gemini가 반환했다고 가정할 가짜 응답
    mock_data = {
        "summary": "PostgreSQL을 사용하기로 결정한 회의",
        "key_points": ["데이터베이스 선정"],
        "decisions": ["PostgreSQL 사용"],
        "action_items": []
    }

    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(mock_data, ensure_ascii=False)

    # 3. 실제 Gemini API 호출을 가짜 응답으로 대체
    with patch("services.ai_service._get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = analyze_meeting(
            transcript=sample_text,
            title="테스트 회의",
            attendees=[]
        )

    # 4. AI 분석 결과 검증
    assert result.summary == mock_data["summary"]
    assert result.key_points == mock_data["key_points"]
    assert result.decisions == mock_data["decisions"]
    assert result.action_items == []

    # 5. Gemini 호출 함수가 정확히 한 번 실행되었는지 확인
    mock_client.chat.completions.create.assert_called_once()