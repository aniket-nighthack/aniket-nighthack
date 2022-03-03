from typing import List
from .model import *
from .exceptions import *
from .schemas import *
from sqlalchemy.orm import Session 
import secrets 
from Common.APIResponses import Responses
from Common.Helper import *


def getUsers(session:Session) ->List[UsersInfo]:
    users = session.query(UsersInfo).all()
    return Responses.success_result_with_data("Users Found", "UserData", users)

# add a new user
def create_user(session: Session, user: CreateUser):
    token = getAuthToken()
    new_user = UsersInfo(full_name=user.full_name, mobile=user.mobile, auth_token=token)
    session.add(new_user)
    session.commit()
    return Responses.success_result("New user added successfully")

#  login the user 
def login_user(session:Session, mobile:String) -> UsersInfo:
    login = session.query(UsersInfo).filter(UsersInfo.mobile == mobile).first()
    if login:
        return Responses.success_result_with_data("User Found Successfully", "UserData", login)
    else:
        return Responses.failed_result("This mobile number is not register.please enter registerd number")    