from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# to create a user
class CreateUser(BaseModel):
    full_name : str 
    mobile : str

# to instance the user data
class User(CreateUser):
    id: int
    auth_token : str

    class Config:
        orm_mode = True

#  get a list of all users data
class PaginatedUserInfo(BaseModel):
    data: List[User]