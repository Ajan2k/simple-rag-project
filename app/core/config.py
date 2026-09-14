from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field,SecretStr, PostgresDsn

class Settings(BaseSettings):

    project_name: str = "Live-Streaming RAG API"
    version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$")
    debug: bool = Field(default=False)

    groq_api_key: SecretStr = Field(...,max_length=60)
    gemini_api_key: SecretStr | None = Field(default=None)

    postgres_uri: PostgresDsn = Field(default="postgresql+asyncpg://postgres:password@localhost:5432/rag_db" ,alias="DATABASE_URL")

    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2")
    FAISS_INDEX_PATH: str = Field(default="app/ml_assets/index.faiss")

    model_config: str = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8", extra="ignore")

settings = Settings()