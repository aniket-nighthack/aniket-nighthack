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

# get movie by id
def getMovieById(session:Session, id: int) -> MovieInfo:
    movies = session.query(MovieInfo).filter(MovieInfo.id == id).first()
    return movies 

# add new movies to the database
def addMovies(session:Session,movie:CreateMovies) -> MovieInfo:
    add_movie = MovieInfo(**movie.dict())
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