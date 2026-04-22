from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    full_name: str


class TokenPayload(BaseModel):
    sub: EmailStr
    role: str = Field(pattern="^(admin|user)$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
