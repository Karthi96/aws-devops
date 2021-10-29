class CustomException(Exception):
    error_message = "ERROR"
    status_code = 0

    def __init__(self, error_details):
        self.error_details = error_details


class AccessDeniedException(CustomException):
    error_message = "ACCESS_DENIED"
    status_code = 401

    def __init__(self):
        super().__init__({})


class BadRequestException(CustomException):
    error_message = "BAD_REQUEST"
    status_code = 400

    def __init__(self):
        super().__init__({})


class InternalServerErrorException(CustomException):
    error_message = "Oops, Something went wrong"
    status_code = 500

    def __init__(self):
        super().__init__({})


class UserNotFoundException(CustomException):
    error_message = "USER_NOT_FOUND"
    status_code = 404

    def __init__(self):
        super().__init__({})


class UserFoundException(CustomException):
    error_message = "USER_ALREADY_EXISTS"
    status_code = 404

    def __init__(self):
        super().__init__({})


EXCEPTIONS = (
    AccessDeniedException, BadRequestException, InternalServerErrorException, UserNotFoundException, UserFoundException)
