from Theter.TCrud import *
from Theter.TModels import *
from Theter.TSchemas import *
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
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
    if booking.noOfSeats != len(booking.seatid):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Number of seats and seat ids must match")
    return addBooking(session, booking)


@router.get("/booking")
def bookings(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return getAllBookings(session)


@router.get("/booking/user-booking/{uid}")
def userBooking(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return getUsersBooking(session, current_user.id)


@router.get("/cancelled-booking/{uid}")
def cancelBookings(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return usersCancelBooking(session, current_user.id)


@router.delete("/booking/cancel-booking/")
def cancelBooking(bookingid: int, seatid: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return CancelBooking(session, bookingid, seatid)
