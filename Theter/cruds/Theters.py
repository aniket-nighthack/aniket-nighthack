from sqlalchemy.orm import Session , joinedload
import secrets 
from Common.APIResponses import Responses
from typing import List
from Theter.TModels import *
from Theter.TSchemas import *
from Common.Helper import *
from Theter.TExceptions import *
from fastapi import HTTPException
from sqlalchemy.sql.expression import func, case
from sqlalchemy.sql.expression import false, true
from Theter.cruds.show import *


# get all theters from the state and city
def theters_from_state_and_city(session:Session, state:str, city:str) -> ThetersInfo:
    theters = session.query(ThetersInfo).filter(ThetersInfo.state == state, ThetersInfo.city == city).all()
    return theters

# get theter by id  
def getThereById(session:Session, tid:int) -> ThetersInfo:
    theter = session.query(ThetersInfo).filter(ThetersInfo.id == tid).first()
    return theter

# display all seats information when user select the show 
def seatsInfo(session:Session, show_id:int) -> ShowsInfo:
    return showSeats(session,show_id)