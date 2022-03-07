from sqlalchemy.orm import Session , joinedload
import secrets 
from Common.APIResponses import Responses
from typing import List
from Theter.TModels import *
from Theter.TSchemas import *
from Common.Helper import *
from Theter.TExceptions import *
from fastapi import HTTPException
from sqlalchemy.sql.expression import func



# get a speicif theter
def get_specific_therter(session:Session, t_name:String) -> ThetersInfo:
    theter = session.query(ThetersInfo).filter(ThetersInfo.t_name == t_name).first()
    return theter  

#  get all theter list
def get_all_theter(session:Session) -> List[ThetersInfo]:
    theter = session.query(ThetersInfo).options(joinedload(ThetersInfo.docs), joinedload(ThetersInfo.verification),
                           joinedload(ThetersInfo.screens)).all()

    return Responses.success_result_with_data("Theters fond", "TheterData", theter)

# create new theter
def create_theter(session:Session, theter:CreateUpdateTheter):
    token = getAuthToken()
    new = ThetersInfo(t_name=theter.t_name, t_address=theter.t_address, t_contact=theter.t_contact,
                          auth_token=token, opening_time=theter.opening_time, closing_time=theter.closing_time)
    session.add(new)
    session.commit()
    return Responses.success_result("New theter added successfully")

# update the theter information
def  update_theter(session:Session, auth_token:str, theter_info:CreateUpdateTheter)-> ThetersInfo:

    theter = session.query(ThetersInfo).filter(ThetersInfo.auth_token == auth_token).first()
    if theter:
        theter.t_name = theter_info.t_name
        theter.t_address = theter_info.t_address
        theter.t_contact = theter_info.t_contact
        theter.opening_time = theter_info.opening_time
        theter.closing_time = theter_info.closing_time

        session.commit()
        session.refresh(theter)
        return theter
    else:
        return "not found"       

# delete the theter information
def deleter_therer(session:Session, auth_token:String) -> ThetersInfo:
    theter = session.query(ThetersInfo).filter(ThetersInfo.auth_token == auth_token).first()

    if theter:
        session.delete(theter)
        return Responses.success_result("Theter Deleted Successfully")
    else:
        return Responses.failed_result("Failed to delete theter")    


# ----------------- theter documents -------------------------------- 

# get all the theter documents
def get_all_docs(session:Session) -> TheterDocsInfo:
    return session.query(TheterDocsInfo).all() 


# add theter documents
def addDocument(session:Session, tid:int, url:str, title:str):

    if title == 'shopact':
        docs = TheterDocsInfo(shop_act_licence=url, tid=tid)
    if title == 'gst':
        docs = TheterDocsInfo(gst_licence=url, tid=tid)  
    session.add(docs)
    session.commit()
    session.refresh(docs)
    return docs

#  ----------------  theter verification ----------------

# get specific theter documents
def get_specific_verification(session:Session,tid:int) -> TheterVerificationInfo:
    verification = session.query(TheterVerificationInfo).filter(TheterVerificationInfo.tid == tid).first()
    return verification

# verify theter
def addVerification(session:Session, verification:CreateVerification):
    isverify = get_specific_verification(session, verification.tid)
    if isverify:
        isverify.shopact_verify = verification.shopact_verify
        isverify.gst_verify = verification.gst_verify
        isverify.is_live = verification.is_live
        isverify.is_verifyed = verification.is_verifyed
        isverify.tid = verification.tid

        session.commit()
        return Responses.success_result("Verification Updated Sucessfully")                          
                                         
    else:
        add_ver = TheterVerificationInfo(shopact_verify=verification.shopact_verify, gst_verify=verification.gst_verify, 
                                         
                                         is_live=verification.is_live, is_verifyed=verification.is_verifyed,
                                         tid=verification.tid)
        session.add(add_ver)
        session.commit()
        return Responses.success_result("verification Added Sucessfully")        


# ---------------- Screen Operation --------------------------------

