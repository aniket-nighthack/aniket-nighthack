import secrets
from passlib.context import CryptContext
import re
from fastapi import APIRouter, Depends, HTTPException, Request, status


def getAuthToken():
    return secrets.token_hex(nbytes=16)


def getAlphaNumeric():
    return secrets.token_hex(nbytes=12)


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# mobile number validation
def numberValidation(mobile: int):
    phoneNumRegex = re.compile(r'^(\+[0-9]{2}[- ]?)?[0-9]{10}$')
    if not phoneNumRegex.match(str(mobile)):
        raise HTTPException(status_code=400,
                            detail=f"Phone number invalid {mobile}")
    return True


def alphaNumeric(string: str):
    if not string.isdigit():
        raise HTTPException(status_code=400,
                            detail=f"Contact number invalid {string}")
    return True


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)
