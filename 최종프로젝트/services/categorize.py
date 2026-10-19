"""
상품 카테고리 분류

방식:
1. data/category_mapping.csv (직접 검증한 정답표)에 상품명이 있으면 그대로 사용 (100% 정확)
2. 정답표에 없는 새 상품(다음 달 새로 추가된 CSV 등)만 키워드 규칙으로 임시 분류

즉 이미 확인한 상품은 사람이 검증한 값을 쓰고, 처음 보는 상품만 자동 추정한다.
나중에 새로 분류된 상품도 검토 후 category_mapping.csv에 추가해주면
그 다음부터는 그 상품도 정답표 기준으로 처리된다.
"""
import pandas as pd

MAPPING_PATH = "data/category_mapping.csv"

# 정답표에 없는 신규 상품에 대한 임시 분류 규칙 (참가격 공식 13개 카테고리 기준)
CATEGORY_RULES = [
    ("곡물", ["쌀(", "쌀 ", "현미", "잡곡", "찹쌀", "보리", "흑미", "진상미"]),
    ("곡물가공품", ["라면", "우동", "냉면", "소면", "칼국수", "짜장", "스파게티", "파스타",
                "너구리", "짬뽕", "왕뚜껑", "밀가루", "부침가루", "튀김가루", "전분",
                "당면", "버터롤", "모닝롤", "빵", "햇반", "오뚜기밥", "컵밥", "콘푸로스트",
                "콘푸라이트", "만두", "떡", "보름달"]),
    ("정육·난류", ["돼지고기", "소고기", "닭고기", "삼겹살", "목살", "안심", "등심", "불고기",
                "계란", "달걀", "유정란", "훈제오리", "오리", "베이컨", "소시지", "그릴",
                "햄", "스팸", "비엔나", "후랑크", "토종닭", "백숙"]),
    ("수산가공품", ["맛살", "참치캔", "통조림", "젓갈", "액젓", "명란젓", "어묵", "황태",
                "북어", "멸치", "미역", "김(", "김 "]),
    ("낙농·축산가공품", ["우유", "치즈", "버터", "요거트", "요구르트", "두유", "분유", "마가린",
                    "홈버터", "앵커버터"]),
    ("조미료·장류·식용유", ["간장", "된장", "고추장", "쌈장", "식용유", "참기름", "들기름",
                      "콩기름", "카놀라유", "고춧가루", "소금", "설탕", "식초", "케첩",
                      "마요네즈", "물엿", "올리고당", "다시다", "와사비", "드레싱", "카레",
                      "토장", "꿀", "벌꿀"]),
    ("채소", ["배추", "무(", "양파", "대파", "마늘", "고추(", "오이", "감자", "당근",
             "시금치", "상추", "깻잎", "고구마", "버섯", "부추", "콩나물", "숙주",
             "애호박", "쪽파"]),
    ("생선류", ["고등어", "갈치", "조기", "오징어", "새우", "연어", "조개", "꽁치"]),
    ("과자·빙과류", ["과자", "스낵", "초콜릿", "사탕", "젤리", "비스킷", "쿠키", "껌",
                 "아이스크림", "월드콘", "메로나", "바밤바", "부라보콘", "싸만코",
                 "빅가나", "ABC초코", "ABC 초코", "목캔디", "에너지바"]),
    ("차·음료·주류", ["음료", "주스", "커피", "생수", "탄산수", "사이다", "콜라", "맥주",
                  "소주", "막걸리", "와인", "에일", "이온음료", "에너지드링크",
                  "에너지 드링크", "삼다수", "아이시스", "차(", "티백", "핫식스",
                  "몬스터", "레드불", "테라", "카스", "하이트", "참이슬", "처음처럼",
                  "제주 위트"]),
    ("이미용품", ["샴푸", "트리트먼트", "염색", "바디워시", "바디밀크", "로션", "크림",
               "세럼", "립", "선크림", "선 ", "치약", "칫솔", "면도날", "생리대",
               "패드", "기저귀", "손소독", "핸드워시", "마스크", "리스테린", "비누"]),
    ("세탁·주방·가사용품", ["화장지", "휴지", "미용티슈", "물티슈", "세제", "섬유유연제",
                     "락스", "방향제", "페브리즈", "키친타월", "호일", "지퍼백", "랩(",
                     "크린백", "건전지", "부탄가스", "습기제로", "물먹는하마", "종이호일"]),
]

DEFAULT_CATEGORY = "기타 가공식품"


def _rule_based_categorize(product_name: str) -> str:
    """정답표에 없는 상품에 대한 키워드 기반 임시 분류."""
    for category, keywords in CATEGORY_RULES:
        for kw in keywords:
            if kw in product_name:
                return category
    return DEFAULT_CATEGORY


def load_mapping(path: str = MAPPING_PATH) -> dict:
    """검증된 정답표(상품명→카테고리)를 딕셔너리로 불러온다."""
    mapping_df = pd.read_csv(path, encoding="utf-8-sig")
    return dict(zip(mapping_df["상품명"], mapping_df["카테고리"]))


def categorize(product_name: str, mapping: dict) -> str:
    """정답표에 있으면 그 값을, 없으면 규칙 기반 임시 분류값을 반환."""
    if product_name in mapping:
        return mapping[product_name]
    return _rule_based_categorize(product_name)


def categorize_series(product_names: pd.Series, mapping: dict) -> pd.Series:
    """pandas Series를 받아서 카테고리 Series를 반환한다."""
    return product_names.map(lambda name: categorize(name, mapping))


if __name__ == "__main__":
    mapping = load_mapping()
    print(f"정답표 로드: {len(mapping)}개 상품")

    df = pd.read_pickle("data/prices_combined.pkl")
    products = pd.Series(sorted(df["상품명"].unique()))
    categories = categorize_series(products, mapping)

    result = pd.DataFrame({"상품명": products, "카테고리": categories})
    result.to_csv("data/product_categories.csv", index=False, encoding="utf-8-sig")

    new_products = [p for p in products if p not in mapping]
    print(f"전체 상품: {len(products)}개")
    print(f"정답표에서 바로 매칭: {len(products) - len(new_products)}개")
    print(f"정답표에 없어서 규칙으로 임시분류: {len(new_products)}개")
    if new_products:
        print("  → 임시분류된 상품 목록:", new_products)
    print()
    print(result["카테고리"].value_counts())