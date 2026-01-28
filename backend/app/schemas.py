from email.policy import default
from typing import Annotated, Dict , Literal, Optional, List
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
    balance: int = 0
    is_active: bool
    class Config:
        from_attributes = True
        
        
class LoginResponse(BaseModel):
    status : Literal["success", "error"]
    message: str
    profile: Optional[UserInfo] = None


class Product(BaseModel):
    id: int
    name: str
    subtitle: str
    description: str
    stock: int = 0
    price: float
    discount: int
    country: str
    image_url: str = ""
    icons: str
    time: date = Field(default_factory=date.today)
    
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
    name: str
    keyword: str
    color: str = "#34A0FF"
    
    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    keyword: str
    color: str = "#34A0FF"

class CategoryDelete(BaseModel):
    pass

class CategoryPublic(BaseModel):
    success: bool
    categories: List[Category] = Field(default_factory=list)