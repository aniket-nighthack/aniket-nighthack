from typing import List
from User.exceptions import *
from User.schemas import *
from sqlalchemy.orm import Session
import secrets
from Common.APIResponses import Responses
from Common.Helper import *
from Common.token import *
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from User.model import *

from ..schemas import CreateLocation
from Theter.cruds.Theters import *

# get user last location
def getLastLocation(session: Session, user_id: int) -> LocationInfo:
    location = session.query(LocationInfo).filter(LocationInfo.user_id == user_id).first()
    return location


# add a location or update location
def updateLocation(session: Session, location: CreateLocation) -> LocationInfo:
    
    last_location = getLastLocation(session, location.user_id)
    if last_location:
        last_location.state = location.state
        last_location.city = location.city
        session.add(last_location)
        session.commit()
        session.refresh(last_location)

         # get a theters by state and city for the end-user   
        theters = theters_from_state_and_city(session, location.state, location.city)

        return Responses.success_result_with_data("User new location updated successfully", "theters", theters)
    else:
        new_location = LocationInfo(**location.dict())
        # new_location = LocationInfo(state=location.state, city=location.city, user_id=location.user_id)
        session.add(new_location)
        session.commit()
        session.refresh(new_location)

        # get a theters by state and city for the end-user   
        theters = theters_from_state_and_city(session, location.state, location.city)

        return Responses.success_result_with_data("User location added successfully", "theters", theters)

# when user skip the update location 
def oldLocation(session:Session, user_id:int) -> LocationInfo:
    last_location = getLastLocation(session, user_id)
    theters = theters_from_state_and_city(session, last_location.state, last_location.city)
    return theters