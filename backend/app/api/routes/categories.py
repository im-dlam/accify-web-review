from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.api.deps import get_db , get_current_user
from app.api.exception import APIException
from app.schemas import CategoryPublic , Category , CategoryCreate , UserPublic
from app.models import ProductCategory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , update
from sqlalchemy.orm import load_only
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/categories", tags=["category"])

@router.get("/", response_model=CategoryPublic)
async def get_categories(db: AsyncSession =  Depends(get_db)):
    """Lấy danh sách loại mặt hàng

    Args:
        db (AsyncSession, optional): _description_. Defaults to Depends(get_db).
    """
    stmt = (
        select(ProductCategory)
        .options(load_only(
            ProductCategory.id, ProductCategory.name,
            ProductCategory.keyword, ProductCategory.color
        ))
        .offset(0)
        .limit(100)
    )
    
    result = await db.execute(stmt)
    categories = result.scalars().all()
    
    return CategoryPublic(success=True, categories=categories)

@router.post("/", response_model=Category, status_code=201)
async def create_category(
    *, 
    category : CategoryCreate, 
    db:AsyncSession = Depends(get_db), 
    current_user: Annotated[UserPublic ,Depends(get_current_user)]):
    
    if current_user.role != "admin":
        raise APIException(status_code=status.HTTP_423_LOCKED, message="Access is not permitted")
    
    category_new = ProductCategory(**category.model_dump())
    try:
        db.add(category_new)
        await db.commit()
        await db.refresh(category_new)    
    except IndentationError as e:
        await db.rollback()
        msg = str(e.orig).lower()
        if "name" in msg:
            raise APIException(status_code=400, message="Name already exists")
        
        if "keyword" in msg:
            raise APIException(status_code=400, message="Keyword already exists")
        
        raise APIException(status_code=400, message="Please double check your name or keyword.")
        
        
    return category_new

@router.delete("/", response_model=Category)
async def delete_category(
    *,
    category : CategoryCreate,
    db:AsyncSession = Depends(get_db),
    current_user: Annotated[UserPublic ,Depends(get_current_user)]):
    pass

@router.put("/", response_model=Category)
async def update_category(
    *,
    category: Category,
    db: AsyncSession = Depends(get_db),
    user: Annotated[UserPublic, Depends(get_current_user)]):
    
    if user.role != "admin":
        raise APIException(status_code=status.HTTP_423_LOCKED, message="Access is not permitted")
    stmt = (
        update(ProductCategory).where(ProductCategory.id == category.id).values(category.model_dump())
    )
    
    await db.execute(stmt)
    await db.commit()

    result = await db.execute(select(ProductCategory).where(ProductCategory.id == category.id))
    
    updated_category = result.scalar_one_or_none()
    if not updated_category:
        raise APIException(status_code=404, message="Category not found")
    
    return updated_category