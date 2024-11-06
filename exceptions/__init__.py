class InvalidSession(BaseException):
    ...

class ApiChangeDetected(BaseException):
    def __init__(self):
        self.message = 'API change detected'
        super().__init__(self.message)

class GetUserInfoError(BaseException):
    ...
