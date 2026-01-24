from pydantic import BaseModel
from typing import Optional , List , Dict
from .user_schema import UserOut
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title : Optional[str]
    content : Optional[str]
    published : Optional[bool]


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # to ref the user 
    owner : UserOut

    class Config:
        from_attributes = True
