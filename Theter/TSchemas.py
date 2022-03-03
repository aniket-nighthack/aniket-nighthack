from typing import Optional, List
from pydantic import BaseModel

# for create and update
class CreateUpdateTheter(BaseModel):
    t_name : str
    t_address : str
    t_contact : str
    opening_time : str
    closing_time : str

class Theter(CreateUpdateTheter):
    id : int
    auth_token : str

    class Config:
        orm_mode = True

# # the list of data
# class PaginatedTheter(BaseModel):
#     data = List[Theter]

