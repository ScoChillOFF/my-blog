import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    test_db_name: str = 'test_db'

    def get_db_url(self) -> str:
        return f'postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'
    
    def get_test_db_url(self) -> str:
        return f'postgresql+psycopg://{self.db_user}:{self.db_password}@{self.db_host}/{self.test_db_name}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()