import os
from decimal import Decimal, InvalidOperation

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 10

st.set_page_config(
    page_title="B2B 재고 운영 시스템",
    page_icon="📦",
    layout="wide",
)


def api_request(method: str, path: str, **kwargs):
    """FastAPI 요청을 공통 처리하고 사용자에게 읽기 쉬운 오류를 보여준다."""
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )
    except requests.ConnectionError:
        st.error("FastAPI 서버에 연결할 수 없습니다. API 서버가 실행 중인지 확인하세요.")
        return None
    except requests.RequestException as exc:
        st.error(f"API 요청 중 오류가 발생했습니다: {exc}")
        return None

    if response.ok:
        return response.json() if response.content else None

    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    st.error(f"요청 실패 ({response.status_code}): {detail}")
    return None


def money(value) -> str:
    try:
        return f"₩{Decimal(str(value)):,.0f}"
    except (InvalidOperation, TypeError):
        return "₩0"


def show_dashboard():
    st.header("운영 대시보드")
    summary = api_request("GET", "/dashboard/summary")
    if summary is None:
        return

    columns = st.columns(5)
    columns[0].metric("등록 상품", f"{summary['product_count']:,}개")
    columns[1].metric("거래처", f"{summary['customer_count']:,}곳")
    columns[2].metric("누적 주문", f"{summary['order_count']:,}건")
    columns[3].metric("누적 매출", money(summary["total_sales"]))
    columns[4].metric("부족 재고", f"{summary['low_stock_count']:,}개")

    st.subheader("재주문 필요 상품")
    low_stock = api_request("GET", "/inventory", params={"low_stock_only": True})
    if low_stock:
        frame = pd.DataFrame(low_stock).rename(
            columns={
                "sku": "상품코드",
                "name": "상품명",
                "quantity": "현재 재고",
                "reorder_point": "재주문 기준",
            }
        )
        st.dataframe(
            frame[["상품코드", "상품명", "현재 재고", "재주문 기준"]],
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("현재 재주문이 필요한 상품이 없습니다.")


def show_products():
    st.header("상품 관리")
    create_tab, list_tab = st.tabs(["상품 등록", "상품 조회"])

    with create_tab:
        with st.form("product_form", clear_on_submit=True):
            left, right = st.columns(2)
            sku = left.text_input("상품코드(SKU)", placeholder="P-001")
            name = right.text_input("상품명", placeholder="산업용 센서")
            unit_price = left.number_input("판매 단가", min_value=1, step=1000)
            reorder_point = right.number_input("재주문 기준", min_value=0, value=10)
            initial_stock = left.number_input("초기 재고", min_value=0, value=0)
            submitted = st.form_submit_button("상품 등록", type="primary")

        if submitted:
            if not sku.strip() or not name.strip():
                st.warning("상품코드와 상품명을 입력하세요.")
            else:
                result = api_request(
                    "POST",
                    "/products",
                    json={
                        "sku": sku.strip(),
                        "name": name.strip(),
                        "unit_price": unit_price,
                        "reorder_point": reorder_point,
                        "initial_stock": initial_stock,
                    },
                )
                if result:
                    st.success(f"{result['name']} 상품을 등록했습니다.")

    with list_tab:
        search = st.text_input("상품 검색", placeholder="상품코드 또는 상품명")
        products = api_request("GET", "/products", params={"search": search, "limit": 100})
        if products:
            frame = pd.DataFrame(products)
            frame["unit_price"] = frame["unit_price"].map(money)
            frame = frame.rename(
                columns={
                    "sku": "상품코드",
                    "name": "상품명",
                    "unit_price": "단가",
                    "reorder_point": "재주문 기준",
                    "stock_quantity": "현재 재고",
                }
            )
            st.dataframe(
                frame[["상품코드", "상품명", "단가", "현재 재고", "재주문 기준"]],
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("등록된 상품이 없습니다. 먼저 상품을 등록하세요.")


def show_customers():
    st.header("거래처 관리")
    create_tab, list_tab = st.tabs(["거래처 등록", "거래처 조회"])

    with create_tab:
        with st.form("customer_form", clear_on_submit=True):
            company_name = st.text_input("회사명", placeholder="테스트 제조")
            business_number = st.text_input("사업자번호", placeholder="123-45-67890")
            contact_name = st.text_input("담당자명")
            contact_email = st.text_input("담당자 이메일")
            submitted = st.form_submit_button("거래처 등록", type="primary")

        if submitted:
            if not company_name.strip() or not business_number.strip():
                st.warning("회사명과 사업자번호를 입력하세요.")
            else:
                result = api_request(
                    "POST",
                    "/customers",
                    json={
                        "company_name": company_name.strip(),
                        "business_number": business_number.strip(),
                        "contact_name": contact_name.strip() or None,
                        "contact_email": contact_email.strip() or None,
                    },
                )
                if result:
                    st.success(f"{result['company_name']} 거래처를 등록했습니다.")

    with list_tab:
        customers = api_request("GET", "/customers", params={"limit": 100})
        if customers:
            frame = pd.DataFrame(customers).rename(
                columns={
                    "company_name": "회사명",
                    "business_number": "사업자번호",
                    "contact_name": "담당자",
                    "contact_email": "이메일",
                }
            )
            st.dataframe(
                frame[["회사명", "사업자번호", "담당자", "이메일"]],
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("등록된 거래처가 없습니다.")


def show_inventory():
    st.header("재고 관리")
    low_stock_only = st.toggle("재주문 필요 상품만 보기")
    inventory = api_request(
        "GET", "/inventory", params={"low_stock_only": low_stock_only}
    )

    if not inventory:
        st.info("조회할 재고가 없습니다. 상품을 먼저 등록하세요.")
        return

    frame = pd.DataFrame(inventory)
    frame["상태"] = frame["needs_reorder"].map({True: "발주 필요", False: "정상"})
    frame = frame.rename(
        columns={
            "sku": "상품코드",
            "name": "상품명",
            "quantity": "현재 재고",
            "reorder_point": "재주문 기준",
        }
    )
    st.dataframe(
        frame[["상품코드", "상품명", "현재 재고", "재주문 기준", "상태"]],
        width="stretch",
        hide_index=True,
    )

    st.subheader("재고 입출고")
    product_options = {
        f"{item['sku']} | {item['name']} (현재 {item['quantity']}개)": item["product_id"]
        for item in inventory
    }
    with st.form("stock_form"):
        selected = st.selectbox("상품", options=list(product_options))
        amount = st.number_input(
            "조정 수량",
            value=1,
            step=1,
            help="입고는 양수, 출고는 음수로 입력하세요.",
        )
        submitted = st.form_submit_button("재고 반영", type="primary")

    if submitted:
        result = api_request(
            "PATCH",
            f"/inventory/{product_options[selected]}",
            json={"amount": amount},
        )
        if result:
            st.success(f"재고를 반영했습니다. 현재 재고: {result['quantity']}개")
            st.rerun()


def show_orders():
    st.header("주문 관리")
    create_tab, list_tab = st.tabs(["주문 등록", "주문 내역"])

    with create_tab:
        customers = api_request("GET", "/customers", params={"limit": 100}) or []
        products = api_request("GET", "/products", params={"limit": 100}) or []

        if not customers or not products:
            st.info("주문을 등록하려면 상품과 거래처가 각각 하나 이상 필요합니다.")
        else:
            customer_options = {
                f"{item['company_name']} | {item['business_number']}": item["id"]
                for item in customers
            }
            product_options = {
                f"{item['sku']} | {item['name']} | 재고 {item['stock_quantity']}개": item["id"]
                for item in products
            }

            with st.form("order_form", clear_on_submit=True):
                customer_label = st.selectbox("거래처", list(customer_options))
                product_label = st.selectbox("상품", list(product_options))
                quantity = st.number_input("주문 수량", min_value=1, value=1)
                submitted = st.form_submit_button("주문 등록", type="primary")

            if submitted:
                result = api_request(
                    "POST",
                    "/orders",
                    json={
                        "customer_id": customer_options[customer_label],
                        "items": [
                            {
                                "product_id": product_options[product_label],
                                "quantity": quantity,
                            }
                        ],
                    },
                )
                if result:
                    st.success(
                        f"주문 #{result['id']}을 등록했습니다. "
                        f"주문금액: {money(result['total_amount'])}"
                    )

    with list_tab:
        orders = api_request("GET", "/orders", params={"limit": 100})
        if orders:
            rows = []
            for order in orders:
                rows.append(
                    {
                        "주문번호": order["id"],
                        "거래처 ID": order["customer_id"],
                        "상태": order["status"],
                        "주문일시": order["ordered_at"],
                        "상품 종류": len(order["items"]),
                        "주문금액": money(order["total_amount"]),
                    }
                )
            st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        else:
            st.info("등록된 주문이 없습니다.")


st.title("📦 B2B 재고·매출 운영 시스템")
st.caption(f"연결 API: {API_BASE_URL}")

page = st.sidebar.radio(
    "메뉴",
    ["대시보드", "상품", "거래처", "재고", "주문"],
)

if page == "대시보드":
    show_dashboard()
elif page == "상품":
    show_products()
elif page == "거래처":
    show_customers()
elif page == "재고":
    show_inventory()
else:
    show_orders()
