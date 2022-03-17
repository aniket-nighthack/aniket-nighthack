from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from User.crud import *
from Connection.database import *
from User.schemas import *
from User.exceptions import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from User.userAuth import *
from Common import oauth, token

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
    if getUserByMobileNumber(session, user_info.mobile):
        return Responses.failed_result(f"{user_info.mobile} this mobile number is already used")
    else:
        try:
            new_user = create_user(session, user_info)
            return new_user
        except:
            raise UserNotAddError


@router.get("/auth/signin/{mobile}")
async def loginUser(mobile: int, session: Session = Depends(get_db)):
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
def getUserById(id: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return specificUser(session, id)
