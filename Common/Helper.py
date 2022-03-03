import secrets 

def getAuthToken():
    return secrets.token_hex(nbytes=16)