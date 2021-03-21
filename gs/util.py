class Error(Exception):
    def __init__(self, msg, status):
        self.msg    = msg
        self.status = status

class InvaildValueException(Error):
    pass

class PathParameterException(Error):
    pass

class PermissionException(Exception):
    def __init__(self, msg="unauthorization", status=403):
        self.msg    = msg
        self.status = status

class NoSignUpException(Exception):
    def __init__(self, msg="unauthorization", status=403):
        self.msg    = msg
        self.status = status

class InfoDeletedException(Exception):
    def __init__(self, msg="not_exist_information", status=400):
        self.msg    = msg
        self.status = status
