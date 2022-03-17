from fastapi import APIRouter, Depends, status, HTTPException, Response
from User import schemas, model
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from User.model import *
from Connection import database
from Common.Helper import *
from Common import token, oauth

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)
get_db = database.get_db


@router.post('')
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    print("HELLO")
    user = db.query(UsersInfo).filter(
        UsersInfo.mobile == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    print(user.hash_password, request.password)
    if not Hash.verify(user.hash_password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    print(user.id)
    access_token = token.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
