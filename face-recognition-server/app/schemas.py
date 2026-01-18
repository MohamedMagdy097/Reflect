from pydantic import BaseModel, EmailStr
from typing import Optional


class SignupResponse(BaseModel):
    success: bool
    message: str
    user_id: int
    email: str


class SigninResponse(BaseModel):
    success: bool
    message: str
    user_id: int
    email: str
    similarity_score: Optional[float] = None


class ErrorResponse(BaseModel):
    detail: str
