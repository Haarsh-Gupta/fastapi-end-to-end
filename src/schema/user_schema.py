from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime

SPECIAL = set("!@#$%^&*")


def validate_password(password: str):
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")

    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter")

    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")

    if not any(c in SPECIAL for c in password):
        raise ValueError("Password must contain at least one special character !@#$%^&*")


# ---------------- REGISTER ----------------
class UserRegister(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=5, max_length=15)
    phone: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_check(cls, v: str):
        validate_password(v)
        return v


# ---------------- LOGIN ----------------
class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str = Field(min_length=5, max_length=15)

    @field_validator("password")
    @classmethod
    def password_check(cls, v: str):
        validate_password(v)
        return v

    @model_validator(mode="after")
    def check_login_identifier(self):
        if not self.email and not self.username:
            raise ValueError("Either email or username must be provided")
        return self


# ---------------- RESPONSE ----------------
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    username: str
    phone: Optional[str] = None
    admin: bool
    created_at: datetime

    class Config:
        from_attributes = True



#-----------------UPDATE----------------------
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_check(cls, v):
        if v is None:
            return v
        validate_password(v)
        return v

class UserPayload(BaseModel):
    id : int
    username : str
    email: EmailStr
    admin: bool

    class Config:
        from_attributes = True