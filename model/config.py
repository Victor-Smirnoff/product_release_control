from pydantic_settings import BaseSettings
from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = getenv('DB_HOST')
    DB_PORT: int = getenv('DB_PORT')
    DB_USER: str = getenv('DB_USER')
    DB_PASS: str = getenv('DB_PASS')
    DB_NAME: str = getenv('DB_NAME')

    @property
    def data_base_url(self) -> str:
        #  postgresql+asyncpg://product_manager:0000@localhost:5432/product_release_control
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    db_echo: bool = True


settings = Settings()
