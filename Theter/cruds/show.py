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


# add/create new show
def addShow(session: Session, shows: CreateShows) -> ShowsInfo:
    add_show = ShowsInfo(**shows.dict())
    session.add(add_show)
    session.commit()
    session.refresh(add_show)
    return add_show


# get all show information
def getAllShows(session: Session) -> ShowsInfo:
    available_seats_case = case(
        [
            (SeatsInfo.seat_status == True, "Available Seats")
        ]
    )

    book_seat_case = case([(SeatsInfo.seat_status == False, "Booked Seats")])

    show = session.query(ShowsInfo).options(joinedload(ShowsInfo.screens),
                                            joinedload(ShowsInfo.movie)).all()
    return show


# get a specific theter show
def getTheterShows(session: Session, tid: int) -> TheterScreenInfo:
    theter_show = session.query(TheterScreenInfo, ShowsInfo).join(ShowsInfo).options(
        joinedload(ShowsInfo.movie),
        joinedload(TheterScreenInfo.seats)).filter(TheterScreenInfo.tid == tid).all()

    if theter_show:
        return Responses.success_result_with_data("Shows Available", "ShowsData", theter_show)
    else:
        return Responses.failed_result("Sorry current movie is not available")

    # get a show by screen id


def showByScreenId(session: Session, screenid: int) -> ShowsInfo:
    available_seats_case = case(
        [
            (SeatsInfo.seat_status == True, "Available Seats")
        ]
    )

    book_seat_case = case([(SeatsInfo.seat_status == False, "Booked Seats")])

    show = session.query(ShowsInfo, func.count(available_seats_case).label('available seats'),
                         func.count(book_seat_case).label('booked seats')).select_from(SeatsInfo).filter(
        SeatsInfo.screenid == ShowsInfo.screenid) \
        .options(joinedload(ShowsInfo.screens),
                 joinedload(ShowsInfo.movie)).filter(ShowsInfo.screenid == screenid).all()
    return show


# get all show by  tid
def getShowByTid(session: Session, tid: int) -> ShowsInfo:
    available_seats_case = case(
        [
            (SeatsInfo.seat_status == True, "Available Seats")
        ]
    )

    book_seat_case = case([(SeatsInfo.seat_status == False, "Booked Seats")])

    show = session.query(ShowsInfo) \
        .join(TheterScreenInfo) \
        .options(joinedload(ShowsInfo.movie), joinedload(ShowsInfo.screens)) \
        .filter(ShowsInfo.tid == tid).all()
    if show:
        return Responses.success_result_with_data("Shows available", "showData", show)
    else:
        # check theter id is exits or not exits
        theter = getThereById(session, tid)
        if theter:
            return Responses.failed_result("Theter don't have any shows available now")
        else:
            return Responses.failed_result("Theter is invalid")

        # get shows by show id


def getShowByID(session: Session, show_id: int) -> ShowsInfo:
    show = session.query(ShowsInfo).filter(ShowsInfo.id == show_id).first()
    return show


# display all  seats information by shows
def showSeats(session: Session, show_id: int) -> ShowsInfo:
    show = getShowByID(session, show_id)
    if show:
        seats = seatsByScreenid(session, show.screenid)
        return seats
    return show
