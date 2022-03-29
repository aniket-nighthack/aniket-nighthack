from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from app.User.crud import *
from app.Connection.database import *
from app.User.schemas import *
from app.User.exceptions import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.User.userAuth import *
from app.Common import oauth, token
from app.Theter.TCrud import *
from app.Theter.cruds.show import *
from app.Theter.cruds.Theters import *

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