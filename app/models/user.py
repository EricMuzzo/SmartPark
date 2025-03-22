from pydantic import BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from pydantic.types import PaymentCardNumber
from typing import Optional, Annotated, List
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class PaymentMethod(BaseModel):
    card_number: PaymentCardNumber = Field(..., example="123456789999")
    expiry_month: Annotated[int, Field(..., gt=0, lt=13, example=3)]
    expiry_year: Annotated[int, Field(..., gt=2000, example=2027)]
    cvv: str = Field(..., example="123", max_length=3)


class UserBase(BaseModel):
    username: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    payment_methods: list[PaymentMethod] = Field(default=[], examples=[{"card_number": "123456789999", "expiry_month": 3, "expiry_year": 2027, "cvv": "123"}])


    
class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class UserCreate(UserBase):
    password: str
    
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
    
class UserCollection(BaseModel):
    users: List[User]
    
#Maybe move next 2 to separate file later on
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None
    
class UserSignUp(User):
    token: Token
    

class UserFilterParams(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None