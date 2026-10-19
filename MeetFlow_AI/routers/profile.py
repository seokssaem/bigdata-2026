import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

import models
from database import get_db
from routers.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["profile"])

PROFILE_DIR = Path("uploads/profile")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_URL_PREFIX = "/uploads/profile/"
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_SIZE_MB = 5


def _delete_old_image(url: str | None) -> None:
    """이전 프로필 사진 파일 삭제 (우리가 저장한 경로일 때만)"""
    if url and url.startswith(PROFILE_URL_PREFIX):
        (PROFILE_DIR / Path(url).name).unlink(missing_ok=True)


@router.post("/profile-image")
def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(
            400,
            f"지원하지 않는 형식입니다. 허용: {', '.join(sorted(ALLOWED_EXT))}"
        )

    filename = f"{uuid.uuid4().hex}{ext}"
    path = PROFILE_DIR / filename

    size = 0
    limit = MAX_SIZE_MB * 1024 * 1024
    with open(path, "wb") as f:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                f.close()
                path.unlink(missing_ok=True)
                raise HTTPException(413, f"파일이 너무 큽니다 (최대 {MAX_SIZE_MB}MB).")
            f.write(chunk)

    old_url = current_user.profile_image
    current_user.profile_image = f"{PROFILE_URL_PREFIX}{filename}"
    db.commit()
    _delete_old_image(old_url)

    return {"profile_image": current_user.profile_image}
