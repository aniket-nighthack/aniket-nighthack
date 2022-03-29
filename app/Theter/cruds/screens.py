from sqlalchemy.orm import Session, joinedload
import secrets
from app.Common.APIResponses import Responses
from typing import List
from app.Theter.TModels import *
from app.Theter.TSchemas import *
from app.Common.Helper import *
from app.Theter.TExceptions import *
from fastapi import HTTPException
from sqlalchemy.sql.expression import func, case
from sqlalchemy.sql.expression import false, true
from app.Theter.cruds.show import *


# ---------------- Screen Operation --------------------------------

def addScreen(session: Session, screen: CreateScreen) -> TheterScreenInfo:
    add_screen = TheterScreenInfo(screen_type=screen.screen_type, tid=screen.tid)
    session.add(add_screen)
    session.commit()
    return Responses.success_result("New Screen added successfully")


def getTheterScreen(tid: int, screenid: int, session: Session) -> TheterScreenInfo:
    screen = session.query(TheterScreenInfo).filter(TheterScreenInfo.tid == tid,
                                                    TheterScreenInfo.id == screenid).first()
    return screen


def getAllScreen(session: Session) -> TheterScreenInfo:
    screens = session.query(TheterScreenInfo).options(joinedload(TheterScreenInfo.seats)).all()
    return screens


def updateScreen(session: Session, screenid: int, screen: CreateScreen) -> TheterScreenInfo:
    screen_update = getTheterScreen(screen.tid, screenid, session)
    if screen_update:
        screen_update.screen_type = screen.screen_type
        session.commit()
        return Responses.success_result("Screen Details updated successfully")
    else:
        return Responses.failed_result("Failed to update screen details")


def deleteScreen(session: Session, screenid: int) -> TheterScreenInfo:
    screen_del = session.query(TheterScreenInfo).get(screenid)
    if screen_del:
        session.delete(screen_del)
        session.commit()
        return Responses.success_result("Screen Deleted Sucessfully")
    else:
        return Responses.failed_result("Failed to delete screen")

    # get screen details by its id


def screenByID(session: Session, screenid: int) -> TheterScreenInfo:
    screen = session.query(TheterScreenInfo).filter(TheterScreenInfo.id == screenid).first()
    return screen


# check a which show is running on a which screen
def screenShowInfo(session: Session, screenid: int):
    screen = screenByID(session, screenid)
    if screen:
        shows = showByScreenId(session, screenid)
        if shows:
            return Responses.success_result_with_data("Screen shows found", "screenShow", shows)
        else:
            return Responses.failed_result("Currently Show is not available")
    else:
        return Responses.failed_result("Invalid screen details")


# get all screens by theter id
def getScreensByTid(session: Session, tid: int) -> TheterScreenInfo:
    screen = session.query(TheterScreenInfo).options(joinedload(TheterScreenInfo.seats)).filter(
        TheterScreenInfo.tid == tid).all()
    if screen:
        return Responses.success_result_with_data("Theter screens find", "screens", screen)
    else:
        return Responses.failed_result("Screen's not allocated for this screen")
