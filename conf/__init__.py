from pydantic import EmailStr, DirectoryPath
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    url_db: str = "mariadb+mariadbconnector://root:@127.0.0.1:3306/jiju"
    mail_username: str = ""
    mail_password: str = ""
    mail_server: str = "localhost"
    mail_port: int = 587
    mail_starttls: bool = False
    mail_ssl_tls: bool = False
    mail_debug: int = 0
    mail_from: EmailStr = "noreply@domain.local"
    mail_from_name: str = "Postmaster"
    template_folder: DirectoryPath = "email_templates"
    suppress_send: int = 0
    use_credentials: bool = False
    validate_certs: bool = True


settings = Settings()
