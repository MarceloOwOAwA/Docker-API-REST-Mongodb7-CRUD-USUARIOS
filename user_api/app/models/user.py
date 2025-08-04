from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    username: str
    hashed_password: str

    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "email": "marcelo@mail.com",
                "username": "marcelo123",
                "hashed_password": "hashedvalue"
            }
        }
    }
