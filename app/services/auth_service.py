from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.users = UserRepository(db)

    def register(self, username: str, password: str):
        if self.users.get_by_username(username):
            raise HTTPException(status_code=409, detail="Пользователь уже существует")
        return self.users.create(username, hash_password(password))

    def login(self, username: str, password: str):
        user = self.users.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учётные данные")
        return create_access_token(user.id)

