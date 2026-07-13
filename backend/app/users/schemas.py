from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    address1: Optional[str] =None
    address2: Optional[str] =None
    address3: Optional[str] =None
    postcode: Optional[str] =None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    postcode: Optional[str] = None

class UserProfileResponse(BaseModel):
    first_name: str
    last_name: str
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    postcode: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RoleResponse(BaseModel):
    id: int
    name: str
    order: int

    model_config = ConfigDict(from_attributes=True)    

class RoleCreate(BaseModel):
    name: str
    order: int

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool
    date_registered: date
    userprofile: Optional[UserProfileResponse] = None
    role: Optional[RoleResponse] = None

    model_config = ConfigDict(from_attributes=True)

class UserResponseBasic(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserResponseRole(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role_name: str | None

class Token(BaseModel):
    access_token: str
    token_type: str


    
