from typing import List
from .model import *
from .exceptions import *
from .schemas import *
from sqlalchemy.orm import Session
import secrets
from Common.APIResponses import Responses
from Common.Helper import *
from Common.token import *
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


def getUsers(session: Session) -> List[UsersInfo]:
    users = session.query(UsersInfo).all()
    return Responses.success_result_with_data("Users Found", "UserData", users)


# get user by mobile number
def getUserByMobileNumber(session: Session, mobile: str) -> UsersInfo:
    user = session.query(UsersInfo).filter(UsersInfo.mobile == mobile).first()
    return user


# get user by id
def getUserById(session: Session, id: int) -> UsersInfo:
    user = session.query(UsersInfo).filter(UsersInfo.id == id).first()
    return user


# add a new user
def create_user(session: Session, user: CreateUser):
    token = getAuthToken()

    new_user = UsersInfo(full_name=user.full_name, mobile=user.mobile, auth_token=token,
                         hash_password=Hash.bcrypt(user.password), user_type=user.user_type)
    session.add(new_user)
    session.commit()
    return Responses.success_result("New user added successfully")


#  login the user
def login_user(session: Session, mobile: String) -> UsersInfo:
    login = session.query(UsersInfo).filter(UsersInfo.mobile == mobile).first()
    if login:
        return Responses.success_result_with_data("User Found Successfully", "UserData", login)
    else:
        return Responses.failed_result("This mobile number is not register.please enter registerd number")


# to update the user information
def user_update(session: Session, user_info: CreateUser) -> UsersInfo:
    user = getUserByMobileNumber(session, user_info.mobile)
    if user:
        user.full_name = user_info.full_name
        user.mobile = user_info.mobile
        user.password = user_info.password

        session.add(user)
        session.commit()
        session.refresh(user)
        return Responses.success_result_with_data("User Information Updated", "userData", user)
    else:
        return Responses.failed_result("Failed to update user information")


# delete user account
def delete_user(session: Session, id: int) -> UsersInfo:
    user = getUserById(session, id)
    if user:
        session.delete(user)
        session.commit()
        return Responses.success_result("User account deleted successfully")
    else:
        return Responses.failed_result("Failed to delete user account")


# get a specific user account details
def specificUser(session: Session, id: int) -> UsersInfo:
    user = getUserById(session, id)
    if user:
        return Responses.success_result_with_data("User account details found", "userDetails", user)
    else:
        return Responses.failed_result("Invalid user details")