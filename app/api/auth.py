from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.dependencies import current_user, token_from_request
from app.api.schemas import Credentials
from app.infrastructure.database import get_db
from app.infrastructure.token_blacklist import revoked_tokens
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Авторизация"])


@router.post("/register", status_code=201)
def register(data: Credentials, db: Session = Depends(get_db)):
    user = AuthService(db).register(data.username, data.password)
    return {
        "id": user.id,
        "username": user.username,
        "access_token": AuthService(db).login(data.username, data.password),
        "token_type": "bearer",
    }


@router.post("/login")
def login(data: Credentials, db: Session = Depends(get_db)):
    return {"access_token": AuthService(db).login(data.username, data.password), "token_type": "bearer"}


@router.post("/logout")
def logout(request: Request, user=Depends(current_user)):
    revoked_tokens.add(token_from_request(request))
    return {"message": "Выход выполнен"}


@router.get("/me")
def me(user=Depends(current_user)):
    return {"id": user.id, "username": user.username}
