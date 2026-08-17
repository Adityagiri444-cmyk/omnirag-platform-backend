from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for registering a new user
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: Optional[str] = "user"

# Schema for login
class UserLogin(BaseModel):
    email: str
    password: str

# Schema for response - what we send back
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

# Schema for JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str