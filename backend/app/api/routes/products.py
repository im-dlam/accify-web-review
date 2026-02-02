from fastapi import APIRouter, Depends, Request, status, Body
from fastapi.responses import Response
from app.api.deps import get_db, get_current_user, get_current_admin
from app.schemas import (
    Product as ProductSchemas,
    ProductPublic,
    UserPublic,
    ProductCreate,
    ItemDelete,
)
from app.models import Product as ProductModels
from sqlalchemy import select, update
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.exception import APIException
from sqlalchemy.exc import IntegrityError
from typing import Annotated

router = APIRouter(prefix="/products", tags=["product"])


@router.get("/")
async def get_products(db: AsyncSession = Depends(get_db)) -> ProductPublic:
    """
    Lấy danh sách sản phẩm
    """
    stmt = (
        select(ProductModels)
        # Load các column chỉ định tránh load hết lag
        .options(
            load_only(
                ProductModels.id,
                ProductModels.name,
                ProductModels.subtitle,
                ProductModels.description,
                ProductModels.stock,
                ProductModels.price,
                ProductModels.discount,
                ProductModels.country,
                ProductModels.icons,
                ProductModels.time,
                ProductModels.image_url,
            )
        )
        # Số bản ghi bỏ qua trước khi lấy kết quả
        .offset(0)
        # Sau này scale thêm phân trang sẽ sửa sau
        .limit(100)
    )

    result = await db.execute(stmt)
    items = result.scalars().all()

    return ProductPublic(success=True, products=items)


@router.post("/", response_model=ProductSchemas, status_code=201)
async def create_product(
    *,
    product: ProductCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    user: UserPublic = Depends(get_current_user),
) -> ProductSchemas:
    """
    Tạo sản phẩm
    """

    if user.role != "admin":
        raise APIException(
            status_code=status.HTTP_423_LOCKED, message="Access is not permitted"
        )
    product_new = ProductModels(**product.model_dump())
    try:
        db.add(product_new)
        await db.commit()
        await db.refresh(product_new)
    except IntegrityError as e:
        msg = str(e.orig).lower()
        if "foreignkeyviolationerror" in msg:
            raise APIException(
                status_code=400, message="Please double check category_id"
            )

        raise APIException(status_code=400, message=msg)

    return product_new


@router.delete("/{product_id}", response_model=ItemDelete)
async def delete_product(
    *,
    product_id: int,
    db: AsyncSession = Depends(get_db),
    user: Annotated[UserPublic, Depends(get_current_admin)],
):
    """
    Xóa sản phẩm theo id
    """
    result = await db.execute(
        select(ProductModels).where(ProductModels.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise APIException(status_code=404, message="Not found product")

    product_data = ProductSchemas.model_validate(product)

    try:
        await db.delete(product)
        await db.commit()
    except IntegrityError as e:
        msg = str(e.orig).lower()
        if "foreignkeyviolationerror" in msg:
            raise APIException(
                status_code=400,
                message="The product still has accounts. Please move or delete them first.",
            )

    return ItemDelete(message="Item deleted successfully", item=product_data)


@router.put("/")
async def update_product(
    *,
    product: ProductSchemas,
    db: AsyncSession = Depends(get_db),
    user: Annotated[UserPublic, Depends(get_current_admin)],
):
    """Cập nhật sản phẩm"""
    filtered_product = {k: v for k, v in product.model_dump().items() if v != None}

    stmt = (
        update(ProductModels)
        .where(ProductModels.id == product.id)
        .values(filtered_product)
    )

    try:
        await db.execute(stmt)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise APIException(status_code=400, message="Duplicate value or invalid data")

    result = await db.execute(
        select(ProductModels).where(ProductModels.id == product.id)
    )

    updated_product = result.scalar_one_or_none()
    if not updated_product:
        raise APIException(status_code=404, message="Product not found")

    return updated_product
