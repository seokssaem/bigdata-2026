"""업로드에 없던 설정 모듈. 기존 프로젝트에서는 기존 config.py를 유지하세요."""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'sqlite:///./inventory.db'
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()
