from fastapi import FastAPI, Header, Request 
from pydantic import BaseModel
from User.api import *
from Theter import TAPI
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from User import authenticatedUsers
from User.Location import location_api
from Theter.api import theters_api, screens_api, seats_api, movie_api, show_api
app = FastAPI()

# authentication router
app.include_router(authenticatedUsers.router)

# users api
app.include_router(router)

# user location router
app.include_router(location_api.router)

# theters for the end- users routes
app.include_router(theters_api.router)



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

