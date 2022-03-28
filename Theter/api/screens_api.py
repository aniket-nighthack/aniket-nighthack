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
from User.crud import *
from Common import oauth, token
from Theter.cruds.screens import *

router = APIRouter(prefix='/theter',
                   tags=["Screens"])


# auth = UserAuthentication()

# this api work for admin user to check a all screens information
@router.get("/screen/get-all-screen/")
def allScreens(session: Session = Depends(get_db), current_user: User = Depends(oauth.check_if_admin)):
    return getAllScreen(session)


@router.post("/screen/create-screen/")
def createScreen(screen: CreateScreen, session: Session = Depends(get_db),
                 current_user: User = Depends(oauth.check_if_merchant)):
    return addScreen(session, screen)


@router.put("/screen/update-screen/{screenid}")
def updateScreens(screenid: int, screen: CreateScreen, session: Session = Depends(get_db),
                  current_user: User = Depends(oauth.check_if_merchant)):
    return updateScreen(session, screenid, screen)


@router.delete("/screen/delete-screen/{screenid}")
def deleteScreen(screenid: int, session: Session = Depends(get_db),
                 current_user: User = Depends(oauth.check_if_merchant)):
    return deleteScreen(session, screenid)


# check which show is on a which screen by screenid
@router.get("/screen/show/{screenid}")
def screenShow(screenid: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.check_if_merchant)):
    return screenShowInfo(session, screenid)


# get all screen's info by theter id
@router.get("/screen/theter-screen/{tid}")
def theterShow(tid: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.check_if_merchant)):
    return getScreensByTid(session, tid)
