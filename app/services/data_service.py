from fastapi import HTTPException


class DataService:
    def __init__(self, repository):
        self.repository = repository

    def list(self, user_id: int | None, search: str | None):
        return self.repository.list(user_id, search)

    def create(self, user_id: int, title: str, content: str):
        return self.repository.create(user_id, title, content)

    def update(self, record_id: int, user_id: int, title: str, content: str):
        record = self.repository.get(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Запись не найдена")
        if record.user_id != user_id:
            raise HTTPException(status_code=403, detail="Нет доступа к записи")
        return self.repository.save(record, title, content)

    def delete(self, record_id: int, user_id: int):
        record = self.repository.get(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Запись не найдена")
        if record.user_id != user_id:
            raise HTTPException(status_code=403, detail="Нет доступа к записи")
        self.repository.delete(record)

