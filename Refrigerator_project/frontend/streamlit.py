import streamlit as st
import requests
import pandas as pd
import math

from collections import Counter
from datetime import date


# --------------------------------------------------
# FastAPI 서버 주소
# --------------------------------------------------
API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# 전체 식재료 조회 함수
# --------------------------------------------------
def get_all_ingredients():
    all_ingredients = []

    skip = 0
    limit = 100

    while True:
        response = requests.get(
            f"{API_URL}/ingredients",
            params={
                "skip": skip,
                "limit": limit
            },
            timeout=5
        )

        if response.status_code != 200:
            return None

        ingredients = response.json()

        all_ingredients.extend(ingredients)

        if len(ingredients) < limit:
            break

        skip += limit

    return all_ingredients


# --------------------------------------------------
# 페이지 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="냉장고 식자재 관리",
    page_icon="🥬",
    layout="wide"
)


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🥬 냉장고 식자재 관리")

st.write(
    "냉장고에 보관 중인 식재료를 등록하고 관리하는 서비스입니다."
)

st.divider()


# --------------------------------------------------
# FastAPI 서버 연결 확인
# --------------------------------------------------
try:
    response = requests.get(
        f"{API_URL}/",
        timeout=3
    )

    if response.status_code == 200:
        server_connected = True
    else:
        server_connected = False

except requests.exceptions.RequestException:
    server_connected = False


# --------------------------------------------------
# 사이드바 메뉴
# --------------------------------------------------
st.sidebar.title("🥬 냉장고 관리")

if server_connected:
    st.sidebar.success("API 연결됨")
else:
    st.sidebar.error("API 연결 실패")


# 처음 실행했을 때 기본 메뉴
if "menu" not in st.session_state:
    st.session_state.menu = "홈"


# --------------------------------------------------
# 이모지 버튼 메뉴
# --------------------------------------------------
if st.sidebar.button(
    "🏠 홈",
    use_container_width=True
):
    st.session_state.menu = "홈"


if st.sidebar.button(
    "📊 식재료 현황",
    use_container_width=True
):
    st.session_state.menu = "식재료 현황"


if st.sidebar.button(
    "📋 식재료 목록",
    use_container_width=True
):
    st.session_state.menu = "식재료 목록"


if st.sidebar.button(
    "➕ 식재료 등록",
    use_container_width=True
):
    st.session_state.menu = "식재료 등록"


if st.sidebar.button(
    "✏️ 수정 / 삭제",
    use_container_width=True
):
    st.session_state.menu = "식재료 수정/삭제"


if st.sidebar.button(
    "📁 CSV 업로드",
    use_container_width=True
):
    st.session_state.menu = "CSV 업로드"


menu = st.session_state.menu


