from sqlalchemy.orm import Session, joinedload
import secrets
from app.Common.APIResponses import Responses
from typing import List
from app.Theter.TModels import *
from app.Theter.TSchemas import *
from app.Common.Helper import *
from app.Theter.TExceptions import *
from fastapi import HTTPException,BackgroundTasks
from sqlalchemy.sql.expression import func, case
from sqlalchemy.sql.expression import false, true
from app.Theter.cruds.Theters import *
from app.Theter.cruds.seats import *
from datetime import date
from datetime import timedelta


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
                                            joinedload(ShowsInfo.movie)).filter(ShowsInfo.show_type == True).all()
    if show:
        return Responses.success_result_with_data("Show information available", "shows", show)
    else:
        return Responses.failed_result("Show information unavailable")


# get a specific theter show
def getTheterShows(session: Session, tid: int) -> TheterScreenInfo:
    theter_show = session.query(TheterScreenInfo, ShowsInfo).join(ShowsInfo).options(
        joinedload(ShowsInfo.movie),
        joinedload(TheterScreenInfo.seats)).filter(TheterScreenInfo.tid == tid).all()

    if theter_show:
        return Responses.success_result_with_data("Shows Available", "ShowsData", theter_show)
    else:
        return Responses.failed_result("Sorry current movie is not available")


# get a show's by logged theter user
def currentTShows(session: Session, uid: int) -> ShowsInfo:
    theter = session.query(ThetersInfo).filter(ThetersInfo.user_id == uid).first()

    shows = session.query(ShowsInfo).options(joinedload(ShowsInfo.screens), joinedload(ShowsInfo.movie)).filter(
        ShowsInfo.tid == theter.id).all()
    return shows


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


# update show Information
def updateShowInfo(session: Session, show: CreateShows, show_id: int) -> ShowsInfo:
    shows = session.query(ShowsInfo).filter(ShowsInfo.id == show_id).first()
    if shows:
        shows.tid = show.tid
        shows.screenid = show.screenid
        shows.start_time = show.start_time
        shows.end_time = show.end_time
        shows.mid = show.mid
        shows.show_type = show.show_type
        shows.show_ticket = show.show_ticket
        shows.show_date = show.show_date

        session.add(shows)
        session.commit()
        session.refresh(shows)
        return Responses.success_result("Show information update successfully")
    else:
        return Responses.failed_result("Failed to update show information")


# delete the show
def deleteShow(session: Session, show_id: int) -> ShowsInfo:
    show = session.query(ShowsInfo).filter(ShowsInfo.id == show_id).first()
    if show:
        session.delete(show)
        session.commit()
        return Responses.success_result("Show deleted Successfully")
    else:
        return Responses.failed_result("Failed to delete show please try again")


# update show status after a 24 hour
def updateShowStatusInfo(session: Session) -> ShowsInfo:
    print("functime update show status called")
    today = date.today()
    yesterday = today - timedelta(days=1)
    print(today, yesterday)
    print("data from query")
    data = session.query(ShowsInfo).all()
    # data = session.query(ShowsInfo).filter(ShowsInfo.show_date == yesterday, ShowsInfo.show_type == True).all()

    if data:
        for i in data:
            i.show_type = False
            session.add(i)
            session.commit()
        return Responses.success_result("Show status updated Successfully")
    else:
        return Responses.failed_result("Failed to update show status")
