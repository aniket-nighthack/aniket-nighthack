import secrets
from passlib.context import CryptContext


def getAuthToken():
    return secrets.token_hex(nbytes=16)


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)
