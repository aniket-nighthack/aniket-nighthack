from fastapi import FastAPI, Header, Request
from pydantic import BaseModel
from app.User.api import *
from app.Theter import TAPI
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.User import authenticatedUsers
from app.User.Location import location_api
from app.Theter.api import theters_api, screens_api, seats_api, movie_api, show_api, booking_api

app = FastAPI()


@app.get("/")
def index():
    return {
        'main': "main run default"
    }


# authentication router
app.include_router(authenticatedUsers.router)

# users api
app.include_router(router)

# user location router
app.include_router(location_api.router)

# theters for the end- users routes
app.include_router(theters_api.router)

# booking module for the end-user routes
app.include_router(booking_api.router)

# theters endpoints
app.include_router(TAPI.router)

# screens router
app.include_router(screens_api.router)

# seats router
app.include_router(seats_api.router)

# movie router
app.include_router(movie_api.router)

# shows router
app.include_router(show_api.router)
