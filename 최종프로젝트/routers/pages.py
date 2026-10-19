"""화면(HTML)을 렌더링하는 라우터 - JSON이 아니라 실제 웹페이지를 반환한다.

화면 목록
  /                  메인 (요약 + 상승 TOP5 + 상품 목록/검색/카테고리 필터 + 페이지 넘기기)
  /product/{이름}     상품 상세 (지표 카드 + 그래프 + 최근 가격 이력)
  /ranking           가격 랭킹 (직전 대비 / 전년동기 대비 / 다음 예측)
  /favorites         내 즐겨찾기 (로그인 필요, 로그인 안 했으면 로그인 화면으로 보냄)
  /partials/cards    상품 카드 묶음(HTML 조각) - 메인의 '최근 본 상품'이 JS로 불러감
"""
import math
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload

from database import get_db
import models
from security import get_current_user
from templates_config import templates

router = APIRouter(tags=["pages"])

PAGE_SIZE = 24  # 한 페이지에 보여줄 상품 수


# ──────────────────────────── 공통 도우미 ────────────────────────────

def get_latest_changes(db: Session, product_ids: list[int]) -> dict[int, models.PriceChange]:
    """상품별로 '가장 최근 조사시점'의 가격/등락률 행을 {product_id: PriceChange}로 돌려준다.

    상품마다 마지막으로 유효했던 조사일이 다를 수 있어서(표본이 부족한 시점은 집계에서
    빠지기 때문에), 전체 최신일이 아니라 상품별 최신일을 기준으로 잡는다.
    """
    if not product_ids:
        return {}
    last_dates = (
        db.query(
            models.PriceChange.product_id,
            func.max(models.PriceChange.survey_date).label("last_date"),
        )
        .filter(models.PriceChange.product_id.in_(product_ids))
        .group_by(models.PriceChange.product_id)
        .subquery()
    )
    rows = (
        db.query(models.PriceChange)
        .join(
            last_dates,
            and_(
                models.PriceChange.product_id == last_dates.c.product_id,
                models.PriceChange.survey_date == last_dates.c.last_date,
            ),
        )
        .all()
    )
    return {r.product_id: r for r in rows}


def parse_page(raw: str) -> int:
    """?page= 값을 안전하게 정수로 바꾼다. (숫자가 아니거나 1보다 작으면 1)"""
    try:
        return max(int(raw), 1)
    except (TypeError, ValueError):
        return 1


def like_escape(text: str) -> str:
    """검색어에 들어있는 % _ 가 LIKE 와일드카드로 해석되지 않게 막는다.

    이스케이프 문자로 백슬래시(\\) 대신 슬래시(/)를 쓴다. 백슬래시는 DB마다 해석이
    달라서(PostgreSQL 설정에 따라 오류가 날 수 있음) 슬래시가 가장 안전하다.
    """
    return text.replace("/", "//").replace("%", "/%").replace("_", "/_")


def build_pagination(page: int, total_pages: int, params: dict) -> dict:
    """'이전 1 2 [3] 4 … 22 다음' 형태의 페이지 링크 목록을 만든다.

    params: 페이지를 넘겨도 유지해야 하는 조건(검색어, 카테고리)
    """
    def url(n: int) -> str:
        query = dict(params)
        if n > 1:
            query["page"] = n
        return "/?" + urlencode(query) if query else "/"

    # 첫 페이지, 마지막 페이지, 현재 페이지 앞뒤 2개만 보여주고 나머지는 … 로 줄인다
    numbers = sorted({1, total_pages, *range(max(1, page - 2), min(total_pages, page + 2) + 1)})
    links, prev = [], None
    for n in numbers:
        if prev is not None and n - prev > 1:
            links.append({"gap": True})
        links.append({"n": n, "url": url(n), "active": n == page})
        prev = n

    return {
        "links": links,
        "prev_url": url(page - 1) if page > 1 else None,
        "next_url": url(page + 1) if page < total_pages else None,
    }


def build_dashboard(db: Session) -> dict | None:
    """메인 화면 위쪽에 보여줄 '이번 조사 상승 TOP5' (조사 기준일 포함)."""
    latest_date = db.query(func.max(models.PriceChange.survey_date)).scalar()
    if latest_date is None:
        return None

    top = (
        db.query(models.PriceChange)
        .options(joinedload(models.PriceChange.product))
        .filter(
            models.PriceChange.survey_date == latest_date,
            models.PriceChange.change_rate.isnot(None),
        )
        .order_by(models.PriceChange.change_rate.desc())
        .limit(5)
        .all()
    )
    return {"date": latest_date, "top": top}


# ──────────────────────────── 화면 라우트 ────────────────────────────

