from fastapi import FastAPI 
from pydantic import BaseModel
from User.api import *
from Theter import TAPI

app = FastAPI()

# users api
app.include_router(router)

# theters endpoints
app.include_router(TAPI.router)

@app.get("/")
def index():
    return {'called sucessfully'}