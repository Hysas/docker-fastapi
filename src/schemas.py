from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# User
class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(User):
    pass

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    Votes: int

    class Config:
        orm_mode = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# Vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)