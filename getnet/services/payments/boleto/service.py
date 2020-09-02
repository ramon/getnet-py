from getnet.services.payments import Customer
from getnet.services.payments.boleto.boleto import Boleto
from getnet.services.payments.boleto.boleto_response import BoletoPaymentResponse
from getnet.services.payments.order import Order
from getnet.services.service import Service


class Service(Service):
    path = "/v1/payments/boleto"

    def create(
        self,
        amount: int,
        currency: str,
        order: Order,
        boleto: Boleto,
        customer: Customer,
    ) -> BoletoPaymentResponse:
        data = {
            "seller_id": self._client.seller_id,
            "amount": amount,
            "currency": currency,
            "order": order.as_dict(),
            "boleto": boleto.as_dict(),
            "customer": customer.as_dict(),
        }

        response = self._post(self._format_url(), json=data)
        return BoletoPaymentResponse(_base_uri=self._client.base_url, **response)