@router.get("/")
def index_page(
    request: Request,
    search: str | None = None,
    category: str | None = None,
    page: str = "1",
    db: Session = Depends(get_db),
):
    search = (search or "").strip() or None
    category = category or None

    query = db.query(models.Product)
    if search:
        query = query.filter(
            models.Product.product_name.ilike(f"%{like_escape(search)}%", escape="/")
        )
    if category:
        query = query.filter(models.Product.category == category)

    total = query.count()
    total_pages = max(1, math.ceil(total / PAGE_SIZE))
    page_no = min(parse_page(page), total_pages)  # 범위를 넘으면 마지막 페이지로

    products = (
        query.order_by(models.Product.product_name)
        .offset((page_no - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
        .all()
    )
    latest = get_latest_changes(db, [p.id for p in products])

    categories = [
        r[0] for r in db.query(models.Product.category).distinct()
        .order_by(models.Product.category).all()
    ]

    filters = {k: v for k, v in {"search": search, "category": category}.items() if v}
    first = (page_no - 1) * PAGE_SIZE + 1

    return templates.TemplateResponse(request, "index.html", {
        "active": "home",
        "products": products,
        "latest": latest,
        "categories": categories,
        "search": search,
        "category": category,
        "total": total,
        "range_start": first if total else 0,
        "range_end": first + len(products) - 1 if total else 0,
        "pagination": build_pagination(page_no, total_pages, filters),
        "total_pages": total_pages,
        # 검색/필터 중이거나 2페이지 이후에는 요약을 숨기고 결과에만 집중하게 한다
        "dashboard": build_dashboard(db) if not filters and page_no == 1 else None,
    })


@router.get("/product/{product_name}")
def product_detail_page(
    product_name: str,
    request: Request,
    db: Session = Depends(get_db),
    user: models.User | None = Depends(get_current_user),
):
    product = db.query(models.Product).filter_by(product_name=product_name).first()
    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    history = sorted(product.price_history, key=lambda h: h.survey_date)
    change = (
        db.query(models.PriceChange)
        .filter_by(product_id=product.id)
        .order_by(models.PriceChange.survey_date.desc())
        .first()
    )
    prediction = db.query(models.Prediction).filter_by(product_id=product.id).first()

    # 로그인했다면 이 상품이 내 즐겨찾기에 들어 있는지 (버튼 모양을 정하는 데 쓴다)
    is_favorite = bool(
        user and db.query(models.Favorite).filter_by(user_id=user.id, product_id=product.id).first()
    )

    return templates.TemplateResponse(request, "product_detail.html", {
        "active": "home",
        "product": product,
        "history": history,
        "change": change,
        "prediction": prediction,
        "is_favorite": is_favorite,
    })


@router.get("/ranking")
def ranking_page(
    request: Request,
    basis: str = "prev",
    direction: str = "up",
    db: Session = Depends(get_db),
):
    if basis not in ("prev", "yoy", "predict"):
        basis = "prev"
    if direction not in ("up", "down"):
        direction = "up"

    if basis == "predict":
        rows = (
            db.query(models.Prediction)
            .options(joinedload(models.Prediction.product))
            # 상한(15%)에 걸려 값이 같은 상품이 많아서, 같은 값끼리는 상한 적용 전 예측값이 큰 순으로 줄 세운다
            .order_by(
                models.Prediction.expected_change_rate.desc(),
                models.Prediction.raw_expected_change_rate.desc(),
            )
            .limit(20)
            .all()
        )
        items = [{
            "product_name": r.product.product_name,
            "from_price": r.base_price,
            "to_price": r.predicted_price,
            "rate": r.expected_change_rate,
        } for r in rows]
        return templates.TemplateResponse(request, "ranking.html", {
            "active": "ranking", "items": items, "basis": basis, "direction": "up",
        })

    latest_date = db.query(func.max(models.PriceChange.survey_date)).scalar()
    rate_col = models.PriceChange.change_rate if basis == "prev" else models.PriceChange.yoy_change_rate

    rows = (
        db.query(models.PriceChange)
        .options(joinedload(models.PriceChange.product))
        .filter(models.PriceChange.survey_date == latest_date)
        .filter(rate_col.isnot(None))
        .order_by(rate_col.desc() if direction == "up" else rate_col.asc())
        .limit(20)
        .all()
    )
    items = [{
        "product_name": r.product.product_name,
        "from_price": r.prev_price if basis == "prev" else r.yoy_price,
        "to_price": r.avg_price,
        "rate": r.change_rate if basis == "prev" else r.yoy_change_rate,
    } for r in rows]

    return templates.TemplateResponse(request, "ranking.html", {
        "active": "ranking", "items": items, "basis": basis, "direction": direction,
        "survey_date": latest_date,
    })


@router.get("/favorites")
def favorites_page(
    request: Request,
    db: Session = Depends(get_db),
    user: models.User | None = Depends(get_current_user),
):
    # 즐겨찾기는 회원별로 DB에 저장되어 있다. 로그인하지 않았다면 로그인 화면으로 보낸다.
    if user is None:
        return RedirectResponse("/login?next=/favorites", status_code=303)

    rows = (
        db.query(models.Favorite)
        .options(joinedload(models.Favorite.product))
        .filter(models.Favorite.user_id == user.id)
        .order_by(models.Favorite.id.desc())  # 가장 최근에 추가한 상품이 맨 앞
        .all()
    )
    products = [r.product for r in rows]
    latest = get_latest_changes(db, [p.id for p in products])
    return templates.TemplateResponse(request, "favorites.html", {
        "active": "favorites", "products": products, "latest": latest,
    })


@router.get("/partials/cards")
def cards_partial(
    request: Request,
    names: list[str] = Query(default=[]),
    db: Session = Depends(get_db),
):
    """상품명 목록을 받아서 상품 카드 HTML 조각을 돌려준다. (names 순서 그대로)"""
    names = names[:30]  # 너무 많이 요청해도 30개까지만
    found = {
        p.product_name: p
        for p in db.query(models.Product).filter(models.Product.product_name.in_(names)).all()
    }
    products = [found[n] for n in names if n in found]
    latest = get_latest_changes(db, [p.id for p in products])
    return templates.TemplateResponse(request, "partial_cards.html", {
        "products": products, "latest": latest,
    })
