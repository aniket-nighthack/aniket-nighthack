from app.Theter.TCrud import *
from app.Theter.TModels import *
from app.Theter.TSchemas import *
from fastapi import APIRouter, Depends, HTTPException,  File, UploadFile
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from app.Connection.database import *
from app.Common.APIResponses import Responses
from fastapi_utils import *
import shutil
from app.User.crud import *
from app.Common import oauth, token
from app.Theter.cruds.screens import *
from app.Theter.cruds.seats import *

router = APIRouter(prefix='/theter',
    tags=["Seats"])

# add new seat
@router.post("/screen/seat/create-screen/")
def createSeat(seat: CreateSeat, session:Session = Depends(get_db),current_user: User = Depends(oauth.get_current_user)):
    return addSeats(session, seat)

# update seat information
@router.put("/screen/seat/update-seat")
def updateSeat(seat:CreateSeat, id:int , session:Session = Depends(get_db),current_user: User = Depends(oauth.get_current_user)):
    return updateSeatInfo(session, seat, id)

# delete seat information
@router.delete("/screen/seat/delete-seat/{seatid}")
def deleteSeat(id:int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return deleteSeatInfo(session, id)

# seats by screen-id  
@router.get("/screen/seat/screen-seats/{screenid}")
def screenSeats(screenid:int, session:Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return seatsByScreenid(session, screenid) 