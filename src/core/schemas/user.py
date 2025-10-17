from pydantic import BaseModel

from . import Role


class UserRead(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    age: int
    role: str
    confirmed: bool
    is_active: bool


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    age: int

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

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserRead