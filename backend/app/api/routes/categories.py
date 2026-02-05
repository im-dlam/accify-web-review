from typing import Annotated, Any
from fastapi import APIRouter, Depends, status, Body
from app.api.deps import get_db, get_current_user, get_current_admin
from app.api.exception import APIException
from app.schemas import CategoryPublic, Category, CategoryCreate, ItemDelete, UserPublic
from app.models import ProductCategory, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import load_only
from sqlalchemy.exc import IntegrityError
from asyncpg import ForeignKeyViolationError
router = APIRouter(prefix="/categories", tags=["category"])


@router.get("/", response_model=CategoryPublic)
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Lấy danh sách loại mặt hàng

    Args:
        db (AsyncSession, optional): _description_. Defaults to Depends(get_db).
    """
    stmt = (
        select(ProductCategory)
        .options(
            load_only(
                ProductCategory.id,
                ProductCategory.name,
                ProductCategory.keyword,
                ProductCategory.color,
            )
        )
        .offset(0)
        .limit(100)
    )

    result = await db.execute(stmt)
    categories = result.scalars().all()

    return CategoryPublic(success=True, categories=categories)


@router.post("/", response_model=Category, status_code=201)
async def create_category(
    *,
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[UserPublic, Depends(get_current_admin)],
):
    """Tạo danh mục mới"""

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

        raise APIException(
            status_code=400, message="Please double check your name or keyword."
        )

    return category_new


@router.delete("/{category_id}", response_model=ItemDelete)
async def delete_category(
    *,
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Annotated[UserPublic, Depends(get_current_admin)],
) -> Any:
    """Xóa danh mục theo id"""

    try:
        result = await db.execute(
            delete(ProductCategory)
            .where(ProductCategory.id == category_id)
            .returning(
                ProductCategory.id,
                ProductCategory.name,
            )
        )

        row = result.first()
        if not row:
            raise APIException(status_code=404, message="Category not found")

        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        if isinstance(e.orig, ForeignKeyViolationError):
            raise APIException(
                status_code=400,
                message="The category still has products. Please move or delete them first.",
            )




    return ItemDelete(message="Item deleted successfully", item={"id":row.id, "name":row.name})


@router.put("/", response_model=Category)
async def update_category(
    *,
    category: Category,
    db: AsyncSession = Depends(get_db),
    user: Annotated[UserPublic, Depends(get_current_admin)],
):
    """Cập nhật sản phẩm theo id"""
    filtered_category = {k: v for k, v in category.model_dump().items() if v != None}
    stmt = (
        update(ProductCategory)
        .where(ProductCategory.id == category.id)
        .values(filtered_category)
    )

    try:
        await db.execute(stmt)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise APIException(status_code=400, message="Duplicate value or invalid data")

    result = await db.execute(
        select(ProductCategory).where(ProductCategory.id == category.id)
    )

    updated_category = result.scalar_one_or_none()
    if not updated_category:
        raise APIException(status_code=404, message="Category not found")

    return updated_category
