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
from Theter.TCrud import *
from Theter.cruds.show import *
from Theter.cruds.Theters import *

router = APIRouter(prefix='/theter',
                   tags=["Theters"])

auth = UserAuthentication()

# display all shows when user select a theter 
@router.get("/shows")
def theterShows(tid: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return getShowByTid(session, tid)

# display  all seats info when user select a show
@router.get("/shows/seats/{showid}")
def showSeats(showid:int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return seatsInfo(session, showid)