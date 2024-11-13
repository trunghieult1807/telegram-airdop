class InvalidSession(BaseException):
    ...

class InvalidProtocol(BaseException):
    ...

class ApiChangeDetected(Exception):
    def __init__(self):
        self.message = 'API change detected'
        super().__init__(self.message)

class GetUserInfoError(Exception):
    ...
