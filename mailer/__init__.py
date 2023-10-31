from typing import List

from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from pydantic import BaseModel, EmailStr

import conf


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=conf.settings.mail_username,
    MAIL_PASSWORD=conf.settings.mail_password,
    MAIL_FROM=conf.settings.mail_from,
    MAIL_PORT=conf.settings.mail_port,
    MAIL_SERVER=conf.settings.mail_server,
    MAIL_FROM_NAME=conf.settings.mail_from_name,
    MAIL_DEBUG=conf.settings.mail_debug,
    MAIL_STARTTLS=conf.settings.mail_starttls,
    MAIL_SSL_TLS=conf.settings.mail_ssl_tls,
    USE_CREDENTIALS=conf.settings.use_credentials,
    VALIDATE_CERTS=conf.settings.validate_certs
)


async def simple_send(email: EmailSchema) -> bool:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.model_dump().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return True
