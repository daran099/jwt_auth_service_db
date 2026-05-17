from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: str


class RegisterResponse(BaseModel):
    id: int
    username: str
