from typing import Annotated

from fastapi import Request, Form, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from auth import verify_client_info, authenticate_user_credentials, generate_authorization_code, process_redirect_url, \
    verify_authorization_code, generate_access_token, JWT_LIFE_SPAN
from template import templates

__all__ = [
    "router"
]

router = APIRouter(prefix="/oidc", tags=["oidc"])


class ErrorResponse(BaseModel):
    error: str


@router.get("/auth", response_class=HTMLResponse)
async def auth(request: Request, client_id: str, redirect_uri: str, code_challenge: str):
    if None in [client_id, redirect_uri, code_challenge]:
        err_item = ErrorResponse()
        err_item.error = "invalid request"
        json_data = jsonable_encoder(err_item)
        return JSONResponse(content=json_data, status_code=400)

    if not verify_client_info(client_id=client_id, redirect_uri=redirect_uri):
        err_item = ErrorResponse()
        err_item.error = "invalid client"
        json_data = jsonable_encoder(err_item)
        return JSONResponse(content=json_data, status_code=400)

    return templates.TemplateResponse(name="ac_pkce_grant_access.html", context={
        "request": request,
        "client_id": client_id,
        "redirect_url": redirect_uri,
        "code_challenge": code_challenge
    })


@router.post('/signin')
def signIn(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        client_id: Annotated[str, Form()],
        redirect_url: Annotated[str, Form()],
        code_challenge: Annotated[str, Form()]
):
    if None in [username, password, client_id, redirect_url, code_challenge]:
        err_item = ErrorResponse()
        err_item.error = "invalid request"
        json_data = jsonable_encoder(err_item)
        return JSONResponse(content=json_data, status_code=400)

    if not verify_client_info(client_id, redirect_url):
        err_item = ErrorResponse()
        err_item.error = "invalid client"
        json_data = jsonable_encoder(err_item)
        return JSONResponse(content=json_data, status_code=400)

    if not authenticate_user_credentials(username, password):
        err_item = ErrorResponse()
        err_item.error = "access denied"
        json_data = jsonable_encoder(err_item)
        return JSONResponse(content=json_data, status_code=401)

    authorization_code = generate_authorization_code(client_id, redirect_url,
                                                     code_challenge)

    url = process_redirect_url(redirect_url, authorization_code)

    return RedirectResponse(url=url, status_code=303)


@router.post('/token')
def exchange_for_token(
        grant_type: Annotated[str, Form()],
        scope: Annotated[str, Form()],
        code: Annotated[str, Form()],
        client_id: Annotated[str, Form()],
        redirect_uri: Annotated[str, Form()],
        code_verifier: Annotated[str, Form()]
):
    if None in [code, client_id, code_verifier, redirect_uri]:
        err_item = ErrorResponse()
        err_item.error = "invalid request"
        json_data = jsonable_encoder(err_item)
        return JSONResponse(content=json_data, status_code=400)

    if not verify_authorization_code(code, client_id, redirect_uri,
                                     code_verifier):
        err_item = ErrorResponse()
        err_item.error = "access denied"
        json_data = jsonable_encoder(err_item)
        return JSONResponse(content=json_data, status_code=401)

    access_token = generate_access_token()
    json_data = jsonable_encoder({
        "access_token": access_token,
        "token_type": "JWT",
        "expires_in": JWT_LIFE_SPAN
    })
    return JSONResponse(content=json_data, status_code=200)


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse(name="signup.html", context={"request": request})