# ==================================================
# 홈
# ==================================================
if menu == "홈":

    st.subheader("🏠 냉장고 현황")

    try:

        ingredients = get_all_ingredients()

        if ingredients is None:

            st.error(
                "식재료 데이터를 불러오지 못했습니다."
            )

        elif not ingredients:

            st.info(
                "현재 등록된 식재료가 없습니다."
            )

        else:

            today = date.today()

            expired = []
            urgent = []
            safe = []

            # ------------------------------------------
            # 유통기한 상태 계산
            # ------------------------------------------
            for item in ingredients:

                expiration = date.fromisoformat(
                    item["expiration_date"]
                )

                days_left = (
                    expiration - today
                ).days

                item["days_left"] = days_left

                if days_left < 0:

                    expired.append(item)

                elif days_left <= 3:

                    urgent.append(item)

                else:

                    safe.append(item)


            # ------------------------------------------
            # 대시보드 통계
            # ------------------------------------------
            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "전체 식재료",
                    len(ingredients)
                )

            with col2:

                st.metric(
                    "유통기한 만료",
                    len(expired)
                )

            with col3:

                st.metric(
                    "3일 이내 임박",
                    len(urgent)
                )

            with col4:

                st.metric(
                    "보관 여유",
                    len(safe)
                )


            st.divider()


            # ------------------------------------------
            # 유통기한별 식재료 수 그래프
            # ------------------------------------------
            st.subheader("📊 유통기한별 식재료 수")

            expiration_counts = Counter()

            for item in ingredients:
                days_left = item["days_left"]

                if days_left < 0:
                    expiration_counts["만료"] += 1
                elif days_left == 0:
                    expiration_counts["오늘까지"] += 1
                elif days_left <= 3:
                    expiration_counts["1~3일 남음"] += 1
                elif days_left <= 7:
                    expiration_counts["4~7일 남음"] += 1
                else:
                    expiration_counts["8일 이상"] += 1

            expiration_order = [
                "만료",
                "오늘까지",
                "1~3일 남음",
                "4~7일 남음",
                "8일 이상"
            ]

            expiration_data = [
                (label, expiration_counts.get(label, 0))
                for label in expiration_order
            ]

            expiration_df = pd.DataFrame(
                expiration_data,
                columns=["유통기한 상태", "개수"]
            ).set_index("유통기한 상태")

            st.bar_chart(expiration_df)

            st.divider()


            # ------------------------------------------
            # 유통기한 만료
            # ------------------------------------------
            st.subheader("🚨 유통기한 만료")

            if expired:

                expired_data = []

                expired.sort(
                    key=lambda x: x["days_left"]
                )

                for item in expired:

                    expired_data.append(
                        {
                            "ID": item["id"],
                            "식재료": item["name"],
                            "카테고리": item["category"],
                            "수량": item["quantity"],
                            "유통기한": item["expiration_date"],
                            "경과일": abs(item["days_left"]),
                            "보관방법": item["storage_method"]
                        }
                    )

                # 만료 식재료를 행 단위로 표시하고 마지막 열에 삭제 버튼 추가
                header_cols = st.columns([0.7, 1.6, 1.4, 1.0, 1.4, 0.9, 1.1, 0.9])
                headers = [
                    "ID",
                    "식재료",
                    "카테고리",
                    "수량",
                    "유통기한",
                    "경과일",
                    "보관방법",
                    "삭제"
                ]

                for col, header in zip(header_cols, headers):
                    col.markdown(f"**{header}**")

                for item in expired:
                    row_cols = st.columns([0.7, 1.6, 1.4, 1.0, 1.4, 0.9, 1.1, 0.9])

                    row_cols[0].write(item["id"])
                    row_cols[1].write(item["name"])
                    row_cols[2].write(item["category"])
                    row_cols[3].write(item["quantity"])
                    row_cols[4].write(item["expiration_date"])
                    row_cols[5].write(abs(item["days_left"]))
                    row_cols[6].write(item["storage_method"])

                    if row_cols[7].button(
                        "🗑️",
                        key=f"delete_expired_{item['id']}",
                        help=f"{item['name']} 삭제"
                    ):
                        try:
                            delete_response = requests.delete(
                                f"{API_URL}/ingredients/{item['id']}",
                                timeout=5
                            )

                            if delete_response.status_code == 204:
                                st.success(
                                    f"{item['name']}을(를) 폐기 처리하고 목록에서 삭제했습니다."
                                )
                                st.rerun()
                            else:
                                st.error(
                                    f"삭제에 실패했습니다. 상태 코드: {delete_response.status_code}"
                                )

                        except requests.exceptions.RequestException as e:
                            st.error(
                                f"삭제 중 오류가 발생했습니다: {e}"
                            )

            else:

                st.success(
                    "유통기한이 지난 식재료가 없습니다."
                )


            st.divider()


            # ------------------------------------------
            # 유통기한 임박
            # ------------------------------------------
            st.subheader("⚠️ 유통기한 임박")

            if urgent:

                urgent_data = []

                urgent.sort(
                    key=lambda x: x["days_left"]
                )

                for item in urgent:

                    if item["days_left"] == 0:

                        status = "오늘까지"

                    else:

                        status = (
                            f"{item['days_left']}일 남음"
                        )

                    urgent_data.append(
                        {
                            "ID": item["id"],
                            "식재료": item["name"],
                            "카테고리": item["category"],
                            "수량": item["quantity"],
                            "유통기한": item["expiration_date"],
                            "상태": status,
                            "보관방법": item["storage_method"]
                        }
                    )

                st.dataframe(
                    urgent_data,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.success(
                    "3일 이내 유통기한이 임박한 "
                    "식재료가 없습니다."
                )


    except requests.exceptions.ConnectionError:

        st.error(
            "FastAPI 서버에 연결할 수 없습니다."
        )

    except requests.exceptions.Timeout:

        st.error(
            "식재료 조회 시간이 초과되었습니다."
        )

    except requests.exceptions.RequestException as e:

        st.error(
            f"식재료 조회 중 오류가 발생했습니다: {e}"
        )

    except ValueError as e:

        st.error(
            f"날짜 처리 중 오류가 발생했습니다: {e}"
        )


# ==================================================
# 식재료 현황
# ==================================================
elif menu == "식재료 현황":

    st.subheader("📊 식재료 현황")

    try:
        all_ingredients = get_all_ingredients()

        if all_ingredients is None:
            st.error("식재료 현황을 불러오지 못했습니다.")

        elif not all_ingredients:
            st.info("현재 등록된 식재료가 없습니다.")

        else:
            today = date.today()

            category_counts = Counter(
                item.get("category") or "미분류"
                for item in all_ingredients
            )

            storage_counts = Counter(
                item.get("storage_method") or "미지정"
                for item in all_ingredients
            )

            # 상단 요약
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("전체 식재료", len(all_ingredients))

            with col2:
                st.metric("카테고리 수", len(category_counts))

            with col3:
                st.metric("보관방법 수", len(storage_counts))

            st.divider()

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.markdown("### 카테고리별 식재료 수")

                category_df = pd.DataFrame(
                    sorted(category_counts.items()),
                    columns=["카테고리", "개수"]
                ).set_index("카테고리")

                st.bar_chart(category_df)

            with chart_col2:
                st.markdown("### 보관방법별 식재료 수")

                storage_df = pd.DataFrame(
                    sorted(storage_counts.items()),
                    columns=["보관방법", "개수"]
                ).set_index("보관방법")

                st.bar_chart(storage_df)


    except requests.exceptions.ConnectionError:
        st.error("FastAPI 서버에 연결할 수 없습니다.")

    except requests.exceptions.Timeout:
        st.error("식재료 현황 조회 시간이 초과되었습니다.")

    except requests.exceptions.RequestException as e:
        st.error(f"식재료 현황 조회 중 오류가 발생했습니다: {e}")

    except ValueError as e:
        st.error(f"유통기한 처리 중 오류가 발생했습니다: {e}")


# ==================================================
# 식재료 목록
# ==================================================
elif menu == "식재료 목록":

    st.subheader("📋 식재료 목록")

    try:
        # 전체 식재료를 가져온 뒤 검색/필터 및 페이지 처리
        all_ingredients = get_all_ingredients()

        if all_ingredients is None:
            st.error("식재료 목록을 불러오지 못했습니다.")

        else:
            # ------------------------------------------
            # 검색 / 필터
            # ------------------------------------------
            col1, col2, col3 = st.columns(3)

            with col1:
                keyword = st.text_input(
                    "식재료 이름 검색",
                    placeholder="예: 우유, 사과"
                )

            with col2:
                category = st.text_input(
                    "카테고리",
                    placeholder="예: 과일, 채소, 유제품"
                )

            with col3:
                storage_method = st.selectbox(
                    "보관 방법",
                    [
                        "전체",
                        "냉장",
                        "냉동",
                        "실온"
                    ]
                )

            # ------------------------------------------
            # 검색 조건 적용
            # ------------------------------------------
            filtered_ingredients = all_ingredients

            if keyword.strip():
                search_keyword = keyword.strip()
                filtered_ingredients = [
                    item for item in filtered_ingredients
                    if search_keyword in item.get("name", "")
                ]

            if category.strip():
                search_category = category.strip()
                filtered_ingredients = [
                    item for item in filtered_ingredients
                    if item.get("category") == search_category
                ]

            if storage_method != "전체":
                filtered_ingredients = [
                    item for item in filtered_ingredients
                    if item.get("storage_method") == storage_method
                ]

            # ------------------------------------------
            # 필터가 바뀌면 1페이지로 이동
            # ------------------------------------------
            current_filter = (
                keyword.strip(),
                category.strip(),
                storage_method
            )

            if "ingredient_filter" not in st.session_state:
                st.session_state.ingredient_filter = current_filter

            if st.session_state.ingredient_filter != current_filter:
                st.session_state.ingredient_filter = current_filter
                st.session_state.ingredient_page = 1

            if "ingredient_page" not in st.session_state:
                st.session_state.ingredient_page = 1

            # ------------------------------------------
            # 20개씩 페이지 처리
            # ------------------------------------------
            page_size = 20
            total_count = len(filtered_ingredients)
            total_pages = max(1, math.ceil(total_count / page_size))

            if st.session_state.ingredient_page > total_pages:
                st.session_state.ingredient_page = total_pages

            page = st.session_state.ingredient_page

            start_index = (page - 1) * page_size
            end_index = start_index + page_size

            page_ingredients = filtered_ingredients[start_index:end_index]

            st.write(
                f"총 {total_count}개 / "
                f"{page}페이지 / {total_pages}페이지"
            )

            # ------------------------------------------
            # 목록 출력
            # ------------------------------------------
            if page_ingredients:
                display_data = []

                for item in page_ingredients:
                    display_data.append(
                        {
                            "ID": item["id"],
                            "식재료": item["name"],
                            "카테고리": item["category"],
                            "수량": item["quantity"],
                            "구매일": item["purchase_date"],
                            "유통기한": item["expiration_date"],
                            "보관방법": item["storage_method"]
                        }
                    )

                st.dataframe(
                    display_data,
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.info("조건에 맞는 식재료가 없습니다.")

            # ------------------------------------------
            # 페이지 이동 버튼
            # - 페이지 번호는 한 번에 최대 10개 표시
            # ------------------------------------------
            if total_count > 0:
                block_start = ((page - 1) // 10) * 10 + 1
                block_end = min(block_start + 9, total_pages)
                page_numbers = list(range(block_start, block_end + 1))

                # 페이지 버튼을 화면 가운데에 더 작고 촘촘하게 배치
                # 좌우 여백을 크게 두고, 버튼 열은 아주 좁게 설정
                pagination_columns = st.columns(
                    [6] + [0.28] * (len(page_numbers) + 2) + [6],
                    gap="small"
                )

                button_columns = pagination_columns[1:-1]

                with button_columns[0]:
                    if st.button(
                        "◀",
                        key="ingredient_prev_page",
                        disabled=(page <= 1)
                    ):
                        st.session_state.ingredient_page -= 1
                        st.rerun()

                for index, page_number in enumerate(page_numbers, start=1):
                    with button_columns[index]:
                        button_label = (
                            f"[{page_number}]"
                            if page_number == page
                            else str(page_number)
                        )

                        if st.button(
                            button_label,
                            key=f"ingredient_page_{page_number}"
                        ):
                            st.session_state.ingredient_page = page_number
                            st.rerun()

                with button_columns[-1]:
                    if st.button(
                        "▶",
                        key="ingredient_next_page",
                        disabled=(page >= total_pages)
                    ):
                        st.session_state.ingredient_page += 1
                        st.rerun()

    except requests.exceptions.ConnectionError:
        st.error("FastAPI 서버에 연결할 수 없습니다.")

    except requests.exceptions.Timeout:
        st.error("식재료 목록 조회 시간이 초과되었습니다.")

    except requests.exceptions.RequestException as e:
        st.error(f"식재료 조회 중 오류가 발생했습니다: {e}")


# ==================================================
# 식재료 등록
# ==================================================
elif menu == "식재료 등록":

    st.subheader("➕ 식재료 등록")

    st.write(
        "새로운 식재료 정보를 입력해주세요."
    )


    with st.form(
        "ingredient_create_form",
        clear_on_submit=True
    ):

        name = st.text_input(
            "식재료 이름 *",
            placeholder="예: 우유"
        )

        category = st.text_input(
            "카테고리",
            placeholder="입력하지 않으면 미분류"
        )

        quantity = st.text_input(
            "수량",
            placeholder="예: 1개, 500g, 2팩"
        )


        col1, col2 = st.columns(2)

        with col1:

            purchase_date = st.date_input(
                "구매일 *"
            )

        with col2:

            expiration_date = st.date_input(
                "유통기한 *"
            )


        storage_method = st.selectbox(
            "보관 방법",
            [
                "",
                "냉장",
                "냉동",
                "실온"
            ]
        )


        submitted = st.form_submit_button(
            "➕ 식재료 등록",
            use_container_width=True
        )


    if submitted:

        if not name.strip():

            st.warning(
                "식재료 이름을 입력해주세요."
            )

        else:

            data = {
                "name": name.strip(),
                "category": category.strip(),
                "quantity": quantity.strip(),
                "purchase_date":
                    purchase_date.isoformat(),
                "expiration_date":
                    expiration_date.isoformat(),
                "storage_method":
                    storage_method
            }


            try:

                response = requests.post(
                    f"{API_URL}/ingredients",
                    json=data,
                    timeout=5
                )

                if response.status_code == 201:

                    st.success(
                        "식재료가 정상적으로 등록되었습니다."
                    )

                    st.json(
                        response.json()
                    )

                else:

                    st.error(
                        f"식재료 등록 실패: "
                        f"{response.status_code}"
                    )

                    try:

                        error_data = response.json()

                        if "detail" in error_data:

                            st.error(
                                error_data["detail"]
                            )

                    except ValueError:
                        pass


            except requests.exceptions.RequestException as e:

                st.error(
                    f"식재료 등록 중 오류가 발생했습니다: {e}"
                )


# ==================================================
# 식재료 수정 / 삭제
# ==================================================
elif menu == "식재료 수정/삭제":

    st.subheader("✏️ 식재료 수정 / 삭제")


    try:

        ingredients = get_all_ingredients()

        if ingredients is None:

            st.error(
                "식재료 목록을 불러오지 못했습니다."
            )

        elif not ingredients:

            st.info(
                "등록된 식재료가 없습니다."
            )

        else:

            # ------------------------------------------
            # 식재료 선택
            # ------------------------------------------
            ingredient_options = {
                f"{item['id']} - {item['name']}":
                    item["id"]
                for item in ingredients
            }


            selected_label = st.selectbox(
                "수정 또는 삭제할 식재료",
                ingredient_options.keys()
            )


            selected_id = (
                ingredient_options[selected_label]
            )


            # ------------------------------------------
            # 단건 조회
            # ------------------------------------------
            detail_response = requests.get(
                f"{API_URL}/ingredients/{selected_id}",
                timeout=5
            )


            if detail_response.status_code != 200:

                st.error(
                    "식재료 정보를 불러오지 못했습니다."
                )

            else:

                ingredient = (
                    detail_response.json()
                )


                # ======================================
                # 수정
                # ======================================
                st.subheader("✏️ 정보 수정")


                with st.form(
                    "ingredient_update_form"
                ):

                    name = st.text_input(
                        "식재료 이름",
                        value=ingredient["name"]
                    )

                    category = st.text_input(
                        "카테고리",
                        value=ingredient["category"]
                    )

                    quantity = st.text_input(
                        "수량",
                        value=ingredient["quantity"]
                    )


                    col1, col2 = st.columns(2)

                    with col1:

                        purchase_date = st.date_input(
                            "구매일",
                            value=date.fromisoformat(
                                ingredient[
                                    "purchase_date"
                                ]
                            )
                        )

                    with col2:

                        expiration_date = st.date_input(
                            "유통기한",
                            value=date.fromisoformat(
                                ingredient[
                                    "expiration_date"
                                ]
                            )
                        )


                    storage_options = [
                        "냉장",
                        "냉동",
                        "실온"
                    ]


                    current_storage = (
                        ingredient["storage_method"]
                    )


                    if current_storage in storage_options:

                        storage_index = (
                            storage_options.index(
                                current_storage
                            )
                        )

                    else:

                        storage_index = 0


                    storage_method = st.selectbox(
                        "보관 방법",
                        storage_options,
                        index=storage_index
                    )


                    update_button = (
                        st.form_submit_button(
                            "💾 수정하기",
                            use_container_width=True
                        )
                    )


                if update_button:

                    update_data = {}


                    if (
                        name.strip()
                        != ingredient["name"]
                    ):

                        update_data["name"] = (
                            name.strip()
                        )


                    if (
                        category.strip()
                        != ingredient["category"]
                    ):

                        update_data["category"] = (
                            category.strip()
                        )


                    if (
                        quantity.strip()
                        != ingredient["quantity"]
                    ):

                        update_data["quantity"] = (
                            quantity.strip()
                        )


                    if (
                        purchase_date.isoformat()
                        != ingredient["purchase_date"]
                    ):

                        update_data[
                            "purchase_date"
                        ] = purchase_date.isoformat()


                    if (
                        expiration_date.isoformat()
                        != ingredient[
                            "expiration_date"
                        ]
                    ):

                        update_data[
                            "expiration_date"
                        ] = expiration_date.isoformat()


                    if (
                        storage_method
                        != ingredient[
                            "storage_method"
                        ]
                    ):

                        update_data[
                            "storage_method"
                        ] = storage_method


                    if not update_data:

                        st.warning(
                            "변경된 내용이 없습니다."
                        )

                    else:

                        update_response = (
                            requests.patch(
                                f"{API_URL}/ingredients/"
                                f"{selected_id}",
                                json=update_data,
                                timeout=5
                            )
                        )


                        if (
                            update_response.status_code
                            == 200
                        ):

                            st.success(
                                "식재료 정보가 "
                                "수정되었습니다."
                            )

                            st.rerun()

                        else:

                            st.error(
                                f"수정 실패: "
                                f"{update_response.status_code}"
                            )


                # ======================================
                # 삭제
                # ======================================
                st.divider()

                st.subheader(
                    "🗑️ 식재료 삭제"
                )

                st.warning(
                    "삭제한 데이터는 복구할 수 없습니다."
                )


                delete_confirm = st.checkbox(
                    f"{ingredient['name']}을(를) "
                    "삭제합니다."
                )


                delete_button = st.button(
                    "🗑️ 삭제하기",
                    use_container_width=True
                )


                if delete_button:

                    if not delete_confirm:

                        st.warning(
                            "삭제 확인을 체크해주세요."
                        )

                    else:

                        delete_response = (
                            requests.delete(
                                f"{API_URL}/ingredients/"
                                f"{selected_id}",
                                timeout=5
                            )
                        )


                        if (
                            delete_response.status_code
                            == 204
                        ):

                            st.success(
                                "식재료가 삭제되었습니다."
                            )

                            st.rerun()

                        else:

                            st.error(
                                f"삭제 실패: "
                                f"{delete_response.status_code}"
                            )


    except requests.exceptions.RequestException as e:

        st.error(
            f"서버 연결 중 오류가 발생했습니다: {e}"
        )


# ==================================================
# CSV 업로드
# ==================================================
elif menu == "CSV 업로드":

    st.subheader("📁 CSV 파일 업로드")

    st.write(
        "CSV 파일을 이용하여 여러 식재료를 "
        "한 번에 등록할 수 있습니다."
    )


    st.info(
        "CSV 컬럼명: "
        "식재료, 분류, 수량, 구매일, 유통기한, 보관"
    )

    st.write(
        """
        날짜 형식

        - 8/25
        - 9/1
        - 12/31
        """
    )


    uploaded_file = st.file_uploader(
        "CSV 파일 선택",
        type=["csv"]
    )


    if uploaded_file is not None:

        st.write(
            f"선택한 파일: {uploaded_file.name}"
        )


        upload_button = st.button(
            "📤 CSV 업로드",
            use_container_width=True
        )


        if upload_button:

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/csv"
                    )
                }


                response = requests.post(
                    f"{API_URL}/ingredients/upload",
                    files=files,
                    timeout=10
                )


                if response.status_code == 201:

                    data = response.json()

                    st.success(
                        data.get(
                            "message",
                            "CSV 업로드가 완료되었습니다."
                        )
                    )

                else:

                    st.error(
                        f"CSV 업로드 실패: "
                        f"{response.status_code}"
                    )

                    try:

                        error_data = response.json()

                        if "detail" in error_data:

                            st.error(
                                error_data["detail"]
                            )

                    except ValueError:
                        pass


            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI 서버에 연결할 수 없습니다."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "CSV 업로드 시간이 초과되었습니다."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"CSV 업로드 중 오류가 "
                    f"발생했습니다: {e}"
                )