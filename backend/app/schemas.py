from datetime import datetime
from typing import Annotated, Any, Dict , Literal, Optional, List, Set
import uuid
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field, model_validator, EmailStr
from datetime import date

class UserBase(BaseModel):
    username : Annotated[str , Field(min_length=4, max_length=36)]

class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    role: str
    wallet_id: int
    class Config:
        from_attributes = True
        
class UserLogin(UserBase):
    password: Annotated[str, Field(min_length=5, max_length=18)]

    @model_validator(mode="after")
    def check_username_or_email(self):
        if not self.username:
            raise ValueError("You must enter your username or email address.")
        return self
    
    
class UserSignup(UserLogin):
    email: Annotated[str , Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", default="string")] 
    
    @model_validator(mode="after")
    def normalize_email(self):
        self.email = self.email.strip().lower()
        if not self.email:
            raise ValueError("Email is required")
        return self
        
    
class UserInfo(BaseModel):
    id: int
    username: str
    balance: float = 0.0
    # is_active: bool
    class Config:
        from_attributes = True
        
        
class LoginResponse(BaseModel):
    status : bool = True
    message: str
    profile: Optional[UserInfo] = None

class ItemDelete(BaseModel):
    status : bool = True
    message: str
    item: Any = {}

    class Config:
        from_attributes = True
        
class Product(BaseModel):
    id: int
    name: str = None
    subtitle: str = None
    description: str =  None
    stock: int = None
    price: float = None
    discount: int = None
    country: str = None
    image_url: str = None
    icons: str = None
    time: date = None
    
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    """
    - name: Tên cho đơn hàng
    - subtitle: Tên mô tả cụ thể
    - description: Mô tả chi tiết hơn cho đơn hàng
    >>> {
    >>> "name" : "Tài khoản facebook ngâm"
    >>> "subtitle" : "Tài khoản 2Fa | Full Info ..."
    >>> "description" : "Tài khoản reg từ tháng 6, bao ngâm, bao back, định dạng .v.v.v"   
    >>> }
    """
    category_id: int
    name: str 
    subtitle: str 
    description: str
    stock: int = 0
    price: float
    discount: int
    country: str
    image_url: str = ""
    icons: str
    time: date
    
    class Config:
        from_attributes = True

class ProductPublic(BaseModel):
    success: bool
    products: List[Product] = Field(default_factory=list)
    
class Category(BaseModel):
    id: int 
    name: str = None
    keyword: str =  None
    color: str = None
    
    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    keyword: str
    color: str = "#34A0FF"

class CategoryPublic(BaseModel):
    success: bool
    categories: List[Category] = Field(default_factory=list)
    
class Inventory(BaseModel):
    id: int
    product_id: int
    data: str
    status: Literal["available","sold","locked","refunded"] 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True
        
class InventoryCreate(BaseModel):
    product_id: int
    items: List[str] | str 

    class Config:
        from_attributes = True
        
class InventoryPublic(BaseModel):
    status: bool = True
    data: List[Inventory] = []
    
    class Config:
        from_attributes = True
        extra = "allow"

class Messages(BaseModel):
    status: bool = True
    message: str = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        extra = "allow" #TODO: Allow them cac attr khac
    

# Wallet
class WalletDeposit(BaseModel):
    transaction_id: uuid.UUID
    content: str
    balance: float
    
    @model_validator(mode="after")
    def check_balance(self):
        if self.balance <= 0:
            raise ValueError("Balance more than 10.000đ")
        return self
    
    class Config:
        from_attributes = True


class WalletPublic(BaseModel):
    id: int
    balance: float
    