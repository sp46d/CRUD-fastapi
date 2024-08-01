from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    created_at: datetime
        

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[int] = None