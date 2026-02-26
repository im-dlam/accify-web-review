from typing import Literal
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, update
from app.models import User, Wallet
from sqlalchemy.exc import IntegrityError
from app.api.exception import APIException
from app.schemas import WalletPublic



async def create_user(*, user_create: User, db: AsyncSession) -> bool:
    """
    Tạo user mới trong database.
    
    Args:
        user_create: User object cần tạo
        db: Database session
        
    Returns:
        True : tạo thành công
        
    Example:
        >>> user = User(username="dinhlam", email="dinhlam@example.com", password_hash="hash123")
        >>> success = await create_user(user_create=user, db=db)
    """
    try:
        db.add(user_create)
    except IntegrityError as e:
        await db.rollback()
        msg = str(e.orig).lower()
        if "username" in msg:
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message="Username already exists")
        
        if "email" in msg:
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message="Email already exists")
        
        raise APIException(status_code=status.HTTP_400_BAD_REQUEST, message="Please double check your username or email.")
        
    return True

async def get_user_by_email(*, email: str, db: AsyncSession) -> User | None:
    """
    Lấy user theo email.
    
    Args:
        email: Email cần tìm
        db: Database session
        
    Returns:
        User object hoặc None nếu không tìm thấy
        
    Example:
        >>> user = await get_user_by_email(email="dinhlam@example.com", db=db)
    """
    result = await db.execute(text("""
                                select u.*, w.id as wid, w.balance as balance
                                from users u join wallets w
                                on u.id = w.user_id
                                where u.email = :email;
                                """),
                            params={'email':email})
    return result.first()


async def get_user_by_username(*, username: str, db: AsyncSession) -> User | None:
    """
    Lấy user theo username.
    
    Args:
        username: Username cần tìm
        db: Database session
        
    Returns:
        User object hoặc None nếu không tìm thấy
        
    Example:
        >>> user = await get_user_by_username(username="dinhlam", db=db)
    """
    result = await db.execute(text("""
                                select u.*, w.id as wid, w.balance as balance
                                from users u join wallets w
                                on u.id = w.user_id
                                where u.username = :username;
                                """),
                            params={'username':username})
    return result.first()

async def get_user_by_id(*, user_id: str, db: AsyncSession) -> User | None:
    """
    Lấy user theo user id.
    
    Args:
        user_id: id của user cần tìm
        db: Database session
        
    Returns:
        User object hoặc None nếu không tìm thấy
        
    Example:
        >>> user = await get_user_by_id(user_id="uuuuu-wwww-mmmm-wwww", db=db)
    """
    result = await db.execute(text("""
                                select u.*, w.id as wid, w.balance as balance
                                from users u join wallets w
                                on u.id = w.user_id
                                where u.id = :user_id;
                                """),
                            params={'user_id':user_id})
    return result.first()

async def update_user(*,
                      user_id: str, 
                      key: Literal["password_hash", "full_name", "role", "is_active"],
                      value: str,
                      db: AsyncSession) -> bool:
    """
    Cập nhật thông tin user.
    
    Args:
        username: username của user cần cập nhật
        key: Tên trường cần cập nhật
        value: Giá trị mới
        db: Database session
        
    Returns:
        True nếu cập nhật thành công
        
    Example:
        >>> success = await update_user(user_id="123", key="full_name", value="John Doe", db=db)
    """
    statement = update(User).where(User.id == user_id).values({key: value})
    result = await db.execute(statement)
    await db.commit()
    
    return result.rowcount > 0
    
