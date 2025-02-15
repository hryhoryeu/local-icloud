from pydantic_settings import BaseSettings


class Secrets(BaseSettings):
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: str
    PG_DB: str
    SECRET_KEY: str

    DEBUG: bool = False

    def generate_db_url(self):
        return f"postgresql+psycopg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"

    class Config:
        env_file = ".env"


secrets = Secrets()
