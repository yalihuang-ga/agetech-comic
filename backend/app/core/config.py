"""應用程式設定。

透過環境變數（或 .env 檔）載入設定。
複製 .env.example 為 .env 並填入實際值。
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 應用程式
    app_name: str = "AgeTech Comic Backend"
    debug: bool = False

    # LINE Bot 憑證（於 LINE Developers Console 取得）
    line_channel_access_token: str = ""
    line_channel_secret: str = ""

    # AI 圖片 / 文字生成服務
    # 例如 OpenAI、Google Gemini、或自架模型的 API 金鑰
    ai_api_key: str = ""
    ai_api_base_url: str = ""

    # CORS：允許前端存取的來源
    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    """回傳快取後的設定實例。"""
    return Settings()
