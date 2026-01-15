class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email

class InvalidCredentialsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass
