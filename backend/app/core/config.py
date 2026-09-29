from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str

    GROQ_API_KEY: str
    GROQ_MODEL: str

    GEMINI_API_KEY: str
    GEMINI_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
