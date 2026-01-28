from fastapi import APIRouter, Depends , status
from fastapi.responses import JSONResponse
# from app.api.routes import login
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from app.api.deps import get_db, get_current_user
from app.core import security
from app.crud import create_user , get_user_by_username
from app.models import User
from app.schemas import (
    UserSignup,
    UserInfo,
    UserPublic
)
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserPublic)
async def read_user_me(user = Depends(get_current_user)):
    return user

@router.post("/logout")
async def logout():
    res = JSONResponse({"success": True})
    # res.delete_cookie(key="access_token",path="/", samesite="lax")
    res.delete_cookie(
        key="access_token",
        httponly=True,
        path="/",
        secure=False,
        samesite="lax",
    )
    return res

@router.post("/signup", response_model=UserInfo , status_code=201)
async def signup(user: UserSignup, db: AsyncSession = Depends(get_db)) -> UserInfo:
    
    role = "admin"
    new_user = User(username=user.username, email=user.email, password_hash=security.get_password(user.password), role=role)
    
    await create_user(user_create=new_user, db=db)
    access_token = security.create_access_token(
        subject={
            "id": new_user.id,
            "username": new_user.username,
            "role": role
        },
        expires_timedelta=timedelta(minutes=30),
    )
    
    
    user_info = UserInfo.model_validate(new_user)
    resp = JSONResponse(content=user_info.model_dump(), status_code=201)
    access_token = security.create_access_token(
        subject={"id": new_user.id, "username": user.username, "role": role},
        expires_timedelta=timedelta(minutes=30),
    )
    resp.set_cookie(key="access_token",value=access_token,
                    httponly=True,
                    path="/",
                    secure=False, # TODO: Change to True in prod
                    samesite="lax",
                    max_age=1800) # 30min
    return resp