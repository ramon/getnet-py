from requests import RequestException


class GetnetException(RequestException):
    pass

# discontinued - Will be removed in version 1.1
APIException = GetnetException

class BadRequest(GetnetException):
    pass


class BusinessError(GetnetException):
    pass


class NotFound(GetnetException):
    pass


class ServerError(GetnetException):
    pass


class ServiceUnavailable(GetnetException):
    pass


class GatewayTimeout(GetnetException):
    pass
