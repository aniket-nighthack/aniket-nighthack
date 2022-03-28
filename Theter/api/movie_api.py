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
from Theter.cruds.movie import *

router = APIRouter(prefix='/theter',
                   tags=["Movie"])


@router.get("/movies/")
def movies(session: Session = Depends(get_db), current_user: User = Depends(oauth.check_if_admin)):
    return getAllMoview(session)


@router.get("/current-movies/")
def currentMovies(session: Session = Depends(get_db), current_User: User = Depends(oauth.check_if_admin)):
    return getCurrentMovies(session)


@router.get("/old-movies/")
def oldMovies(session: Session = Depends(get_db), current_User: User = Depends(oauth.check_if_admin)):
    return getOldMovies(session)


@router.get("/location_movies/")
def get_movie_by_location(location: str, session: Session = Depends(get_db)):
    return moviesByLocation(location, session)


@router.post("/movies/create-movies/")
def createMovie(movie: CreateMovies, session: Session = Depends(get_db),
                current_user: User = Depends(oauth.check_if_admin)):
    return addMovies(session, movie, current_user.id)


# update movie details
@router.put("/movies/update-movie/{id}")
def updateMovie(id: int, movie: CreateMovies, session: Session = Depends(get_db),
                current_user: User = Depends(oauth.check_if_admin)):
    return updateMovieInfo(session, movie, id)


# delete movie details
@router.delete("/movies/delete-movie/{id}")
def deleteMovie(id: int, session: Session = Depends(get_db), current_user: User = Depends(oauth.check_if_admin)):
    return deleteMovieInfo(session, id)


@router.put('/change_status/{id}', status_code=202)
def changeStatus(id: int, status: bool, db: Session = Depends(get_db),
                 current_user: User = Depends(oauth.check_if_admin)):
    return change_status(id, status, db)


@router.get("/search_movie/")
def search_movie_by_title(title: str, session: Session = Depends(get_db)):
    return searchMovieTitle(title, session)


@router.post("/allocate_movie/")
def allocate_movie_to_theter(allocate: CreateMovieAllocated, session: Session = Depends(get_db),
                             current_user: User = Depends(oauth.check_if_admin)):
    return allocateMovies(session, allocate)


@router.get("/theater_movie/")
def get_theater_movies(tid: int, session: Session = Depends(get_db),
                       current_user: User = Depends(oauth.check_if_admin)):
    return theaterMovies(session, tid)


# get show details after selecting the movie
@router.get("/movie/show")
def get_shoes_by_movie(mid: int, session: Session = Depends(get_db),
                       current_user: User = Depends(oauth.get_current_user)):
    return movieShows(session, mid, current_user.id)
