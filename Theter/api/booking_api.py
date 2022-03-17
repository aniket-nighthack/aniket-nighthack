from Theter.TCrud import *
from Theter.TModels import *
from Theter.TSchemas import *
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from Connection.database import *
from Common.APIResponses import Responses
from fastapi_utils import *
import shutil
from Theter.cruds.booking import *
from User.schemas import *
from Common import oauth, token

router = APIRouter(prefix='/user',
                   tags=["Booking"])


@router.post("/booking/new-booking/")
def createBooking(booking: CreateBooking, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return addBooking(session, booking)


@router.get("/booking")
def bookings(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return getAllBookings(session)


@router.get("/booking/user-booking/{uid}")
def userBooking(uid: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return getUsersBooking(session, uid)


@router.get("/cancelled-booking/{uid}")
def cancelBookings(uid: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return usersCancelBooking(session, uid)


@router.delete("/booking/cancel-booking/")
def cancelBooking(bookingid: int, seatid: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return CancelBooking(session, bookingid, seatid)
