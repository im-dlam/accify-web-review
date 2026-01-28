
from aiohttp import TraceRequestChunkSentParams
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Boolean, Enum,
    DateTime, Date ,Float
    )
from app.core.db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, default="")
    role = Column(Enum("admin","member","distributor","collaborator", name="user_role") , default="member")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False , unique=True)
    keyword = Column(String, unique=True, index=True, nullable=False)
    color = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now , onupdate=datetime.now)

    
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('product_categories.id'), index=True)
    name = Column(String, nullable=False)
    price = Column(Float, default=999999)
    stock = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    discount = Column(Integer, default=0)
    subtitle = Column(String, default="")
    description = Column(String, default="")
    country = Column(String, default="")
    image_url = Column(String, default="")
    icons = Column(String, default="")
    time = Column(Date, default=datetime.today) # mô tả thời gian cho sản phẩm
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class ProductInventory(Base):
    __tablename__ = "product_inventories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    product = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    balance = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), unique=True)
    amount = Column(Float)
    status = Column(Enum("pending","success","failed", name="payment_status"))
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.now)