def addScreen(session:Session, screen:CreateScreen) -> TheterScreenInfo:                                           
    add_screen = TheterScreenInfo(screen_type= screen.screen_type, tid= screen.tid)
    session.add(add_screen)
    session.commit()
    return Responses.success_result("New Screen added successfully")

def getTheterScreen(tid:int, screenid:int,session:Session) -> TheterScreenInfo:
    screen = session.query(TheterScreenInfo).filter(TheterScreenInfo.tid == tid, TheterScreenInfo.id==screenid).first()
    return screen

def getAllScreen(session:Session) -> TheterScreenInfo:
    screens = session.query(TheterScreenInfo).options(joinedload(TheterScreenInfo.seats)).all()
    return screens

def updateScreen(session:Session, screenid:int, screen:CreateScreen) -> TheterScreenInfo:
    screen_update =  getTheterScreen(screen.tid, screenid, session)
    if screen_update:
        screen_update.screen_type = screen.screen_type
        session.commit()
        return Responses.success_result("Screen Details updated successfully")
    else:
        return Responses.failed_result("Failed to update screen details")        

def deleteScreen(session:Session, screenid:int)-> TheterScreenInfo: 
    screen_del = session.query(TheterScreenInfo).get(screenid)
    if screen_del:
        session.delete(screen_del)
        session.commit()
        return Responses.success_result("Screen Deleted Sucessfully")
    else:
        return Responses.failed_result("Failed to delete screen")    


# ---------------- Screen Seats ---------------- 

def addSeats(session:Session, seat:CreateSeat) -> SeatsInfo:
    seat_add = SeatsInfo(screenid=seat.screenid, tid=seat.tid, seat_name=seat.seat_name,
                         seat_price=seat.seat_price, seat_status=seat.seat_status)
    session.add(seat_add)
    session.commit()
    return Responses.success_result("Seat added successfully")                     


# ------------------- movies ----------------

def getAllMoview(session:Session) -> MovieInfo:
    movies = session.query(MovieInfo).all()
    return movies

def addMovies(session:Session,movie:CreateMovies) -> MovieInfo:
    add_movie = MovieInfo(**movie.dict())
    session.add(add_movie)
    session.commit()
    session.refresh(add_movie)
    return add_movie

# -------------- shows crud -------------------------------
def addShow(session:Session, shows:CreateShows) -> ShowsInfo:
    add_show = ShowsInfo(**shows.dict())
    session.add(add_show)
    session.commit()
    session.refresh(add_show)
    return add_show

def getAllShows(session:Session)-> ShowsInfo:
    show = session.query(ShowsInfo).options(joinedload(ShowsInfo.screens), joinedload(ShowsInfo.movie)).all()
    return show

def getTheterShows(session:Session, tid:int) -> TheterScreenInfo:
    # theter_show = session.query(TheterScreenInfo).options(joinedload(TheterScreenInfo.show),
    #                              joinedload(TheterScreenInfo.seats)).filter(TheterScreenInfo.tid == tid).all()
    
    theter_show = session.query(TheterScreenInfo,ShowsInfo).join(ShowsInfo).options(
                                 joinedload(ShowsInfo.movie),
                                 joinedload(TheterScreenInfo.seats)).filter(TheterScreenInfo.tid == tid).all()
    
    # theter_show = session.query(TheterScreenInfo, SeatsInfo, ShowsInfo, MovieInfo).\
    #               select_from(TheterScreenInfo).join(SeatsInfo, SeatsInfo.screenid == TheterScreenInfo.id).join(ShowsInfo).join(MovieInfo,  ShowsInfo.mid == MovieInfo.id).filter(TheterScreenInfo.tid == tid).all()

    # theter_show = session.query(ShowsInfo, MovieInfo).\
    #               select_from(ShowsInfo).join(MovieInfo, MovieInfo.id == ShowsInfo.mid).\
    #                         filter(ShowsInfo.tid == tid).all()

    return Responses.success_result_with_data("Shows Available", "ShowsData", theter_show)                             
