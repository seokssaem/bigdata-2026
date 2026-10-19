"""matplotlib으로 가격 추이 그래프를 그려서 PNG로 반환하는 엔드포인트.
JS 차트 라이브러리 없이, 서버에서 이미지를 만들어 <img> 태그로 보여주는 방식."""
import io
import matplotlib
matplotlib.use("Agg")  # 화면 없는 서버 환경에서 그래프 그리기용 설정
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FuncFormatter

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from database import get_db
import models

router = APIRouter(tags=["charts"])

BRAND = "#0f766e"   # 사이트 메인 색 (style.css의 --brand와 같은 값)
MUTED = "#86868b"

# 한글 폰트가 없으면 그래프의 한글이 깨져서(네모) 보일 수 있어,
# 시스템에 있는 한글 지원 폰트를 찾아서 사용한다 (없으면 기본 폰트로 대체됨).
_KOREAN_FONT_CANDIDATES = ["Pretendard", "Malgun Gothic", "AppleGothic", "NanumGothic", "Noto Sans CJK KR"]
for _name in _KOREAN_FONT_CANDIDATES:
    if any(_name in f.name for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = _name
        break
plt.rcParams["axes.unicode_minus"] = False

# 최저가 대비 이 비율보다 변동이 작으면 "변동 적음"으로 보고 Y축을 0부터 그린다
VARIATION_THRESHOLD = 0.3


@router.get("/chart/{product_name}.png")
def product_chart(product_name: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter_by(product_name=product_name).first()
    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    history = sorted(product.price_history, key=lambda h: h.survey_date)
    dates = [h.survey_date for h in history]
    prices = [h.avg_price for h in history]

    fig, ax = plt.subplots(figsize=(8, 3.5))

    if not prices:
        # 가격 데이터가 하나도 없을 때도 이미지는 만들어서 화면이 깨지지 않게 한다
        ax.text(0.5, 0.5, "표시할 가격 데이터가 없어요", ha="center", va="center", color=MUTED, fontsize=12)
        ax.set_axis_off()
    else:
        ax.plot(dates, prices, marker="o", markersize=3, linewidth=1.8, color=BRAND)
        ax.grid(axis="y", linestyle="--", alpha=0.35)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#d8d8da")
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
        ax.tick_params(colors=MUTED, labelsize=9)

        # 변동폭이 작은 상품은 Y축을 0부터 시작시켜서 "실제로 별 차이 없다"는 걸
        # 그래프 모양 자체로 보여준다. 변동폭이 큰 상품은 확대해서 보여줘야
        # 진짜 변동이 드러나므로 이 경우엔 Y축을 건드리지 않는다.
        price_min, price_max = min(prices), max(prices)
        variation_ratio = (price_max - price_min) / price_min if price_min > 0 else 0
        if variation_ratio < VARIATION_THRESHOLD:
            ax.set_ylim(0, price_max * 1.15)

        # 선 아래 영역은 "그래프 맨 아래"까지 칠한다 (Y축 범위를 정한 뒤에 칠해야 어색하지 않음)
        y_bottom, y_top = ax.get_ylim()
        ax.fill_between(dates, prices, y_bottom, color=BRAND, alpha=0.07)
        ax.set_ylim(y_bottom, y_top)

        # 마지막 점에 현재가를 표시
        ax.scatter([dates[-1]], [prices[-1]], s=36, color=BRAND, zorder=3)
        ax.annotate(f"{prices[-1]:,.0f}원", (dates[-1], prices[-1]),
                    textcoords="offset points", xytext=(-6, 9), ha="right",
                    fontsize=10, fontweight="bold", color=BRAND)

        fig.autofmt_xdate(rotation=30)

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110)
    plt.close(fig)
    buf.seek(0)

    return Response(content=buf.read(), media_type="image/png")
