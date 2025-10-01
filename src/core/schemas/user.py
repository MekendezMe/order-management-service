from pydantic import BaseModel

from . import Role


class UserRead(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    age: int
    role: Role
    confirmed: bool
    is_active: bool


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    age: int
    role: str

class UserUpdate(BaseModel):
    id: int
    email: str
    password: str
    name: str
    surname: str
    age: int

class UserLogin(BaseModel):
    email: str
    password: str