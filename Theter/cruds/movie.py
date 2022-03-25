from sqlalchemy.orm import Session, joinedload
import secrets
from Common.APIResponses import Responses
from typing import List
from Theter.TModels import *
from Theter.TSchemas import *
from Common.Helper import *
from Theter.TExceptions import *
from fastapi import HTTPException, status
from sqlalchemy.sql.expression import func, case
from sqlalchemy.sql.expression import false, true
from User.crud import getUserById
from User.Location.location_crud import getLastLocation


# get all movies
def getAllMoview(session: Session) -> MovieInfo:
    movies = session.query(MovieInfo).all()
    return movies


# get all current movies
def getCurrentMovies(session: Session) -> MovieInfo:
    movies = session.query(MovieInfo).filter(MovieInfo.status == True).all()
    if movies:
        return Responses.success_result_with_data("Current Movies find", "movies", movies)
    else:
        return Responses.failed_result("There is no current movies")


# get all old's movies
def getOldMovies(session: Session) -> MovieInfo:
    movies = session.query(MovieInfo).filter(MovieInfo.status == False).all()
    if movies:
        return Responses.success_result_with_data("Old Movies find", "movies", movies)
    else:
        return Responses.failed_result("There is no old movies")


# get movie by id
def getMovieById(session: Session, id: int) -> MovieInfo:
    movies = session.query(MovieInfo).filter(MovieInfo.id == id).first()
    if movies:
        return movies
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Movie not found")


# add new movies to the database
def addMovies(session: Session, movie: CreateMovies, userid: int) -> MovieInfo:
    # add_movie = MovieInfo(**movie.dict())
    theter = session.query(ThetersInfo).filter(ThetersInfo.user_id == userid).first()

    add_movie = MovieInfo(mov_name=movie.mov_name, language=movie.language,
                          mov_type=movie.mov_type, tid=theter.id,
                          description=movie.description, duration=movie.duration, status=True)
    session.add(add_movie)
    session.commit()
    session.refresh(add_movie)
    return add_movie


# update movie details
def updateMovieInfo(session: Session, movie: CreateMovies, id: int) -> MovieInfo:
    movie_info = getMovieById(session, id)
    if movie_info:
        movie_info.mov_name = movie.mov_name
        movie_info.language = movie.language
        movie_info.mov_type = movie.mov_type

        session.add(movie_info)
        session.commit()
        session.refresh(movie_info)

        return Responses.success_result_with_data("Movie Information Updated Successfully", "movieData", movie_info)
    else:
        return Responses.failed_result("Failed to update movie details")

    # delete the movie details


def deleteMovieInfo(session: Session, id: int) -> MovieInfo:
    movie_info = getMovieById(session, id)
    if movie_info:
        session.delete(movie_info)
        session.commit()
        return Responses.success_result("Movie Information Deleted Successfully")
    else:
        return Responses.failed_result("Failed to delete movie information")


def change_status(id: int, status: bool, db: Session) -> MovieInfo:
    movie = db.query(MovieInfo).filter(MovieInfo.id == id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Movie with the id {id} is not found")

    movie.status = status
    db.commit()

    return {"msg": "status updated"}


def moviesByLocation(city: str, session: Session) -> MovieInfo:
    movies = session.query(MovieInfo).join(ThetersInfo) \
        .filter(ThetersInfo.city.contains(city),
                MovieInfo.tid == ThetersInfo.id, MovieInfo.status == True).all()

    return Responses.success_result_with_data("location movie fond", "movies", movies)


def searchMovieTitle(title: str, session: Session):
    movies = session.query(MovieInfo).filter(MovieInfo.mov_name.contains(title)).all()
    return movies


def allocateMovies(session: Session, allocated: AllocateMovies) -> AllocateMoviesInfo:
    data = session.query(AllocateMoviesInfo).filter(AllocateMoviesInfo.mid == allocated.mid,
                                                    AllocateMoviesInfo.tid == allocated.tid).first()
    if data:
        return Responses.failed_result(
            f"This movie {allocated.mid} is already allocated to this theter {allocated.tid}")
    else:
        movie = AllocateMoviesInfo(**allocated.dict())
        session.add(movie)
        session.commit()
        session.refresh(movie)
        return Responses.success_result("Movies allocated successfully")


def theaterMovies(session: Session, tid: int) -> AllocateMoviesInfo:
    movie = session.query(AllocateMoviesInfo).options(joinedload(AllocateMoviesInfo.movie)).filter(
        AllocateMoviesInfo.tid == tid).all()
    return movie


def movieShows(session: Session, mid: int, uid: int) -> MovieInfo:
    user_location = getLastLocation(session, uid)
    # theter = session.query(ThetersInfo, AllocateMoviesInfo).options(joinedload(AllocateMoviesInfo.movie))\
    #                                  .join(AllocateMoviesInfo, AllocateMoviesInfo.tid == ThetersInfo.id)\
    #                                  .filter(ThetersInfo.city == user_location.city).all()
    theter = session.query(ThetersInfo, ShowsInfo)\
         .join(ShowsInfo, ShowsInfo.tid == ThetersInfo.id)\
        .filter(ThetersInfo.city == user_location.city).all()
    return theter
