from sqlalchemy.orm import Session, joinedload
import secrets
from Common.APIResponses import Responses
from typing import List
from Theter.TModels import *
from Theter.TSchemas import *
from Common.Helper import *
from Theter.TExceptions import *
from fastapi import HTTPException
from sqlalchemy.sql.expression import func, case, literal_column
from sqlalchemy.sql.expression import false, true
from Theter.cruds.Theters import *
from Theter.cruds.seats import *
from datetime import datetime, date
from sqlalchemy import cast, Date


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
    ).filter(BookingInfo.uid == uid, cast(BookingInfo.create_at,Date) == date.today(), BookingInfo.booking_status == True).all()

    return Responses.success_result_with_data("User Booking Find", "BookindDetails", booking)

# get user's old bookings
def getUserOldBookings(session: Session, uid: int) -> BookingInfo:
    booking = session.query(ShowsInfo, BookingInfo).join(BookingInfo).options(
        joinedload(ShowsInfo.movie),
        joinedload(ShowsInfo.screens),
        joinedload(ShowsInfo.theter),
    ).filter(BookingInfo.uid == uid, cast(BookingInfo.create_at,Date) != date.today()).all()

    return booking


# get seats details by booking
def getSeatsByBooking(session: Session, booking_id: int) -> ShowSeatBookingInfo:
    seats = session.query(ShowSeatBookingInfo).options(joinedload(ShowSeatBookingInfo.seatDeatils))\
                                     .filter(ShowSeatBookingInfo.booking_id == booking_id).all()
    return seats

# create/ add a new booking by end-user
def addBooking(session: Session, booking: CreateBooking, uid:int) -> BookingInfo:
    add_booking = BookingInfo(showid=booking.showid, noOfSeats=booking.noOfSeats, uid=uid,  booking_status=True)
    session.add(add_booking)
    session.commit()
    session.refresh(add_booking)
    session.begin_nested()


    for i in booking.seatid:
        seat = session.query(SeatsInfo).filter(SeatsInfo.id == i).first()
        if seat:
            seat.seat_status = False
            session.add(seat)
            session.commit()

            add_multiple = addShowBooking(session, add_booking.id, i)
            
        else:
            return deleteAllBookings(session, add_booking.id)
            

    return Responses.success_result("Booking is created")

# cancel the user booking
def CancelBooking(session: Session, bookingid: int) -> BookingInfo:
    # booking = session.query(BookingInfo).filter(BookingInfo.id == bookingid).first()
    # if booking:
    #     booking.booking_status = False
    #     session.add(booking)
    #     session.commit()

    #     seat = session.query(SeatsInfo).filter(SeatsInfo.id == seatid).first()
    #     if seat:
    #         seat.seat_status = True
    #         session.add(seat)
    #         session.commit()
    #         return Responses.success_result("Booking Cancelled Successfully")
    # return Responses.failed_result("Failed to cancelled booking")

    seats = session.query(ShowSeatBookingInfo).filter(ShowSeatBookingInfo.booking_id == bookingid).all()
    for i in seats:
        seat = session.query(SeatsInfo).filter(SeatsInfo.id == i.seat_id).first()
        if seat:
            seat.seat_status = True
            session.add(seat)
            session.commit()

            # remove a seat and booking id from showSeatBookingInfo
            removeBookedSeats(session, i.seat_id)

        else:
            return Responses.failed_result("Failed to cancelled booking")  

    booking = session.query(BookingInfo).filter(BookingInfo.id == bookingid).first()
    if booking:
        booking.booking_status = False
        session.add(booking)
        session.commit()
        return Responses.success_result("Booking Cancelled Successfully")       
    else:
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

#  add a booking into showsBooking to multiple seats book by one booking
def addShowBooking(session: Session, booking_id:int, seat_id: int) -> ShowSeatBookingInfo:
    new_booking = ShowSeatBookingInfo(booking_id=booking_id, seat_id=seat_id, status=True)
    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)

# delete/remove a multiple booking
def deleteAllBookings(session: Session, booking_id:int) -> ShowSeatBookingInfo:

    booking = session.query(ShowSeatBookingInfo).filter(ShowSeatBookingInfo.booking_id == booking_id).all()
    session.delete(booking)
    session.commit()  
    return Responses.failed_result("Faild to create booking")  

# delete a multiple data one-by-one by seat_id
def removeBookedSeats(session, seat_id:int) -> ShowSeatBookingInfo:
    booking = session.query(ShowSeatBookingInfo).filter(ShowSeatBookingInfo.seat_id == seat_id).first()
    session.delete(booking)
    session.commit()
