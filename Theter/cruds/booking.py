from sqlalchemy.orm import Session, joinedload
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
from Theter.cruds.Theters import *
from Theter.cruds.seats import *


# get a all bookings
def getAllBookings(session: Session) -> BookingInfo:
    bookings = session.query(BookingInfo).all()
    return Responses.success_result_with_data("Bookings find", "Bookings", bookings)


# get specific user booking
def getUsersBooking(session: Session, uid: int) -> BookingInfo:
    booking = session.query(ShowsInfo, BookingInfo).join(BookingInfo).options(
        joinedload(ShowsInfo.movie),
        joinedload(ShowsInfo.screens),
        joinedload(ShowsInfo.theter),
    ).filter(BookingInfo.uid == uid).all()

    return Responses.success_result_with_data("User Booking Find", "BookindDetails", booking)


# create/ add a new booking by end-user
def addBooking(session: Session, booking: CreateBooking) -> BookingInfo:
    add_booking = BookingInfo(**booking.dict())
    session.add(add_booking)
    session.commit()
    session.refresh(add_booking)
    session.begin_nested()

    seat = session.query(SeatsInfo).filter(SeatsInfo.id == booking.seatid).first()
    if seat:
        seat.seat_status = False
        session.add(seat)
        session.commit()
        return Responses.success_result("Booking is created")
    else:
        return Responses.failed_result("Faild to create booking")

    return add_booking

# cancel the user booking
def CancelBooking(session: Session, bookingid: int, seatid: int) -> BookingInfo:
    booking = session.query(BookingInfo).filter(BookingInfo.id == bookingid).first()
    if booking:
        booking.booking_status = False
        session.add(booking)
        session.commit()

        seat = session.query(SeatsInfo).filter(SeatsInfo.id == seatid).first()
        if seat:
            seat.seat_status = True
            session.add(seat)
            session.commit()
            return Responses.success_result("Booking Cancelled Successfully")
    return Responses.failed_result("Failed to cancelled booking")


# show how many bookings cancel by user
def usersCancelBooking(session: Session, uid: int) -> BookingInfo:
    user = session.query(BookingInfo).filter(BookingInfo.uid == uid, BookingInfo.booking_status == False).all()

    if user:
        return Responses.success_result_with_data("User's cancelled booking found", "cancelledBooking", user)
    else:
        return Responses.failed_result("Users don't have a cancelled bookings")


def getAllSeats(session: Session) -> SeatsInfo:
    seats = session.query(SeatsInfo, func.count(SeatsInfo.seat_status).label('avilable seats')).filter(
        SeatsInfo.seat_status == True).all()
    return seats
