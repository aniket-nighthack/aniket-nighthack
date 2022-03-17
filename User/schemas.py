from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


# to create a user
class CreateUser(BaseModel):
    full_name: str
    mobile: str
    password: str
    user_type: str


# to instance the user data
class User(CreateUser):
    id: int
    auth_token: str
    hash_password: str

    class Config:
        orm_mode = True


#  get a list of all users data
class PaginatedUserInfo(BaseModel):
    data: List[User]


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[str] = None
    name: Optional[str] = None


# location create
class CreateLocation(BaseModel):
    state: str
    city: str
    user_id: int


class Location(CreateLocation):
    id: int

    class Config:
        orm_mode = True
