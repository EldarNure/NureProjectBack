from pydantic import BaseModel, UUID4, EmailStr
from typing import Dict, List, Optional
from user.config import settings

class UserPrivate(BaseModel):
    id: UUID4
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    roles: List[str] = ["user"]
    email: EmailStr = ""
    phone_number: Optional[str] = ""
    password: Optional[str] = ""

class UserPublic(BaseModel):
    id: UUID4
    first_name: Optional[str]
    last_name: Optional[str]
    roles: List[str] = ["user"]
    email: EmailStr
    phone_number: Optional[str]

class CreateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    phone_number: Optional[str]
    password: Optional[str]


class PatchUser(BaseModel):
    id: UUID4
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    phone_number: Optional[str]
    password: Optional[str]


class Login(BaseModel):
    email: Optional[str]
    password: Optional[str]