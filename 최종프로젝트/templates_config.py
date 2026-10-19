"""
Jinja2 템플릿 설정을 한 곳에 모아둔 모듈.
main.py와 routers/pages.py 양쪽에서 같은 templates 객체를 가져다 쓴다
(안 그러면 순환 참조 문제가 생김).
"""
import os

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def static_url(path: str) -> str:
    """정적 파일(CSS/JS) 주소 뒤에 '파일 수정 시각'을 붙여서 돌려준다.

    예) static_url("css/style.css") → "/static/css/style.css?v=1791247125"

    브라우저는 CSS/JS를 한동안 저장(캐시)해두고 다시 안 받아오는데, 파일을 고쳐도
    주소가 그대로면 옛날 파일을 계속 쓸 수 있다. 파일이 바뀌면 ?v= 뒤 숫자도 바뀌어서
    주소가 달라지므로, 브라우저가 반드시 새 파일을 받아간다.
    """
    full_path = os.path.join("static", path)
    try:
        version = int(os.path.getmtime(full_path))
    except OSError:
        version = 0
    return f"/static/{path}?v={version}"


# 템플릿 안에서 {{ static_url('css/style.css') }} 처럼 쓸 수 있게 등록
templates.env.globals["static_url"] = static_url


# 카테고리(13개) → 태그 색 그룹(7개) 대응표.
# 색은 카테고리의 "의미"에 맞게 묶었다. (그룹별 실제 색은 static/css/style.css 의 .tag-* 에 있다)
#   grain 곡물류(호박색) · veg 채소(초록) · meat 육류·난류(살구색) · sea 수산(하늘색)
#   processed 가공·조미(갈색) · snack 간식·음료(보라) · living 생활용품(회색)
CATEGORY_GROUPS = {
    "곡물": "grain",
    "곡물가공품": "grain",
    "채소": "veg",
    "정육·난류": "meat",
    "생선류": "sea",
    "수산가공품": "sea",
    "낙농·축산가공품": "processed",
    "조미료·장류·식용유": "processed",
    "기타 가공식품": "processed",
    "과자·빙과류": "snack",
    "차·음료·주류": "snack",
    "이미용품": "living",
    "세탁·주방·가사용품": "living",
}


def category_tag_class(category: str) -> str:
    """카테고리 이름 → 태그 CSS 클래스. 대응표에 없는 새 카테고리는 기본색(tag-default)."""
    return "tag-" + CATEGORY_GROUPS.get(category, "default")


# 템플릿 안에서 {{ p.category|tag_class }} 처럼 쓸 수 있게 등록
templates.env.filters["tag_class"] = category_tag_class
