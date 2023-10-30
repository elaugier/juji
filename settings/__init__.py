from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url_db: str = "mariadb+mariadbconnector://root:@127.0.0.1:3306/jiju"


settings = Settings()
