from pydantic import BaseModel


class RefreshResponse(BaseModel):
    access_token: str


class LoginResponse(BaseModel):
    access_token: str
    user_id: int
    username: str


class MessageResponse(BaseModel):
    message: str
