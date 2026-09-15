from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.infrastructure.security import decode_access_token
from app.infrastructure.token_blacklist import revoked_tokens
from app.repositories.user_repository import UserRepository


def current_user(request: Request, db: Session = Depends(get_db)):
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется access-токен")
    token = authorization[7:]
    if token in revoked_tokens:
        raise HTTPException(status_code=401, detail="Токен отозван")
    try:
        user_id = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Недействительный access-токен")
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user


def token_from_request(request: Request) -> str:
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Требуется access-токен")
    return authorization[7:]

