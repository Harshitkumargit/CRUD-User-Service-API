from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    name: str
    age: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    age: Optional[int] = None

    class Config:
        orm_mode = True