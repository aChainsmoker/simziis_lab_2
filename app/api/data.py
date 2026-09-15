from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import current_user
from app.api.schemas import DataInput
from app.infrastructure.database import get_db
from app.infrastructure.models import ConfidentialDataModel, PublicDataModel
from app.repositories.data_repository import DataRepository
from app.infrastructure import encryption
from app.services.data_service import DataService


def make_router(path: str, model, owner_only: bool):
    router = APIRouter(prefix=f"/api/{path}", tags=[path])

    def service(db):
        return DataService(DataRepository(db, model, encryption if owner_only else None))

    @router.post("", status_code=201)
    def create(data: DataInput, db: Session = Depends(get_db), user=Depends(current_user)):
        record = service(db).create(user.id, data.title, data.content)
        return record

    @router.get("")
    def list_data(search: str | None = Query(default=None), db: Session = Depends(get_db), user=Depends(current_user)):
        records = service(db).list(user.id if owner_only else None, search)
        return records

    @router.get("/{record_id}")
    def get_one(record_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
        record = service(db).repository.get(record_id)
        if not record:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Запись не найдена")
        if owner_only and record.user_id != user.id:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail="Нет доступа к записи")
        return record

    @router.put("/{record_id}")
    def update(record_id: int, data: DataInput, db: Session = Depends(get_db), user=Depends(current_user)):
        return service(db).update(record_id, user.id, data.title, data.content)

    @router.delete("/{record_id}", status_code=204)
    def delete(record_id: int, db: Session = Depends(get_db), user=Depends(current_user)):
        service(db).delete(record_id, user.id)

    return router


confidential_router = make_router("confidential", ConfidentialDataModel, True)
public_router = make_router("public-data", PublicDataModel, False)
