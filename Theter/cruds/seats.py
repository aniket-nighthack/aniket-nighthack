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


# ---------------- Add New Seats ----------------
def addSeats(session: Session, seat: CreateSeat) -> SeatsInfo:
    seat_add = SeatsInfo(screenid=seat.screenid, tid=seat.tid, seat_name=seat.seat_name,
                         seat_price=seat.seat_price, seat_status=seat.seat_status)
    session.add(seat_add)
    session.commit()
    return Responses.success_result("Seat added successfully")


# get seats by seat id  
def getSeatById(session: Session, seatid: int) -> SeatsInfo:
    seat = session.query(SeatsInfo).filter(SeatsInfo.id == seatid).first()
    return seat


# get seats by screenid
# def seatsByScreenid(session:Session,screenid:int) -> SeatsInfo:
#     seats = session.query(SeatsInfo).filter(SeatsInfo.screenid == screenid).all()
#     if seats:
#         return Responses.success_result_with_data("Seats find", "seats", seats)
#     else:    
#         return Responses.failed_result("Screen is invalid")


def seatsByScreenid(session: Session, screenid: int) -> SeatsInfo:
    available_seats_case = case(
        (SeatsInfo.seat_status == 1, "Available Seats")
    )

    book_seat_case = case([(SeatsInfo.seat_status == False, "Booked Seats")])

    # check first if screen is exits or not
    if session.query(SeatsInfo).filter(SeatsInfo.screenid == screenid).first():
        seats = session.query(SeatsInfo).filter(SeatsInfo.screenid == screenid).all()

        if seats:
            return Responses.success_result_with_data("Seats find", "seats", seats)
        else:
            return Responses.failed_result("Screen is invalid")
    else:
        return Responses.failed_result("seats not allocated for this screen now")

    # ---------------- update seat information ----------


def updateSeatInfo(session: Session, seat: CreateSeat, id: int) -> SeatsInfo:
    seat_info = getSeatById(session, id)
    if seat_info:
        seat_info.screenid = seat.screenid
        seat_info.tid = seat.tid
        seat_info.seat_name = seat.seat_name
        seat_info.seat_price = seat.seat_price
        seat_info.seat_status = seat.seat_status

        session.add(seat_info)
        session.commit()
        session.refresh(seat_info)
        return Responses.success_result_with_data("Seat Information Updated Successfully", "seatInfo", seat_info)
    else:
        return Responses.failed_result("Seat Information Updated Failed")

    # ---------------- delete seat ------------------------


def deleteSeatInfo(session: Session, id: int) -> SeatsInfo:
    seat = getSeatById(session, id)
    if seat:
        session.delete(seat)
        session.commit()
        return Responses.success_result("Seat Information Deleted Successfully")
    else:
        return Responses.failed_result("Failed to delete seat information")

    # ---------------- check seat is avialabel or not ---


def seatAvailableOrNot(session: Session, seatid: int) -> SeatsInfo:
    seat = getSeatById(session, seatid)
    if seat:
        if seat.seat_status:
            print("all seats available")
            return True
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"This {seatid} seat id is already booked by another user.please try to book another seat")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid seat")
