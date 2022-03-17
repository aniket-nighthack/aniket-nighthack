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
from User.Location.location_crud import  *
router = APIRouter(prefix='/user',
                   tags=["Location"])

auth = UserAuthentication()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.put("/location/updateLocation")
def update(location:CreateLocation, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return updateLocation(session, location)

# when user skip to the update location we use the last location
@router.get("/location/theters/{userid}")
def userOldLocationTheters(user_id: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return oldLocation(session, user_id)