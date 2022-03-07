from Theter.TCrud import *
from Theter.TModels import *
from Theter.TSchemas import *
from fastapi import APIRouter, Depends, HTTPException,  File, UploadFile
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from Connection.database import *
from Common.APIResponses import Responses
from fastapi_utils import *
import shutil

router = APIRouter()

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 


# --------------- thete information ---------------------

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

@router.delete("/deleteTheter")
def delete(auth_token: str, session:Session = Depends(get_db)):
    return deleter_therer(session, auth_token)


# --------------- theter documents --------------------------------

@router.get("/theterdocs")
def getTheterDocs(session:Session = Depends(get_db)):
    return get_all_docs(session)

@router.post("/addDocs")
def image(tid:int,title:str,image: UploadFile = File(...),  session:Session = Depends(get_db)):
    with open("media/"+ image.filename, "wb") as image_obj:
        shutil.copyfileobj(image.file, image_obj)
    url = str("media/"+ image.filename)
    return addDocument(session, 1, url, title)   

# --------------- theter verification --------------------
@router.put("/verification")
def verify(verification: CreateVerification, session:Session = Depends(get_db)):
    return addVerification(session, verification)    



# -------------- theter screen --------------------

@router.get("/screen")
def allScreens(session:Session = Depends(get_db)):
    return getAllScreen(session)

@router.post("/screen")
def createScreen(screen: CreateScreen, session:Session = Depends(get_db)):
    return addScreen(session, screen)

@router.put("/screen")
def updateScreens(screenid:int,screen: CreateScreen, session:Session = Depends(get_db)):
    return updateScreen(session, screenid, screen)

@router.delete("/screen")
def delScreen(screenid:int, session:Session = Depends(get_db)):
    return deleteScreen(session, screenid)


# --------------- screen seats --------------------

@router.post("/seat")
def createSeat(seat: CreateSeat, session:Session = Depends(get_db)):
    return addSeats(session, seat)


# ---------------------- Movies  -------------------------

@router.get("/movies")
def movies(session:Session = Depends(get_db)):
    return getAllMoview(session)

@router.post("/movies")
def createMovie(movie:CreateMovies, session:Session = Depends(get_db)):
    return addMovies(session, movie)


# ---------------------- Show ------------------------

@router.get("/show")
def allShows(session:Session = Depends(get_db)):
    return getAllShows(session)

@router.get("/thetershow")
def theter_show(tid:int,session:Session = Depends(get_db)):    
    return getTheterShows(session, tid)

@router.post("/show")
def createshow(show:CreateShows, session:Session = Depends(get_db)):
    return addShow(session, show)


# ------------------------- Booking ------------------------

@router.post("/booking")
def createBooking(booking:CreateBooking, session:Session = Depends(get_db)):
    return addBooking(session, booking)

@router.get("/booking")
def bookings(session:Session = Depends(get_db)):
    return getAllBookings(session)

@router.get("/userbooking")
def userBooking(uid:int,session:Session = Depends(get_db)):
    return getUsersBooking(session, uid)

