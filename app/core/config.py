from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_VERSION: str = "v1"

    BASE_URL: str = "api"

    API_URL: str | None

    @validator("API_URL", pre=True)
    def assemble_api_url(cls, v: str, values: dict[str, str]) -> str:
        return f"{values.get('BASE_URL')}/{values.get('API_VERSION')}"

    ENV: str | None
    IS_PRODUCTION: bool = False

    @validator("IS_PRODUCTION", pre=True)
    def set_production_if_needed(cls, v: bool, values: dict[str, str]) -> bool:
        if values.get("ENV") == "prod":
            return True
        return v

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: list[str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

        raise ValueError(
            f"BACKEND_CORS_ORIGINS must be a string or list of strings, got {type(v)}"
        )

    PROJECT_NAME: str = "URL Shortener"

    POSTGRES_HOST: str | None
    POSTGRES_USER: str | None
    POSTGRES_PASSWORD: str | None
    POSTGRES_DB: str | None
    POSTGRES_PORT: int | None

    SQLALCHEMY_DATABASE_URI: str | None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER", "postgres"),
            password=values.get("POSTGRES_PASSWORD", "postgres"),
            host=values.get("POSTGRES_HOST") or "localhost",
            path=f"/{values.get('POSTGRES_DB', 'db')}",
            port=f"{values.get('POSTGRES_PORT') or 5432}",
        )

        if not isinstance(dsn, str):
            raise ValueError(
                "Could not assemble a valid Postgres DSN. "
                "Please check your settings."
            )

        return dsn

    class Config:
        case_sensitive: bool = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
