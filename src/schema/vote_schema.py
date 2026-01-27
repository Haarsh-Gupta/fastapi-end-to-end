from pydantic import BaseModel, Field
from typing import Literal

class VoteRequest(BaseModel):
    post_id: int
    vote: int = Field(le= -1 , ge= 1)

class VoteResponse(BaseModel):
    post_id : int 
    user_id : int 
    vote : int = Literal[-1 , 1]
    