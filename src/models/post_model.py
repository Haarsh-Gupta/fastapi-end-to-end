from pydantic import BaseModel
from typing import Optional , List , Dict


class Post(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(Post):
    pass 