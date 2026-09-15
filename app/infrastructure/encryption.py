from cryptography.fernet import Fernet, InvalidToken

from app.core.config import CONFIDENTIAL_DATA_KEY


_cipher = Fernet(CONFIDENTIAL_DATA_KEY.encode())


def encrypt(value: str) -> str:
    return _cipher.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    try:
        return _cipher.decrypt(value.encode()).decode()
    except InvalidToken:
        # Позволяет прочитать старые записи, созданные до включения шифрования.
        return value
