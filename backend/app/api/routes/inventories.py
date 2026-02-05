from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, text, bindparam, delete
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from app.api.deps import get_db, get_current_admin
from app.schemas import (
    UserPublic, InventoryPublic,
    InventoryCreate, Messages, Inventory
)
from app.models import ProductInventory
from app.api.exception import APIException
from asyncpg import ForeignKeyViolationError


router = APIRouter(prefix="/inventories", tags=["inventories"])

@router.get("/", response_model=InventoryPublic)
async def get_inventory_private(
    *,
    db: AsyncSession = Depends(get_db),
    user: UserPublic = Depends(get_current_admin)
):

    result = await db.execute(select(ProductInventory))
    data = result.scalars().all()
    total = len(data)
    inventories = [Inventory.from_orm(obj) for obj in data]  # Pydantic v2
    return InventoryPublic(data=inventories, total=total)
    
@router.get("/{inventory_id}")
async def get_inventory(
    *,
    inventory_id: int,
    db: AsyncSession = Depends(get_db),
    user: UserPublic = Depends(get_current_admin)
):
    
    result = await db.execute(select(ProductInventory).where(ProductInventory.id == inventory_id))
    data = result.scalar_one_or_none()
    if not data:
        raise APIException(status_code=404, message="Not Found ID!")
    return data
    
@router.post("/")
async def create_inventories(
    *,
    inventories: InventoryCreate,
    db: AsyncSession = Depends(get_db),
    user: UserPublic = Depends(get_current_admin)
):
    items = inventories.items
    if isinstance(items, str):
        items = [items]

    if not items:
        raise APIException(400, "No items to insert")

    atomic_command = text("""
    WITH insert_inventory AS (
        INSERT INTO product_inventories (product_id, data)
        SELECT
            :product_id,
            unnest(:items)
        -- ON CONFLICT (product_id,data) DO NOTHING
        RETURNING 1
    )
    UPDATE products
    SET stock = stock + (SELECT COUNT(*) FROM insert_inventory)
    WHERE id = :product_id
    RETURNING stock
    """).bindparams(
        bindparam("items", type_=ARRAY(TEXT))
    )

    try:
        result = await db.execute(atomic_command, {"product_id": inventories.product_id, "items": items})
    except IntegrityError as e:
        msg = str(e.orig).lower()
        if "is not present in table" in msg:
            raise APIException(status_code=404, message="Not Found Product!")
        
    new_stock = result.scalar()
    await db.commit()
    
    return Messages(message=f"Inserted success!", stock=new_stock)

@router.delete("/{inventory_id}")
async def delete_inventory(
    *,
    inventory_id: int,
    db: AsyncSession = Depends(get_db),
    user: UserPublic = Depends(get_current_admin)
    ):
    

    try:
        result =  await db.execute(
            delete(ProductInventory)
            .where(ProductInventory.id == inventory_id)
            .returning(
                ProductInventory.id
            )
        )
        row = result.first()
        if not row:
            raise APIException(status_code=404, message="Not found id")
        await db.commit()
    except IntegrityError as e:
        if isinstance(e.orig, ForeignKeyViolationError):
            raise APIException(status_code=400, message="")
        print(e.orig)
    
    return Messages(message="Inventory deleted successfully", inventory={"id":row.id})