from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

current_file = Path(__file__).resolve()
current_dir = current_file.parent
env_path = current_dir / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")

    BASE_URL: str
    TIMEOUT: float


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
