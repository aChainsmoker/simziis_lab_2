# Lab 2

Приложение на FastAPI для регистрации, авторизации и управления конфиденциальными и неконфиденциальными данными.

## Запуск

```powershell
cd lab2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Открыть в браузере: http://127.0.0.1:8000

Access-токен хранится в `localStorage` браузера и передаётся в API через `Authorization: Bearer <token>`.

Настройки приложения загружаются из файла `.env` в корне проекта `lab2`.

Содержимое конфиденциальных данных шифруется Fernet перед сохранением в SQLite. Для production необходимо задать собственный ключ в переменной окружения `CONFIDENTIAL_DATA_KEY`. Ключ должен быть сгенерирован командой:

```powershell
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
