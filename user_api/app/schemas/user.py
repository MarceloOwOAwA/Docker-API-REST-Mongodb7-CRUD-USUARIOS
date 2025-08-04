from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List
import re
from uuid import UUID
from datetime import datetime

class Phone(BaseModel):
    number: str = Field(..., example="1234567")
    citycode: str = Field(..., example="1")
    contrycode: str = Field(..., example="57")

class UserCreate(BaseModel):
    name: str = Field(..., example="Juan Rodriguez")
    email: EmailStr = Field(..., example="juan@rodriguez.org")
    password: str = Field(..., min_length=6, example="Password123")
    phones: List[Phone]

    @field_validator('email')
    def email_must_match_regex(cls, v):
        v = v.lower()  # Convierte el email a minúsculas
        pattern = r'^[\w\.-]+@[\w\.-]+\.cl$'
        if not re.match(pattern, v):
            raise ValueError("El correo debe tener un formato válido y terminar en '.cl'")
        return v

    @field_validator('password')
    def password_complexity(cls, v):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=(?:.*\d){2,}).{6,}$'
        if not re.match(pattern, v):
            raise ValueError(
                "La contraseña debe tener al menos una mayúscula, letras minúsculas y dos números"
            )
        return v

class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phones: List[Phone]
    created: datetime
    modified: datetime
    last_login: datetime
    token: str
    isactive: bool

    model_config = {
        "from_attributes": True,
    }

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="juan@rodriguez.org")

    @field_validator('email')
    def email_to_lower(cls, v):
        return v.lower()

    password: str = Field(..., example="Password123")

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    phones: List[Phone]
    created: datetime
    modified: datetime
    last_login: datetime
    token: str
    isactive: bool

    model_config = {
        "from_attributes": True,
    }
