from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.api.exception import APIException
from app.core import security
from app.crud import get_user_by_email, get_user_by_username
from app.schemas import UserBase , UserInfo, UserLogin, LoginResponse

router = APIRouter(tags=["login"])

@router.post("/recover-password")
async def recover_password():
    pass


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)) -> LoginResponse:

    if "@" in user.username:
        user_in = await get_user_by_email(email=user.username, db=db)
    else:
        user_in = await get_user_by_username(username=user.username, db=db)
        
    if not user_in:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid credentials"
        )

    if not security.verify_password(user.password, user_in.password_hash):
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid credentials"
        )
        
    
    content = LoginResponse(
        message=f"Hi {user_in.username}! Welcome to BanVia.VN",
        profile=UserInfo.model_validate(user_in),
    )
    
    access_token = security.create_access_token(
        subject={"id": user_in.id, "username": user.username, "role": user_in.role, "wid": user_in.wid},
        expires_timedelta=timedelta(minutes=30),
    )
    response = JSONResponse(content.model_dump())
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        path="/",
        secure=False,
        samesite="lax",
    )
    return response
