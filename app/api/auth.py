from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.api.dependencies import current_user, token_from_request
from app.api.schemas import Credentials
from app.core.config import ACCESS_TOKEN_COOKIE, ACCESS_TOKEN_EXPIRE_MINUTES
from app.infrastructure.database import get_db
from app.infrastructure.token_blacklist import revoked_tokens
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Авторизация"])


@router.post("/register", status_code=201)
def register(data: Credentials, response: Response, db: Session = Depends(get_db)):
    user = AuthService(db).register(data.username, data.password)
    token = AuthService(db).login(data.username, data.password)
    response.set_cookie(ACCESS_TOKEN_COOKIE, token, httponly=True, secure=False, samesite="lax", max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return {"id": user.id, "username": user.username}


@router.post("/login")
def login(data: Credentials, response: Response, db: Session = Depends(get_db)):
    token = AuthService(db).login(data.username, data.password)
    response.set_cookie(ACCESS_TOKEN_COOKIE, token, httponly=True, secure=False, samesite="lax", max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return {"message": "Авторизация выполнена"}


@router.post("/logout")
def logout(request: Request, response: Response, user=Depends(current_user)):
    revoked_tokens.add(token_from_request(request))
    response.delete_cookie(ACCESS_TOKEN_COOKIE)
    return {"message": "Выход выполнен"}


@router.get("/me")
def me(user=Depends(current_user)):
    return {"id": user.id, "username": user.username}
