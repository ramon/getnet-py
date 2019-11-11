from requests import RequestException


class GetnetException(RequestException):
    def __init__(self, *args, **kwargs):
        self.error_code = kwargs.pop('error_code')
        self.description = kwargs.pop('description')
        super(GetnetException, self).__init__(*args, **kwargs)

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
