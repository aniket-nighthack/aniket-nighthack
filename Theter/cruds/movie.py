from sqlalchemy.orm import Session , joinedload
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

# get all movies
def getAllMoview(session:Session) -> MovieInfo:
    movies = session.query(MovieInfo).all()
    return movies

# get all current movies
def getCurrentMovies(session:Session) -> MovieInfo:
    movies = session.query(MovieInfo).filter(MovieInfo.status == True).all()
    if movies:
        return Responses.success_result_with_data("Current Movies find", "movies", movies)
    else:
        return Responses.failed_result("There is no current movies")

# get all old's movies
def getOldMovies(session:Session) -> MovieInfo:
    movies = session.query(MovieInfo).filter(MovieInfo.status == False).all()
    if movies:
        return Responses.success_result_with_data("Old Movies find", "movies", movies)
    else:
        return Responses.failed_result("There is no old movies")

# get movie by id
def getMovieById(session:Session, id: int) -> MovieInfo:
    movies = session.query(MovieInfo).filter(MovieInfo.id == id).first()
    return movies 

# add new movies to the database
def addMovies(session:Session,movie:CreateMovies, userid:int) -> MovieInfo:
    # add_movie = MovieInfo(**movie.dict())
    theter = session.query(ThetersInfo).filter(ThetersInfo.user_id == userid).first()

    add_movie = MovieInfo(mov_name=movie.mov_name, language=movie.language,
                          mov_type = movie.mov_type, tid=theter.id,
                          description=movie.description, duration=movie.duration, status=True)
    session.add(add_movie)
    session.commit()
    session.refresh(add_movie)
    return add_movie

# update movie details
def updateMovieInfo(session:Session, movie:CreateMovies, id:int) -> MovieInfo:
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
def deleteMovieInfo(session:Session, id:int) -> MovieInfo:
    movie_info = getMovieById(session, id)
    if movie_info:
        session.delete(movie_info)
        session.commit()
        return Responses.success_result("Movie Information Deleted Successfully")
    else:
        return Responses.failed_result("Failed to delete movie information")    