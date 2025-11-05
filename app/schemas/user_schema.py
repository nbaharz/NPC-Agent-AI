from pydantic import BaseModel, EmailStr,Field

class UserCreate(BaseModel):
    username: str = Field(..., alias="username")
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel): #this should return jwt token later
    id: str
    username: str
    email: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str