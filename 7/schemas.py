from typing import List, Union

from pydantic import BaseModel


class PasteBase(BaseModel):
    title: str
    content: str

class PasteCreate(PasteBase):
    pass

class Paste(PasteBase):
    id: int
    owner_id = int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    pastes: List[Paste] = []

    class Config:
        orm_mode = True

class UserDetail(User):
    salt: str

