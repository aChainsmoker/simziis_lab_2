from sqlalchemy.orm import Session

from app.infrastructure.models import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.get(UserModel, user_id)

    def get_by_username(self, username: str):
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def create(self, username: str, password_hash: str):
        user = UserModel(username=username, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

