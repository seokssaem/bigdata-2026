import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile
from openai import OpenAI, OpenAIError

load_dotenv()

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads/audio"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXT = {
    ".mp3", ".wav", ".m4a", ".ogg",
    ".flac", ".webm", ".aac"
}

MAX_SIZE_MB = int(os.getenv("MAX_AUDIO_MB", "25"))
STT_MODEL = os.getenv(
    "OPENAI_STT_MODEL",
    "gpt-4o-mini-transcribe"
)


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            500,
            "OPENAI_API_KEY가 설정되지 않았습니다."
        )
    return OpenAI(api_key=api_key)


def save_audio_file(file: UploadFile) -> str:
    """음성 파일 저장"""
    ext = Path(file.filename or "").suffix.lower()

    if ext not in ALLOWED_EXT:
        raise HTTPException(
            400,
            "지원하지 않는 음성 파일 형식입니다."
        )

    path = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
    size = 0

    with open(path, "wb") as f:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)

            if size > MAX_SIZE_MB * 1024 * 1024:
                f.close()
                path.unlink(missing_ok=True)
                raise HTTPException(
                    413,
                    f"파일 크기는 최대 {MAX_SIZE_MB}MB입니다."
                )

            f.write(chunk)

    return str(path)


def transcribe_audio(
    audio_path: str,
    language: str = "한국어"
) -> str:
    """OpenAI 음성-텍스트 변환"""

    if not os.path.exists(audio_path):
        raise HTTPException(
            404,
            "오디오 파일을 찾을 수 없습니다."
        )

    client = _get_client()

    try:
        with open(audio_path, "rb") as audio:
            response = client.audio.transcriptions.create(
                model=STT_MODEL,
                file=audio,
                language="ko"
            )

        text = (response.text or "").strip()

        if not text:
            raise HTTPException(
                422,
                "음성에서 텍스트를 추출하지 못했습니다."
            )

        return text

    except HTTPException:
        raise

    except OpenAIError as e:
        raise HTTPException(
            502,
            f"OpenAI STT 처리 오류: {type(e).__name__}"
        )


def delete_audio_file(audio_path: str | None) -> None:
    """음성 파일 삭제"""
    if audio_path:
        Path(audio_path).unlink(missing_ok=True)
