'''
streamlit_app.py

- "카탈로그" 탭: KOBIS API를 실시간으로 직접 호출해서 보여줌 (팀원 A 담당)
                 .env의 KOBIS_API_KEY 사용
- "즐겨찾기 관리" 탭: 즐겨찾기 메모 수정 / 삭제 (팀원 C 담당)
  (즐겨찾기 추가는 카탈로그 탭의 "즐겨찾기" 버튼에서 이루어짐 - 팀원 B 영역)
'''
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE = 'http://127.0.0.1:8000'
KOBIS_LIST_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
KOBIS_INFO_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

st.set_page_config(page_title='영화 즐겨찾기', page_icon='🎬')
st.title('🎬 영화 카탈로그 & 즐겨찾기')


def get_kobis_key() -> str | None:
    return os.getenv('KOBIS_API_KEY')


RAW_PAGE_SIZE = 100  # KOBIS가 한 번에 줄 수 있는 최대 개수
PAGE_SIZE = 12        # 화면에 한 번에 보여줄 개수


def fetch_kobis_raw(api_key, keyword, director_nm, start_year, end_year, raw_page):
    """KOBIS에 100개 단위로 원시 조회 (필터링 전)"""
    params = {'key': api_key, 'curPage': raw_page, 'itemPerPage': RAW_PAGE_SIZE}
    if keyword:
        params['movieNm'] = keyword
    if director_nm:
        params['directorNm'] = director_nm
    if start_year:
        params['openStartDt'] = start_year
    if end_year:
        params['openEndDt'] = end_year
    res = requests.get(KOBIS_LIST_URL, params=params)
    res.raise_for_status()
    return res.json()['movieListResult']


def fill_catalog_cache(api_key, keyword, director_nm, start_year, end_year, min_count):
    """
    성인물을 걸러내고도 화면에 min_count개 이상 보여줄 수 있을 때까지
    KOBIS를 100개 단위로 반복 호출해서 캐시(st.session_state.catalog_cache)를 채운다.
    이미 KOBIS 쪽에 더 이상 데이터가 없으면(exhausted) 중단한다.
    """
    safety_limit = 50  # 무한 호출 방지용 상한 (100개 x 50번 = 5000개면 충분)
    calls = 0

    while (
        len(st.session_state.catalog_cache) < min_count
        and not st.session_state.catalog_exhausted
        and calls < safety_limit
    ):
        raw = fetch_kobis_raw(api_key, keyword, director_nm, start_year, end_year, st.session_state.catalog_raw_page)
        raw_movies = raw['movieList']
        st.session_state.catalog_total = int(raw['totCnt'])

        filtered = [m for m in raw_movies if '성인물' not in (m.get('genreAlt') or '')]
        st.session_state.catalog_excluded += len(raw_movies) - len(filtered)
        st.session_state.catalog_cache.extend(filtered)

        if len(raw_movies) < RAW_PAGE_SIZE:
            st.session_state.catalog_exhausted = True  # KOBIS에 더 이상 데이터가 없음

        st.session_state.catalog_raw_page += 1
        calls += 1


def fetch_kobis_detail(api_key, movie_cd):
    """상세정보(감독/배우 포함) 조회 - 즐겨찾기 등록 시 카탈로그에 저장할 정보를 채우기 위함"""
    res = requests.get(KOBIS_INFO_URL, params={'key': api_key, 'movieCd': movie_cd})
    res.raise_for_status()
    return res.json()['movieInfoResult']['movieInfo']


def add_to_favorites(api_key, movie_cd, movie_nm):
    """즐겨찾기 버튼 클릭 시: KOBIS 상세정보 조회 -> 카탈로그에 등록(이미 있으면 무시) -> 즐겨찾기 추가"""
    info = fetch_kobis_detail(api_key, movie_cd)

    body = {
        'movie_cd': movie_cd,
        'movie_nm': movie_nm,
        'movie_nm_en': info.get('movieNmEn') or None,
        'open_dt': info.get('openDt') or None,
        'show_tm': info.get('showTm') or None,
        'genre': '|'.join(g['genreNm'] for g in info.get('genres', [])) or None,
        'nation': '|'.join(n['nationNm'] for n in info.get('nations', [])) or None,
        'directors': [d['peopleNm'] for d in info.get('directors', [])],
        'actors': [a['peopleNm'] for a in info.get('actors', [])],
    }

    requests.post(f'{API_BASE}/movies/ensure', json=body)  # 카탈로그에 없으면 등록 (있으면 무시)
    fav_res = requests.post(f'{API_BASE}/favorites', json={'movie_cd': movie_cd})

    if fav_res.status_code == 201:
        st.success(f'"{movie_nm}" 즐겨찾기 추가됨')
    else:
        st.warning(fav_res.json().get('detail', '이미 즐겨찾기했거나 실패했습니다.'))


tab_catalog, tab_manage = st.tabs(['카탈로그 (KOBIS 실시간)', '즐겨찾기 관리'])

