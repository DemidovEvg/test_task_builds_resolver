from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import FilePath


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", str_to_upper=True
    )

    path_to_builds: FilePath = BASE_DIR / "builds/builds.yaml"
    path_to_tasks: FilePath = BASE_DIR / "builds/tasks.yaml"
    reload_for_every_request: bool = False


settings = Settings()
