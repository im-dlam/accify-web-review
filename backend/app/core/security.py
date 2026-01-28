from typing import Any
from pwdlib import PasswordHash
from datetime import datetime , timedelta, timezone
import jwt

ALGORITHM = "HS256"
SECRET_KEY   = "9f3c8e6b1a4d2e8f9c7b0a5e1f4c9d8b7e2a6f0c1d9e4b8a7c6e5d3f2b1a"
password_hash = PasswordHash.recommended()


def create_access_token(subject: str | Any, expires_timedelta: timedelta) -> str:
    expires = datetime.now(timezone.utc) + expires_timedelta
    to_encode = {**subject, "exp": expires}
    return jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

def get_password(pwd: str) -> str:
    return  password_hash.hash(pwd)

def verify_password(plain_pwd, hashed_pwd) -> bool:
    return password_hash.verify(plain_pwd , hashed_pwd)