# ===================== 카탈로그 - KOBIS 실시간 (팀원 A, 즐겨찾기 추가 버튼은 팀원 B 영역) =====================
with tab_catalog:
    api_key = get_kobis_key()

    if not api_key:
        st.error('.env 파일에 KOBIS_API_KEY가 설정되어 있지 않습니다.')
        st.stop()

    col1, col2 = st.columns(2)
    keyword = col1.text_input('영화명 검색')
    director_nm = col2.text_input('감독명 검색')

    # 검색 버튼 / 개봉연도 시작 / ~ / 개봉연도 종료 를 한 줄에 배치.
    search_col, spacer_col, label_col, start_col, tilde_col, end_col = st.columns([1, 3.4, 0.6, 0.6, 0.25, 0.6])
    with search_col:
        search_clicked = st.button('검색')
    with label_col:
        st.markdown(
            "<div style='padding-top:0.5rem; font-size:14px;'>개봉연도</div>",
            unsafe_allow_html=True,
        )
    start_year = start_col.text_input('개봉연도 시작', placeholder='1919', label_visibility='collapsed')
    with tilde_col:
        st.markdown(
            "<div style='text-align:center; padding-top:0.4rem;'>~</div>",
            unsafe_allow_html=True,
        )
    end_year = end_col.text_input('개봉연도 종료', placeholder='2026', label_visibility='collapsed')

    # 검색 조건이 바뀌었는지 확인 -> 바뀌었으면 캐시를 전부 초기화하고 처음부터 다시 채움
    search_key = (keyword, director_nm, start_year, end_year)
    if 'catalog_search_key' not in st.session_state or st.session_state.catalog_search_key != search_key or search_clicked:
        st.session_state.catalog_search_key = search_key
        st.session_state.catalog_cache = []
        st.session_state.catalog_raw_page = 1
        st.session_state.catalog_exhausted = False
        st.session_state.catalog_total = 0
        st.session_state.catalog_excluded = 0
        st.session_state.catalog_display_page = 0

    display_page = st.session_state.catalog_display_page

    try:
        # 현재 페이지(display_page) + 다음 페이지 존재 여부 확인을 위해 한 페이지 더 채워둠
        fill_catalog_cache(api_key, keyword, director_nm, start_year, end_year, (display_page + 2) * PAGE_SIZE)
    except Exception as e:
        st.error(f'KOBIS 조회 실패: {e}')

    cache = st.session_state.catalog_cache
    movies = cache[display_page * PAGE_SIZE : (display_page + 1) * PAGE_SIZE]
    has_next = len(cache) > (display_page + 1) * PAGE_SIZE

    caption = f'KOBIS 전체 검색결과 {st.session_state.catalog_total}개 · 현재 페이지 {display_page + 1}'
    st.caption(caption)

    for m in movies:
        c1, c2 = st.columns([7, 1])
        c1.write(f'**{m["movieNm"]}** · {m.get("openDt") or "-"} · {m.get("genreAlt") or "-"} · {m.get("nationAlt") or "-"}')
        # ------------------ 즐겨찾기 추가 (팀원 B 담당 영역) ------------------
        if c2.button('즐겨찾기', key=f'fav_{m["movieCd"]}'):
            add_to_favorites(api_key, m['movieCd'], m['movieNm'])

    _, nav1, nav2, _ = st.columns([3, 1, 1, 3])
    if nav1.button('◀ 이전', disabled=display_page <= 0):
        st.session_state.catalog_display_page -= 1
        st.rerun()
    if nav2.button('다음 ▶', disabled=not has_next):
        st.session_state.catalog_display_page += 1
        st.rerun()

# ===================== 즐겨찾기 관리 (팀원 C 담당) =====================
with tab_manage:
    res = requests.get(f'{API_BASE}/favorites')
    favorites = res.json() if res.status_code == 200 else []

    search_fav = st.text_input('즐겨찾기 내 검색', placeholder='영화명으로 검색')
    if search_fav:
        favorites = [f for f in favorites if search_fav in f['movie_nm']]

    if not favorites:
        st.info('즐겨찾기한 영화가 없습니다. "카탈로그" 탭에서 먼저 추가해보세요.')

    for f in favorites:
        c1, c2, c3 = st.columns([4, 1, 1])
        c1.write(f'**{f["movie_nm"]}** · 메모: {f.get("memo") or "-"}')

        if c2.button('수정', key=f'edit_fav_{f["id"]}'):
            st.session_state.editing_fav = f['id']
            st.rerun()

        if c3.button('삭제', key=f'del_fav_{f["id"]}'):
            st.session_state.confirming_delete = f['id']  # "확인 중" 상태로 표시만 하고, 아직 지우지 않음
            st.rerun()

        # 방금 "삭제" 버튼을 누른 항목이면, 진짜 지울지 확인하는 문구+버튼을 보여줌
        if st.session_state.get('confirming_delete') == f['id']:
            st.warning(f'"{f["movie_nm"]}"을(를) 정말 삭제하시겠습니까?')
            confirm_col, cancel_col = st.columns(2)
            if confirm_col.button('네, 삭제합니다', key=f'confirm_del_{f["id"]}'):
                requests.delete(f'{API_BASE}/favorites/{f["id"]}')
                st.session_state.confirming_delete = None
                st.success('즐겨찾기 삭제됨')
                st.rerun()
            if cancel_col.button('취소', key=f'cancel_del_{f["id"]}'):
                st.session_state.confirming_delete = None
                st.rerun()

        if st.session_state.get('editing_fav') == f['id']:
            with st.form(f'edit_fav_form_{f["id"]}'):
                new_memo = st.text_input('메모', f.get('memo') or '')
                save = st.form_submit_button('저장')
            if save:
                requests.patch(f'{API_BASE}/favorites/{f["id"]}', json={'memo': new_memo})
                st.session_state.editing_fav = None
                st.success('수정됨')
                st.rerun()