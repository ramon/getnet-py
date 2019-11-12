from requests import RequestException


class GetnetException(RequestException):
    def __init__(self, *args, **kwargs):
        self.error_code = kwargs.pop("error_code")
        self.description = kwargs.pop("description")
        super(GetnetException, self).__init__(*args, **kwargs)


# discontinued - Will be removed in version 1.1
APIException = GetnetException


class BadRequest(GetnetException):
    pass


class BusinessError(GetnetException):
    @property
    def details(self):
        return self.response.json().get("details")[0]

    @property
    def payment_id(self):
        return self.details.get("payment_id")

    @property
    def authorization_code(self):
        return self.details.get("authorization_code")

    @property
    def terminal_nsu(self):
        return self.details.get("terminal_nsu")

    @property
    def acquirer_transaction_id(self):
        return self.details.get("acquirer_transaction_id")

    @property
    def status(self):
        return self.details.get("status")


class NotFound(GetnetException):
    pass


class ServerError(GetnetException):
    pass


class ServiceUnavailable(GetnetException):
    pass


class GatewayTimeout(GetnetException):
    pass
