from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "DocChat API"
    app_env: str = "development"
    app_port: int = 8000

    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "docchat"
    postgres_user: str = "docchat"
    postgres_password: str = "docchat"

    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    chunk_size: int = 900
    chunk_overlap: int = 150
    top_k: int = 5

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
