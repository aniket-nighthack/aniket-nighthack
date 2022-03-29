from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.Common import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    print('dffdf')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_details = token.verify_token(data, credentials_exception)
    if token_details.user_type == "admin":
        raise credentials_exception
    return token_details


def check_if_admin(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("checking admin")
    token_details = token.verify_token(data, credentials_exception)
    if token_details.user_type != "admin":
        raise credentials_exception
    return token_details


def check_if_merchant(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_details = token.verify_token(data, credentials_exception)

    # if token_details.role != "admin" and token_details.role != "merchant":
    #     raise credentials_exception
    if token_details.user_type != "tuser":
        raise credentials_exception
    return token_details
