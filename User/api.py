from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from User.crud import *
from Connection.database import *
from User.schemas import *
from User.exceptions import *

router = APIRouter()

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 

@cbv(router)
class Users():
    session: Session = Depends(get_db)

    @router.get("/users")
    def getAllUsers(self):
        users = getUsers(self.session)
        return users


# add new user / registration
@router.post("/users/add_new")
def add_new_user(user_info: CreateUser, session:Session = Depends(get_db)):
    try:
        new_user = create_user(session, user_info)
        return new_user
    except:
        raise UserNotAddError     

#  login the user
@router.get("/loginUser")
async  def loginUser(mobile:int, session:Session = Depends(get_db)):
    try:
        login = login_user(session, mobile)
        return login
    except:
        raise UserNotFoundError    