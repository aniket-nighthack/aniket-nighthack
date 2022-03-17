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
from Theter.cruds.movie import *

router = APIRouter(prefix='/theter',
    tags=["Movie"])


@router.get("/movies/")
def movies(session:Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return getAllMoview(session)

@router.post("/movies/create-movies/")
def createMovie(movie:CreateMovies, session:Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return addMovies(session, movie)

# update movie details
@router.put("/movies/update-movie/{id}")
def updateMovie(id: int, movie:CreateMovies,session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return updateMovieInfo(session, movie, id) 

# delete movie details
@router.delete("/movies/delete-movie/{id}")
def deleteMovie(id:int, session: Session = Depends(get_db), current_user: User = Depends(oauth.get_current_user)):
    return deleteMovieInfo(session, id)

