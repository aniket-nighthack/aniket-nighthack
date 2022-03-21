from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from User.crud import *
from Connection.database import *
from User.schemas import *
from User.exceptions import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from User.userAuth import *
from Common import oauth, token, Helper
import re

router = APIRouter(prefix='/user',
                   tags=["Users"])

auth = UserAuthentication()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/all-users/")
def getAllUsers(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    users = getUsers(session)
    return users


# add new user / registration
@router.post("/add-new-user/")
def add_new_user(user_info: CreateUser, session: Session = Depends(get_db)):
    number_valid = getUserByMobileNumber(session, user_info.mobile)
    if number_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"This mobile number already used please try another mobile or login")
    phoneNumRegex = re.compile(r'^(\+[0-9]{2}[- ]?)?[0-9]{10}$')
    if not phoneNumRegex.match(str(user_info.mobile)):
        raise HTTPException(status_code=400,
                            detail=f"Phone number invalid {user_info.mobile}")
    if user_info.user_type == "admin" or user_info.user_type == "EndUser":
        return create_user(session, user_info)
    else:
        raise HTTPException(status_code=400, detail="user type missmatch please try again")




@router.get("/auth/signin/{mobile}")
async def loginUser(mobile: int, session: Session = Depends(get_db)):
    if Helper.numberValidation(mobile):
        try:
            login = login_user(session, mobile)
            return login
        except:
            raise UserNotFoundError


@router.put("/update_user_details")
def update(user: CreateUser, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return user_update(session, user)


@router.delete("/delete_user/{id}")
def deleteUser(id: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return delete_user(session, id)


@router.get("/get_user_by_id/{id}")
def getUserById(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return specificUser(session, current_user.id)
