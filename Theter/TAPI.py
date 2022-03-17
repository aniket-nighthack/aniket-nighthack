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
from User.crud import *

router = APIRouter(prefix='/theter',
    tags=["Theter-User"])

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close() 


# --------------- theter user login ---------------
@router.get("/sign-in")
def loignUser(mobile:str, session:Session = Depends(get_db)):
    return login_user(session, mobile)


# --------------- thete information ---------------------

# get all theters data
@router.get("/all-theters/")
def get_all(session:Session = Depends(get_db)):
    return get_all_theter(session)

# create or add new theter 
@router.post("/add-theter/")
def create_the(theter:CreateUpdateTheter, session:Session = Depends(get_db)):
    new = create_theter(session, theter)
    return new 
    check = get_specific_therter(session, theter.t_name)
    if check is None:
        new = create_theter(session, theter)
        return new 
    else:
        return Responses.failed_result("Theter is already register please try again")


@router.put("/update-theter/{auth_token}")
def update(theter: CreateUpdateTheter,auth_token: str, session:Session = Depends(get_db)):
    return update_theter(session, auth_token, theter)

@router.delete("/delete-theter/{auth_token}")
def delete(auth_token: str, session:Session = Depends(get_db)):
    return deleter_therer(session, auth_token)


# --------------- theter documents --------------------------------

# @router.get("/theter-docs/")
# def getTheterDocs(session:Session = Depends(get_db)):
#     return get_all_docs(session)

# @router.post("/add-docs/{tid}")
# def image(tid:int,title:str,image: UploadFile = File(...),  session:Session = Depends(get_db)):
#     with open("media/"+ image.filename, "wb") as image_obj:
#         shutil.copyfileobj(image.file, image_obj)
#     url = str("media/"+ image.filename)
#     return addDocument(session, 1, url, title)   

# # --------------- theter verification --------------------
# @router.put("/verification/")
# def verify(verification: CreateVerification, session:Session = Depends(get_db)):
#     return addVerification(session, verification)    



# -------------- theter screen --------------------

# @router.get("/screen/get-all-screen/")
# def allScreens(session:Session = Depends(get_db)):
#     return getAllScreen(session)

# @router.post("/screen/create-screen/")
# def createScreen(screen: CreateScreen, session:Session = Depends(get_db)):
#     return addScreen(session, screen)

# @router.put("/screen/update-screen/{screenid}")
# def updateScreens(screenid:int,screen: CreateScreen, session:Session = Depends(get_db)):
#     return updateScreen(session, screenid, screen)

# @router.delete("/screen/delete-screen/{screenid}")
# def delScreen(screenid:int, session:Session = Depends(get_db)):
#     return deleteScreen(session, screenid)


# --------------- screen seats --------------------

# @router.post("/screen/seat/create-screen/")
# def createSeat(seat: CreateSeat, session:Session = Depends(get_db)):
#     return addSeats(session, seat)


# ---------------------- Movies  -------------------------

# @router.get("/movies/")
# def movies(session:Session = Depends(get_db)):
#     return getAllMoview(session)

# @router.post("/movies/create-movies/")
# def createMovie(movie:CreateMovies, session:Session = Depends(get_db)):
#     return addMovies(session, movie)


# ---------------------- Show ------------------------

# @router.get("/show/all-shows/")
# def allShows(session:Session = Depends(get_db)):
#     return getAllShows(session)

# @router.get("/theter-show/{tid}")
# def theter_show(tid:int,session:Session = Depends(get_db)):    
#     return getTheterShows(session, tid)

# @router.post("/show/create-show/")
# def createshow(show:CreateShows, session:Session = Depends(get_db)):
#     return addShow(session, show)


# ------------------------- Booking ------------------------

@router.post("/users/booking/new-booking/")
def createBooking(booking:CreateBooking, session:Session = Depends(get_db)):
    return addBooking(session, booking)

@router.get("/booking")
def bookings(session:Session = Depends(get_db)):
    return getAllBookings(session)

@router.get("/users/booking/user-booking/{uid}")
def userBooking(uid:int,session:Session = Depends(get_db)):
    return getUsersBooking(session, uid)

@router.get("/users/cancelled-booking/{uid}")
def cancelBookings(uid:int,session:Session = Depends(get_db)):
    return usersCancelBooking(session, uid)

@router.delete("/users/booking/cancel-booking/")
def cancelBooking(bookingid:int,seatid: int, session:Session = Depends(get_db)):
    return CancelBooking(session, bookingid,seatid)

# @router.get('/seatsinfo')
# def seatsInfo(session:Session = Depends(get_db)):
#     return getAllSeats(session)


