
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Boolean,
    Enum,
    DateTime,
    Date,
    Float,
    CheckConstraint
)
from app.core.db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, default="")
    role = Column(
        Enum("admin", "member", "distributor", "collaborator", name="user_role"),
        default="member",
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    keyword = Column(String, unique=True, index=True, nullable=False)
    color = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, default=999999)
    stock = Column(Integer, default=0)
    sold = Column(Integer, default=0 , )
    discount = Column(Integer, default=0)
    subtitle = Column(String, default="")
    description = Column(String, default="")
    country = Column(String, default="")
    image_url = Column(String, default="")
    icons = Column(String, default="")
    time = Column(Date, default=datetime.today)  # mô tả thời gian cho sản phẩm
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint("stock >= 0", "check_stock_non_negative"),
        CheckConstraint("price >= 0" , "check_price_non_negative"),
    )

class ProductInventory(Base):
    __tablename__ = "product_inventories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    data = Column(String, index=True)
    status = Column(
        Enum("available", "sold", "refunded", "locked", name="inventory_status"),
        default="available",
        index=True,
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint("length(data) > 0", name="check_inventory_data_length"),
    )

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    balance = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint("balance >= 0", name="check_wallet_balance"),
    )

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    amount = Column(Float)
    status = Column(Enum("pending", "success", "failed", name="payment_status"))
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)
    
    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_payment"),
    )

class UserPurchase(Base):
    __tablename__ = "user_purchases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    name = Column(String)
    quantity = Column(Integer)
    total_price = Column(Integer)
    data = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=True)

    __table_args__ = (
        CheckConstraint("length(data) > 0", name="check_purchase_data_length"),
    )