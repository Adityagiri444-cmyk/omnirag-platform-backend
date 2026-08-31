from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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

# Schema for JWT token response — now includes refresh_token too
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

# Schema for requesting a new access token using a refresh token
class RefreshRequest(BaseModel):
    refresh_token: str

# Schema for document response - what we send back after upload/listing
class DocumentResponse(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    owner_id: int

    class Config:
        from_attributes = True