from typing import Union
from uuid import UUID

from getnet.services.payments import Customer
from getnet.services.payments.credit.credit import Credit
from getnet.services.payments.credit.credit_cancel import CreditCancelPaymentResponse
from getnet.services.payments.credit.credit_response import CreditPaymentResponse
from getnet.services.payments.order import Order
from getnet.services.service import Service
from getnet.services.utils import Device


class Service(Service):
    path = "/v1/payments/credit"

    def create(
        self,
        amount: int,
        currency: str,
        order: Order,
        credit: Credit,
        customer: Customer,
        device: Device = None,
    ) -> CreditPaymentResponse:
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
        return CreditPaymentResponse(**response)

    def cancel(self, payment_id: Union[UUID, str]) -> CreditCancelPaymentResponse:
        response = self._post(
            self._format_url(path="/{payment_id}/cancel", payment_id=str(payment_id))
        )
        return CreditCancelPaymentResponse(**response)
