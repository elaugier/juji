import base64
import hashlib
import json
import time
import urllib.parse as urlparse
from datetime import datetime

import jwt
from cryptography.fernet import Fernet

from models import AuthorizationCode, SessionLocal

# KEY = Fernet.generate_key()
KEY = b'YHD1m3rq3K-x6RxT1MtuGzvyLz4EWIJAEkRtBRycDHA='

f = Fernet(KEY)

ISSUER = 'sample-auth-server'
CODE_LIFE_SPAN = 600
JWT_LIFE_SPAN = 1800

authorization_codes = {}

with open('private.key', 'rb') as file:
    private_key = file.read()


def verify_client_info(client_id: str, redirect_uri: str):
    return True


def authenticate_user_credentials(username, password):
    return True


def generate_code_challenge(code_verifier):
    m = hashlib.sha256()
    m.update(code_verifier.encode())
    code_challenge = m.digest()
    return base64.b64encode(code_challenge, b'-_').decode().replace('=', '')


def generate_access_token():
    payload = {
        "iss": ISSUER,
        "exp": time.time() + JWT_LIFE_SPAN
    }

    access_token = jwt.encode(payload, private_key, algorithm='RS256')

    return access_token


def generate_authorization_code(client_id, redirect_url, code_challenge):
    # f = Fernet(KEY)
    authorization_code = f.encrypt(json.dumps({
        "client_id": client_id,
        "redirect_url": redirect_url,
    }).encode())

    authorization_code = base64.b64encode(authorization_code, b'-_').decode().replace('=', '')

    expiration_date = time.time() + CODE_LIFE_SPAN

    newAuthCode = AuthorizationCode(
        authorization_code=authorization_code,
        client_id=client_id,
        redirect_url=redirect_url,
        expiration_date=datetime.fromtimestamp(expiration_date),
        code_challenge=code_challenge
    )

    session = SessionLocal()

    session.add(newAuthCode)
    session.commit()

    return authorization_code


def verify_authorization_code(authorization_code, client_id, redirect_url,
                              code_verifier):
    # f = Fernet(KEY)
    session = SessionLocal()
    record = session.query(AuthorizationCode).filter(AuthorizationCode.authorization_code == authorization_code).first()
    if not record:
        return False

    client_id_in_record = record.client_id
    redirect_url_in_record = record.redirect_url
    exp = record.expiration_date
    code_challenge_in_record = record.code_challenge

    if client_id != client_id_in_record or \
            redirect_url != redirect_url_in_record:
        return False

    if datetime.timestamp(exp) < time.time():
        return False

    code_challenge = generate_code_challenge(code_verifier)
    if code_challenge != code_challenge_in_record:
        return False

    session.delete(record)
    session.commit()

    return True


def process_redirect_url(redirect_url, authorization_code):
    # Prepare the redirect URL
    url_parts = list(urlparse.urlparse(redirect_url))
    queries = dict(urlparse.parse_qsl(url_parts[4]))
    queries.update({"code": authorization_code})
    url_parts[4] = urlparse.urlencode(queries)
    url = urlparse.urlunparse(url_parts)
    return url
