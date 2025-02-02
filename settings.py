from pydantic_settings import BaseSettings


class Secrets(BaseSettings):
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: str
    PG_DB: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


secrets = Secrets()
