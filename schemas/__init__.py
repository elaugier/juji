from time import time

from pydantic import BaseModel


class AuthorizationCodeAdd(BaseModel):
    client_id: str
    redirect_url: str
    exp: time
    code_challenge: str
