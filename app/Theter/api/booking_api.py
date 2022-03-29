from app.Theter.TCrud import *
from app.Theter.TModels import *
from app.Theter.TSchemas import *
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from app.Connection.database import *
from app.Common.APIResponses import Responses
from fastapi_utils import *
from fastapi_utils.tasks import repeat_every
import shutil
from app.Theter.cruds.booking import *
from app.User.schemas import *
from app.Common import oauth, token

router = APIRouter(prefix='/user',
                   tags=["Booking"])


@router.post("/booking/new-booking/")
def createBooking(booking: CreateBooking, session: Session = Depends(get_db),
                  current_user: User = Depends(oauth.get_current_user)):
    if booking.noOfSeats != len(booking.seatid):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Number of seats and seat ids must match")
    for i in booking.seatid:
        seatAvailableOrNot(session, i)
    return addBooking(session, booking, current_user.id)


@router.get("/booking")
def bookings(session: Session = Depends(get_db), current_user: User = Depends(oauth.check_if_admin)):
    return getAllBookings(session)


@router.get("/old-booking/")
def userOldBooking(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return getUserOldBookings(session, current_user.id)


@router.get("/booking/user-booking/{uid}")
def userBooking(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return getUsersBooking(session, current_user.id)


@router.get("/booking_seats/")
def bookingSeats(bookingid: int, session: Session = Depends(get_db),
                 current_user: User = Depends(oauth.get_current_user)):
    return getSeatsByBooking(session, bookingid)


@router.get("/cancelled-booking/{uid}")
def cancelBookings(session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return usersCancelBooking(session, current_user.id)


@router.post("/change_booking_status/{bookingid}")
def changeBooking(bookingid: int, session: Session = Depends(get_db),
                  current_user: User = Depends(oauth.get_current_user)):
    return updateBookingUpdate(session, bookingid)


@router.delete("/booking/cancel-booking/")
def cancelBooking(bookingid: int, session: Session = Depends(get_db),
                  current_user: User = Depends(oauth.get_current_user)):
    return CancelBooking(session, bookingid)



