from typing import Union
from uuid import UUID

from getnet.services.base import ServiceBase
from getnet.services.payments import Customer
from getnet.services.payments.credit.credit import Credit
from getnet.services.payments.credit.credit_response import CreditResponse
from getnet.services.payments.order import Order
from getnet.services.payments.payment_response import PaymentResponse
from getnet.services.utils import Device


class Service(ServiceBase):
    path = "/v1/payments/credit"

    def create(
        self,
        amount: int,
        currency: str,
        order: Order,
        credit: Credit,
        customer: Customer,
        device: Device = None,
    ) -> PaymentResponse:
        data = {
            "seller_id": self._client.seller_id,
            "amount": amount,
            "currency": currency,
            "order": order.as_dict(),
            "credit": credit.as_dict(),
            "customer": customer.as_dict(),
        }

        if device is not None:
            data["device"] = device.as_dict()

        response = self._post(self._format_url(), json=data)
        credit = CreditResponse(**response.pop("credit"))
        return PaymentResponse(credit=credit, **response)

    def cancel(self, payment_id: Union[UUID, str]):
        response = self._post(
            self._format_url(path="/{payment_id}/cancel", payment_id=str(payment_id))
        )
        return PaymentResponse(**response)
