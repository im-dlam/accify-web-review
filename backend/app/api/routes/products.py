from fastapi import APIRouter, Depends, status 
from fastapi.responses import Response
from app.api.deps import get_db, get_current_user
from app.schemas import Product as ProductSchemas, ProductPublic, UserPublic , ProductCreate
from app.models import Product  as ProductModels
from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.exception import APIException
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/products", tags=["product"])



@router.get('/')
async def get_products(db: AsyncSession = Depends(get_db)) -> ProductPublic:
    """
    Lấy danh sách sản phẩm
    """
    stmt = (
        select(ProductModels)
        # Load các column chỉ định tránh load hết lag
        .options(load_only(
                ProductModels.id, ProductModels.name, ProductModels.subtitle,
                 ProductModels.description, ProductModels.stock, ProductModels.price,
                 ProductModels.discount, ProductModels.country, ProductModels.icons,
                 ProductModels.time, ProductModels.image_url
        ))
        # Số bản ghi bỏ qua trước khi lấy kết quả
        .offset(0)
        # Sau này scale thêm phân trang sẽ sửa sau
        .limit(100)
    )
    
    result = await db.execute(stmt)
    items = result.scalars().all()

    return ProductPublic(success=True, products=items)

@router.post('/', response_model=ProductSchemas, status_code=201)
async def create_product(
    *,
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user: UserPublic = Depends(get_current_user)
    ) -> ProductSchemas:
    """
    Tạo sản phẩm
    """
    if user.role != "admin":
        raise APIException(status_code=status.HTTP_423_LOCKED, message="Access is not permitted")
    product_new = ProductModels(**product.model_dump())
    try:
        db.add(product_new)
        await db.commit()
        await db.refresh(product_new)
    except IntegrityError as e:
        msg = str(e.orig).lower()
        
        raise APIException(status_code=400, message=msg)
    

    
    return product_new

@router.delete('/{id}')
async def delete_product():
    """
    Xóa sản phẩm theo id
    """

@router.put('/{id}')
async def update_product():
    """
    Cập nhật sản phẩm
    """