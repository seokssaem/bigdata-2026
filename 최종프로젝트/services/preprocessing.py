"""
한국소비자원 생필품 가격 CSV 병합 및 전처리

data/raw_csv/ 폴더에 원본 CSV 파일들(월별/격주별로 여러 개)을 넣어두면,
이 스크립트가 전부 읽어서 하나로 합치고, 조사 시점이 너무 적은(신상품/조사중단)
상품은 걸러낸 뒤 결과를 저장한다.
"""
import glob
import pandas as pd


def load_and_merge(csv_dir: str = "data/raw_csv") -> pd.DataFrame:
    """폴더 안의 모든 CSV를 cp949 인코딩으로 읽어서 하나로 합친다."""
    files = sorted(glob.glob(f"{csv_dir}/*.csv") + glob.glob(f"{csv_dir}/*.CSV"))
    if not files:
        raise FileNotFoundError(f"{csv_dir} 안에 CSV 파일이 없습니다.")

    dfs = [pd.read_csv(f, encoding="cp949") for f in files]
    merged = pd.concat(dfs, ignore_index=True)
    merged["조사일"] = pd.to_datetime(merged["조사일"])

    dup_count = merged.duplicated().sum()
    if dup_count > 0:
        merged = merged.drop_duplicates()

    return merged


def filter_by_coverage(df: pd.DataFrame, min_surveys: int = 30) -> pd.DataFrame:
    """
    전체 조사 시점 중 min_surveys 이상 등장한 상품만 남긴다.
    (등장 횟수가 너무 적은 상품은 추이 그래프를 그려도 의미가 없어서 제외)
    """
    coverage = df.groupby("상품명")["조사일"].nunique()
    valid_products = coverage[coverage >= min_surveys].index
    return df[df["상품명"].isin(valid_products)].copy()


def preprocess(csv_dir: str = "data/raw_csv", min_surveys: int = 30) -> pd.DataFrame:
    """병합 + 커버리지 필터링까지 한 번에 처리하는 진입점 함수."""
    merged = load_and_merge(csv_dir)
    filtered = filter_by_coverage(merged, min_surveys)
    return filtered.sort_values(["상품명", "조사일", "판매업소"]).reset_index(drop=True)


if __name__ == "__main__":
    result = preprocess()
    print(f"전처리 완료: {len(result)}행, 상품 {result['상품명'].nunique()}개, "
          f"조사일 {result['조사일'].nunique()}개 "
          f"({result['조사일'].min().date()} ~ {result['조사일'].max().date()})")
    result.to_pickle("data/prices_combined.pkl")
