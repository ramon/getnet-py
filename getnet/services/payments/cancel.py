from datetime import datetime

from getnet.services.base import ServiceBase


class Cancel:
    seller_id: str
    payment_id: str
    cancel_request_at: datetime
    cancel_request_id: str
    cancel_custom_key: str
    status: str

    def __init__(self, **kwargs):
        self.cancel_request_at = datetime.fromisoformat(kwargs.pop("cancel_request_at"))

        for key, val in kwargs.items():
            setattr(self, key, val)


class PaymentCancelService(ServiceBase):
    path = "/v1/payments/cancel/request"

    def request(self, payment_id: str, amount: int, cancel_custom_key: str) -> Cancel:
        data = {
            "payment_id": payment_id,
            "cancel_amount": amount,
            "cancel_custom_key": cancel_custom_key,
        }

        response = self._post(self._format_url(), json=data)

        return Cancel(**response)
