class UserExceptions(Exception):
    ...

class UserNotFoundError(UserExceptions):
    def __init__(self):
        self.status_code = 404
        self.error_msg = "User Info Not Found"

class UserNotAddError(UserExceptions):
    def __init__(self):
        self.status_code = 304
        self.error_msg = "Failed to add a new user please try again"