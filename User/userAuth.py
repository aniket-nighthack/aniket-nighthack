from User.model import *
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import FastAPI, Header, Depends, Request, HTTPException, status
from User.api import *

class UserAuthentication():

    def isAuthenticated(self, token, session) -> UsersInfo:
        PREFIX = 'Bearer'
        bearer, _, token = token.partition(' ')
        if bearer != PREFIX:
            raise ValueError('Invalid token')

        user = session.query(UsersInfo).filter(UsersInfo.auth_token == token).first()
        if user:
            return True
        else:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unautheraised Request",
            headers={"WWW-Authenticate": "Basic"},
        )
