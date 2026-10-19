# STOCKFLOW — Jinja2 재고 운영 화면

업로드한 FastAPI API를 사용하는 한국어 관리 화면입니다. Jinja2가 페이지·메뉴를 렌더링하고 JavaScript가 같은 서버의 기존 API를 fetch로 호출합니다. 별도의 화면 서버나 API URL 설정이 필요하지 않습니다.

## 기존 프로젝트에 적용하기 (권장)

1. 다음 항목을 기존 프로젝트에 복사합니다.
   - `app/web.py`
   - `app/templates/` 전체
   - `app/static/` 전체
2. 기존 `app/main.py` 맨 아래에 다음 두 줄을 추가합니다.

```python
from app.web import install_web
install_web(app)
```

3. Jinja2를 추가하고 실행합니다.

```bash
uv add jinja2
uv run uvicorn app.main:app --reload
```

pip 환경이라면:

```bash
python -m pip install jinja2
python -m uvicorn app.main:app --reload
```

4. **http://127.0.0.1:8000/ui/overview** 를 엽니다. API 문서는 `/docs`에서 확인할 수 있습니다.

기존 `app/core/config.py`, `.env`, DB 설정은 그대로 사용하세요. 기존에 `/` 또는 `/static`을 사용 중이면 `web.py`의 해당 경로를 조정하세요. `/ui/...`는 API 경로와 구분됩니다.

## 전체 프로젝트를 별도로 실행하기

업로드한 파일을 import 경로에 맞게 정리한 전체 프로젝트도 포함했습니다. 프로젝트 폴더에서 실행하세요.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

uv 환경에서는 `uv sync` 후 `uv run uvicorn app.main:app --reload`도 가능합니다.

`app/core/config.py`가 업로드에 없어서 별도 실행용 기본 설정을 제공했습니다. 기본적으로 프로젝트 폴더에 SQLite `inventory.db`를 생성합니다. PostgreSQL을 사용하려면 프로젝트 폴더의 `.env`에 본인의 연결 정보를 설정하세요.

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/DB_NAME
```

실제 PostgreSQL 연결과 기존 DB 데이터는 확인하지 않았습니다. 기존 프로젝트에 화면만 적용할 때는 새 기본 설정을 복사하지 않아도 됩니다.

## 화면과 API 연결

| 화면 | 경로 | 연결한 기존 API |
|---|---|---|
| 운영 대시보드 | `/ui/overview` | `GET /dashboard/summary`, 부족 재고·최근 주문 조회 |
| 상품 관리 | `/ui/products` | `GET /products` 검색·페이지 이동, `POST /products` |
| 거래처 관리 | `/ui/customers` | `GET /customers` 페이지 이동, `POST /customers` |
| 주문 관리 | `/ui/orders` | `GET /orders` 페이지 이동, `POST /orders`, 상품·거래처 조회 |
| 재고 관리 | `/ui/inventory` | `GET /inventory` 부족 재고 필터, `PATCH /inventory/{product_id}` |
| 수요 예측 | `/ui/forecasts` | `GET /forecasts`, `GET /forecasts/products/{product_id}` |
| 발주 추천 | `/ui/replenishment` | `GET /replenishment` |
| 주문 CSV 가져오기 | `/ui/imports` | `POST /imports/orders` |

- 주문은 여러 상품을 담을 수 있으며 등록하면 기존 API가 재고를 차감합니다. 중복 품목은 기존 API에서 합산합니다.
- 주문 상세는 조회 응답의 품목을 표시합니다. 삭제·취소 API는 제공되지 않아 해당 기능은 추가하지 않았습니다.
- 재고 조정은 증감량 입력입니다. 절대 수량 지정이 아닙니다.
- 상품·거래처·주문은 페이지당 20건을 표시합니다. 21건을 조회해 다음 페이지 유무를 확인합니다. 목록 API에 전체 건수가 없으므로 현재 페이지 건수만 표시합니다.
- 주문 선택 목록은 상품·거래처를 100건씩 조회해 전체 목록을 구성합니다.
- 대시보드는 누적 주문 금액을 표시합니다. 월 매출이나 성장률을 생성하지 않습니다.
- 예측은 실적·예측 그래프, 주별 수량 표, WAPE, 제외 사유를 표시합니다. WAPE는 낮을수록 좋은 백테스트 오차율이며 정확도가 아닙니다.
- **수요 예측과 발주 추천 모두 기존 서비스에서 26주 이상의 주문 이력을 요구합니다.** 부족하면 API 오류를 화면에 표시합니다.
- 발주 추천은 추천 조회만 수행합니다. 실제 발주나 입고를 생성하지 않습니다. 계산되지 않은 수량(null)은 0으로 해석하지 않습니다.
- CSV는 UTF-8 또는 UTF-8 BOM, 최대 10MB입니다. 필수 컬럼과 예시 파일은 업로드 화면에서 확인할 수 있습니다.
- CSV 주문 이력은 현재 재고를 차감하지 않습니다. 기존 API에 중복 업로드 방지가 없으므로 같은 파일을 다시 올리지 않도록 확인하세요.
- 중복 SKU, 재고 부족, 입력값 오류 등을 페이지 상단 또는 등록 모달에 표시합니다.
- 주문 시각은 브라우저 현지 시간, 예측·발주 날짜는 기존 API의 UTC 기준입니다.

## 파일 구성

```text
app/
  main.py                  기존 API 등록 + install_web 연결
  web.py                   새 화면 라우팅과 Jinja2 설정
  templates/base.html      공통 메뉴·헤더·등록 모달
  templates/page.html      8개 화면 구성
  static/style.css         화면 스타일·모바일 레이아웃
  static/app.js            API 호출·폼·표·예측 그래프
  static/orders-template.csv
  core/config.py           업로드에 없던 기본 설정 (별도 실행용)
  routers/                 업로드한 API 라우터
  ...                      업로드한 모델·서비스·계산 코드
```

| 업로드 이름 | 프로젝트 위치 |
|---|---|
| `main(9).py` | `app/main.py` |
| `models(7).py` | `app/models.py` |
| `schemas(2).py` | `app/schemas.py` |
| `database(6).py` | `app/database.py` |
| `replenishment.py` | `app/replenishment.py` (계산 코드) |
| `replenishment(1).py` | `app/routers/replenishment.py` (라우터) |

기존 서비스·라우터·모델의 업무 로직은 수정하지 않았습니다. Jinja2 의존성을 추가하고 requirements의 중복 requests를 정리했습니다. 제공된 pyproject의 다른 버전 제약은 유지했습니다.

## 검증

임시 SQLite DB에서 통합 테스트 3개가 통과했습니다.

- 8개 Jinja2 화면·정적 파일·루트 이동·health API
- 상품·거래처·주문 등록 → 자동 재고 차감 → 재고 조정
- 중복 SKU·재고 부족·음수 재고 조정 오류
- CSV 이력 등록 → 실제 전체·상품별 수요 예측 → 발주 추천
- 데이터 부족·잘못된 CSV 오류

```bash
python -m pip install pytest httpx
python -m pytest tests -q
```

테스트는 임시 SQLite를 사용하고 실제 DB lifespan 초기화를 실행하지 않습니다. Python 컴파일과 JavaScript 문법 검사도 통과했습니다. 가상 DOM과 모의 API 응답을 이용해 8개 화면의 초기 로드, 등록·재고 조정·CSV 업로드·상품별 예측 이벤트도 확인했습니다. 브라우저 런타임을 설치할 수 없어 실제 브라우저에서의 클릭·시각 검증은 완료하지 못했습니다.
