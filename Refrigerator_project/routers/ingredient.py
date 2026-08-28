'''
routers/ingredient.py

API 엔드포인트
'''
import csv
from codecs import iterdecode
from datetime import date, timedelta
from fastapi import Depends, APIRouter, File, UploadFile, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models import Ingredient
from schema.response import IngredientResponse
from schema.request import IngredientCreate, IngredientUpdate

router = APIRouter(tags=['Ingredient'])

def parse_date(raw: Optional[str], year: int=2026) -> Optional[str]:
    """공용 유틸 : 'M/D' 형식 문자열을 'YYYY-MM-DD' 문자열로 반환 (실패 시 None)"""
    if not raw or '/' not in raw:
        return None
    parts = [p.strip() for p in raw.split('/')]
    if len(parts) != 2:
        return None
    try:
        month = int(parts[0])
        day = int(parts[1])
        return f"{year}-{month:02d}-{day:02d}"
    except ValueError:
        return None

def get_ingredient_or_404(ingredient_id: int, db: Session) -> Ingredient:
    """공용 유틸 : id로 식재료 조회 (없으면 404)"""
    ingredient = db.get(Ingredient, ingredient_id)  # 기본키로 단건 조회
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'id={ingredient_id}에 해당하는 식재료를 찾을 수 없습니다'
        )
    return ingredient

@router.post(
    "/ingredients/upload",
    status_code=status.HTTP_201_CREATED,
    summary="CSV 파일을 통한 식재료 데이터"
)
async def upload_ingredients_csv(
    file: UploadFile = File(..., description="식재료 CSV 파일"),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="csv 파일만 업로드 가능합니다."
        )

    try:
        decoded = iterdecode(file.file, 'utf-8-sig')
        csv_reader = csv.DictReader(decoded)
        
        ingredients_to_insert = []
        skipped_rows = 0

        for row in csv_reader:
            name = row.get("식재료")
            if not name:
                continue
                
            category = row.get("분류", "미분류")
            quantity = row.get("수량", "1")
            storage_method = row.get("보관", "냉장") 

            # 구매일: 필수값 - 파싱 실패 시 이 행은 등록 X
            raw_purchase = row.get('구매일')
            purchase_date_str = parse_date(raw_purchase)

            # 유통기한: 필수값 - 파싱 실패 시 이 행은 등록 X
            raw_expiration = row.get('유통기한')
            expiration_date_str = parse_date(raw_expiration)

            if purchase_date_str is None or expiration_date_str is None:
                skipped_rows += 1
                continue

            try:
                purchase_date = date.fromisoformat(purchase_date_str)
                expiration_date = date.fromisoformat(expiration_date_str)
            except ValueError:
                # 형식이 깨진 행은 건너뛰고 진행
                skipped_rows += 1
                continue

            db_ingredient = Ingredient(
                name=name,
                category=category,
                quantity=quantity,
                purchase_date=purchase_date,
                expiration_date=expiration_date,
                storage_method=storage_method
            )
            ingredients_to_insert.append(db_ingredient)

        # [수정 4] FOR 루프 외부에서 안전하게 대량 적재 및 단일 커밋 실행
        success_count = len(ingredients_to_insert)
        if success_count > 0:
            db.add_all(ingredients_to_insert)
            db.commit()
            message = f"성공적으로 {success_count}개의 식재료 데이터를 적재했습니다."
            if skipped_rows > 0:
                message += f'(필수값 누락/형식 오류로 {skipped_rows}개 행은 건너뛰었습니다.)'
            return {'message':message}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="적재할 유효한 데이터가 파일에 없습니다."
            )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터 적재 중 오류가 발생했습니다: {str(e)}"
        )

@router.post(
    '/ingredients',
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
    summary='식재료 단건 등록',
    description='날짜는 "YYYY-MM-DD" 형식으로 입력해주세요.'
)
async def create_ingredient(body: IngredientCreate, db: Session = Depends(get_db)):
    # model_dump() : pydantic 객체 → 딕셔너리 변환
    # ** : 언패킹 (키, 값)
    ingredient = Ingredient(**body.model_dump())
    db.add(ingredient)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'등록 중 오류가 발생했습니다: {str(e)}'
        )
    db.refresh(ingredient)
    return ingredient

@router.get("/ingredients",
    response_model=List[IngredientResponse],
    summary="식재료 목록 조회",
    description=(
        '저장된 모든 식재료 목록을 가져옵니다.\n'
        '\n파라미터 지정 시, 해당하는 식재료만 필터링해서 보여줍니다.'
    )
)
async def list_ingredients(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    storage_method: Optional[str] = None,
    skip: int=0,
    limit: int=20,
    db: Session = Depends(get_db)
):
    """
    저장된 모든 식재료 목록을 가져옵니다. 
    쿼리 파라미터 지정 시, 해당하는 식재료만 필터링해서 보여줍니다.
    """

    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='skip은 0 이상이어야 합니다.'
        )
    if limit <= 0 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='limit은 1~100 사이여야 합니다.'
        )
    
    try:
        stmt = select(Ingredient)
        
        if keyword:
            stmt = stmt.where(Ingredient.name.contains(keyword))
        if category:
            stmt = stmt.where(Ingredient.category == category)
        if storage_method:
            stmt = stmt.where(Ingredient.storage_method == storage_method)

        # ID 순서대로 정렬하여 가져오기
        stmt = stmt.order_by(Ingredient.id).offset(skip).limit(limit)
        
        result = db.execute(stmt)
        ingredients = result.scalars().all()

        return ingredients
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.get(
    '/ingredients/{ingredient_id}',
    response_model=IngredientResponse,
    status_code=status.HTTP_200_OK,
    summary='식재료 단건 조회'
)
async def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    return get_ingredient_or_404(ingredient_id, db)

@router.patch(
    '/ingredients/{ingredient_id}',
    response_model=IngredientResponse,
    status_code=status.HTTP_200_OK,
    summary='식재료 부분 수정',
    description='수정하고 싶은 필드만 남기고, 나머지 필드는 요청 본문에서 지워주세요.'
)
async def update_ingredient(
    ingredient_id: int,
    body: IngredientUpdate,
    db: Session = Depends(get_db)
):
    ingredient = get_ingredient_or_404(ingredient_id, db)

    # exclude_unset=True : 보낸 필드만 골라낸다, None인 필드는 뺀다
    update_data = body.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='수정할 필드가 없습니다.'
        )

    for field, value in update_data.items():
        # setattr(객체, 속성이름, 값) → 객체.속성이름 = 값
        setattr(ingredient, field, value)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'수정 중 오류가 발생했습니다: {str(e)}'
        )
    db.refresh(ingredient)
    return ingredient

@router.delete(
    '/ingredients/{ingredient_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='식재료 삭제'
)
async def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = get_ingredient_or_404(ingredient_id, db)
    try:
        db.delete(ingredient)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'삭제 중 오류가 발생했습니다: {str(e)}'
        )
    return None