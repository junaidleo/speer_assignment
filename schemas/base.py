from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class NoteBase(BaseModel):
    notes: str

class UserCreate(UserBase):
    password: str

class Note(NoteBase):
    id: Optional[int] = 0
    created_by: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str
