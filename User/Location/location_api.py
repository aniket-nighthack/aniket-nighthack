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


@router.put("/location/updateLocation")
def update(location:CreateLocation, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    if not location.state.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid state name provide please try again")
    if not location.city.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid city name provide please try again")
    return updateLocation(session, location, current_user.id)

# when user skip to the update location we use the last location
@router.get("/location/theters/{userid}")
def userOldLocationTheters(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return oldLocation(session, current_user.id)

# get movies by location of user
@router.get("/location/movies/")
def movieLocation(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return moviesByLocation(session, current_user.id)