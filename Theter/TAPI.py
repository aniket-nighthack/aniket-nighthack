from Theter.TCrud import *
from Theter.TModels import *
from Theter.TSchemas import *
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from Connection.database import *
from Common.APIResponses import Responses


router = APIRouter()

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 


# get all theters data
@router.get("/theters")
def get_all(session:Session = Depends(get_db)):
    return get_all_theter(session)

# create or add new theter 
@router.post("/addTheter")
def create_the(theter:CreateUpdateTheter, session:Session = Depends(get_db)):
    check = get_specific_therter(session, theter.t_name)
    if check is None:
        new = create_theter(session, theter)
        return new 
    else:
        return Responses.failed_result("Theter is already register please try again")


@router.put("/updateTheter")
def update(theter: CreateUpdateTheter,auth_token: str, session:Session = Depends(get_db)):
    return update_theter(session, auth_token, theter)