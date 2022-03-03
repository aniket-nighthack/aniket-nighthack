from sqlalchemy.orm import Session 
import secrets 
from Common.APIResponses import Responses
from typing import List
from Theter.TModels import *
from Theter.TSchemas import *
from Common.Helper import *
from Theter.TExceptions import *
from fastapi import HTTPException


# get a speicif theter
def get_specific_therter(session:Session, t_name:String) -> ThetersInfo:
    theter = session.query(ThetersInfo).filter(ThetersInfo.t_name == t_name).first()
    return theter  

#  get all theter list
def get_all_theter(session:Session) -> ThetersInfo:
    theter = session.query(ThetersInfo).all()
    return Responses.success_result_with_data("Theters fond", "TheterData", theter)

# create new theter
def create_theter(session:Session, theter:CreateUpdateTheter):
    token = getAuthToken()
    new = ThetersInfo(t_name=theter.t_name, t_address=theter.t_address, t_contact=theter.t_contact,
                          auth_token=token, opening_time=theter.opening_time, closing_time=theter.closing_time)
    session.add(new)
    session.commit()
    return Responses.success_result("New theter added successfully")

# 
def  update_theter(session:Session, auth_token:str, theter_info:CreateUpdateTheter)-> ThetersInfo:
    theter = session.query(ThetersInfo).filter(ThetersInfo.auth_token == auth_token).first()
    if theter:
        return theter
    else:
        return "not found"       