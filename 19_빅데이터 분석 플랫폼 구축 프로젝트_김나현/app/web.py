from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

ROOT = Path(__file__).resolve().parent
PAGES = [
    ('overview', '운영 대시보드', '오늘의 재고와 주문 현황을 한눈에 확인하세요.', '◈'),
    ('products', '상품 관리', '상품 정보와 판매 단가, 재주문 기준을 관리하세요.', '▦'),
    ('customers', '거래처 관리', '함께하는 거래처와 담당자 정보를 확인하세요.', '▤'),
    ('orders', '주문 관리', '거래처 주문을 등록하고 주문 내역을 확인하세요.', '▣'),
    ('inventory', '재고 관리', '입고·출고 수량을 반영하고 부족한 재고를 확인하세요.', '▥'),
    ('forecasts', '수요 예측', '주간 주문 실적을 바탕으로 앞으로의 수요를 살펴보세요.', '↗'),
    ('replenishment', '발주 추천', '예상 수요와 입고 소요 시간을 기준으로 발주를 계획하세요.', '⟳'),
    ('imports', '데이터 가져오기', 'CSV 주문 내역으로 상품·거래처·과거 주문을 함께 등록하세요.', '⇧'),
]

def install_web(app: FastAPI):
    templates = Jinja2Templates(directory=str(ROOT / 'templates'))
    app.mount('/static', StaticFiles(directory=str(ROOT / 'static')), name='static')

    @app.get('/', include_in_schema=False)
    def home():
        return RedirectResponse('/ui/overview')

    def make_page(key, title, description):
        async def page(request: Request):
            return templates.TemplateResponse(
                request=request, name='page.html',
                context={'page': key, 'title': title, 'description': description, 'pages': PAGES},
            )
        return page

    for key, title, description, _ in PAGES:
        app.add_api_route('/ui/' + key, make_page(key, title, description), methods=['GET'], include_in_schema=False)
