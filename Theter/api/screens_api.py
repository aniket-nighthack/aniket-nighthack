from Theter.TCrud import *
from Theter.TModels import *
from Theter.TSchemas import *
from fastapi import APIRouter, Depends, HTTPException,  File, UploadFile
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


@router.get("/screen/get-all-screen/")
def allScreens(session:Session = Depends(get_db),current_user: User = Depends(oauth.get_current_user)):
    return getAllScreen(session)

@router.post("/screen/create-screen/")
def createScreen(screen: CreateScreen, session:Session = Depends(get_db),current_user: User = Depends(oauth.get_current_user)):
    return addScreen(session, screen)

@router.put("/screen/update-screen/{screenid}")
def updateScreens(screenid:int,screen: CreateScreen, session:Session = Depends(get_db),current_user: User = Depends(oauth.get_current_user)):
    return updateScreen(session, screenid, screen)

@router.delete("/screen/delete-screen/{screenid}")
def deleteScreen(screenid:int, session:Session = Depends(get_db),current_user: User = Depends(oauth.get_current_user)):
    return deleteScreen(session, screenid)

# chek which show is on a which screen by screenid
@router.get("/screen/show/{screenid}")
def screenShow(screenid:int, session:Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return screenShowInfo(session, screenid)
