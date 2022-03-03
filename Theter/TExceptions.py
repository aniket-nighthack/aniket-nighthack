class TheterException(Exception):
    ...

class TheterNotFoundError(TheterException):
    def __init__(self):
        self.status_code = 404
        self.error_msg = "User Info Not Found"

class TheterNotAddError(TheterException):
    def __init__(self):
        self.status_code = 304
        self.error_msg = "Failed to add a new theter please try again"