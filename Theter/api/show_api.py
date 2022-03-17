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
from Theter.cruds.show import *

router = APIRouter(prefix='/theter',
    tags=["Shows"])


@router.get("/show/all-shows/")
def allShows(session:Session = Depends(get_db)):
    return getAllShows(session)

@router.get("/theter-show/{tid}")
def theter_show(tid:int,session:Session = Depends(get_db)):    
    return getTheterShows(session, tid)

@router.post("/show/create-show/")
def createshow(show:CreateShows, session:Session = Depends(get_db)):
    return addShow(session, show)


