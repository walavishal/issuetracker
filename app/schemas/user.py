from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool

    class Config:
        from_attributes = True



class UpdateProfile(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class ChangePassword(BaseModel):
    current_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)