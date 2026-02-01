from app.core.db import AsyncSessionLocal 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from app.api.exception import APIException
from app.core import security
from app.crud import get_user_by_username
from app.models import User
from app.schemas import UserPublic
import jwt



SECRET_KEY   = "9f3c8e6b1a4d2e8f9c7b0a5e1f4c9d8b7e2a6f0c1d9e4b8a7c6e5d3f2b1a"


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> UserPublic:
    token = request.cookies.get("access_token")
    if not token:
        raise APIException(
            status_code=401,
            message="Missing access token"
        )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[security.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise APIException(status_code=401, message="Token expired!")
    except jwt.PyJWTError:
        raise APIException(status_code=401, message="Token error!")
    username = payload.get("username")
    if not username:
        raise APIException(status_code=401, message="Invalid token payload")
    
    user = await get_user_by_username(username=username, db=db)
    if not user:
        raise APIException(status_code=404, message="User not found")
    
    if not user.is_active:
        raise APIException(status_code=403, message="User inactive")
        
    return UserPublic(
        id=user.id,
        username=user.username,
        role=user.role,
        email=user.email
    )


async def get_current_admin(request: Request, db: AsyncSession = Depends(get_db)) -> UserPublic:
    user = await get_current_user(request, db)
    if user.role != "admin":
        raise APIException(status_code=423, message="Access is not permitted")
    
    return user