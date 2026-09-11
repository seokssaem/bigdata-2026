"""
실습1 보너스 - 검색어 입력 검증 테스트 중 발견한 결함(DEF-2024-003) 재현

대상: GET /books/search
발견 경위: 정상/무결과/빈문자열 케이스를 테스트하던 중,
"공백만 입력하면 어떻게 될까?"라는 경계 케이스를 추가로 떠올려 테스트하면서 발견했다.
"""
import pytest
from fastapi.testclient import TestClient

from book_api import app

client = TestClient(app)


@pytest.mark.xfail(
    reason="DEF-2024-003: 공백(' ')만 입력해도 400 처리가 되지 않고, "
           "모든 책 제목에 포함된 띄어쓰기와 매치되어 전체 목록이 반환됨"
)
def test_search_books_whitespace_keyword_reveals_defect():
    """
    [경계값/예외] 검색어로 공백 문자(' ')만 입력하는 상황을 재현한다.
    기대 결과: '검색어 없음'과 동일하게 처리되어 400 또는 빈 결과(count: 0)여야 한다.
    실제 결과: 200과 함께 전체 도서 목록이 그대로 반환된다 (count: 3).
    """
    response = client.get("/books/search", params={"keyword": " "})

    assert response.status_code == 400
