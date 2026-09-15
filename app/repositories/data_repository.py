from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.infrastructure.models import ConfidentialDataModel, PublicDataModel


class DataRepository:
    def __init__(self, db: Session, model, encryptor=None):
        self.db, self.model, self.encryptor = db, model, encryptor

    def list(self, user_id: int | None = None, search: str | None = None):
        query = self.db.query(self.model)
        if user_id is not None:
            query = query.filter(self.model.user_id == user_id)
        if search and not self.encryptor:
            pattern = f"%{search}%"
            query = query.filter(or_(self.model.title.ilike(pattern), self.model.content.ilike(pattern)))
        records = query.order_by(self.model.id.desc()).all()
        if self.encryptor:
            records = [record for record in records if not search or search.lower() in record.title.lower() or search.lower() in self.encryptor.decrypt(record.content).lower()]
            for record in records:
                record.content = self.encryptor.decrypt(record.content)
        return records

    def get(self, record_id: int):
        record = self.db.get(self.model, record_id)
        if record and self.encryptor:
            record.content = self.encryptor.decrypt(record.content)
        return record

    def create(self, user_id: int, title: str, content: str):
        if self.encryptor:
            content = self.encryptor.encrypt(content)
        record = self.model(user_id=user_id, title=title, content=content)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        if self.encryptor:
            record.content = self.encryptor.decrypt(record.content)
        return record

    def save(self, record, title: str, content: str):
        record.title, record.content = title, self.encryptor.encrypt(content) if self.encryptor else content
        self.db.commit()
        self.db.refresh(record)
        if self.encryptor:
            record.content = self.encryptor.decrypt(record.content)
        return record

    def delete(self, record):
        self.db.delete(record)
        self.db.commit()


def confidential_repository(db: Session):
    from app.infrastructure import encryption
    return DataRepository(db, ConfidentialDataModel, encryption)


def public_repository(db: Session):
    return DataRepository(db, PublicDataModel)
