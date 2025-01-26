from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESS_USER: str
    POSTGRESS_PASSWORD: str
    POSTGRESS_HOST: str
    POSTGRESS_PORT: str
    POSTGRESS_DB: str


settings = Settings()
