from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr

class UserIn(UserBase):
    password:str

class UserOut(UserBase):
    created_at:datetime

class SugarLevelIn(BaseModel):
    slevel:int

class SugarLevelOut(SugarLevelIn):
    id: int
    created_at:datetime

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int|None=None


