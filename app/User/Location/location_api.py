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
from app.User.Location.location_crud import *

router = APIRouter(prefix='/user',
                   tags=["Location"])

auth = UserAuthentication()


@router.put("/location/updateLocation")
def update(location: CreateLocation, session: Session = Depends(get_db),
           current_user: User = Depends(oauth.get_current_user)):
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
# @router.get("/location/movies/")
# def movieLocation(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
#     return moviesByLocation(session, current_user.id)
