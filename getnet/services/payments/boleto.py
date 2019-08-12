import re
from typing import Union, List

from datetime import datetime, date

from getnet.services import Customer
from getnet.services.payments import Order, Payment
from getnet.services.token import CardToken
from ..base import ServiceBase

BRANDS = ("Mastercard", "Visa", "Amex", "Elo", "Hipercard")
CARD_STATUS = ("all", "active", "renewed")

CARDHOLDER_IDENTIFICATION_REGEX = re.compile(r"\A\d+\Z")
VERIFY_CODE = re.compile(r"\A\d{3,4}\Z")


class Boleto:
    boleto_id: str
    bank: int
    our_number: str
    document_number: str
    issue_date: date
    expiration_date: date
    instructions: str
    provider: str

    status_code: int
    status_label: str
    typeful_line: str
    bar_code: str
    links: dict = {}

    def __init__(
        self,
        document_number: str,
        expiration_date: Union[date, str],
        instructions: str = None,
        our_number: str = None,
        provider: str = "santander",
        boleto_id: str = None,
        bank: int = None,
        issue_date: Union[date, str] = None,
        status_code: int = None,
        status_label: str = None,
        typeful_line: str = None,
        bar_code: str = None,
        _links: List[dict] = iter([]),
        _base_uri: str = None,
    ) -> None:
        if len(document_number) > 15:
            raise AttributeError("The document_number must have bellow 15 characters")

        if instructions and len(instructions) > 1000:
            raise AttributeError("The instrunctions must have bellow 1000 characters")

        self.document_number = document_number
        self.expiration_date = (
            datetime.strptime(expiration_date, "%d/%m/%Y")
            if expiration_date and not isinstance(expiration_date, date)
            else expiration_date
        )
        self.instructions = instructions
        self.our_number = our_number
        self.provider = provider
        self.boleto_id = boleto_id
        self.bank = bank
        self.issue_date = (
            datetime.strptime(issue_date, "%d/%m/%Y")
            if issue_date and not isinstance(issue_date, date)
            else issue_date
        )
        self.status_code = status_code
        self.status_label = status_label
        self.typeful_line = typeful_line
        self.bar_code = bar_code

        for link in _links:
            self.links[link.get("rel")] = "".join([_base_uri, link.get("href")])

    def toJSON(self):
        return {
            "our_number": self.our_number,
            "document_number": self.document_number,
            "expiration_date": self.expiration_date.strftime("%d/%m/%Y"),
            "instructions": self.instructions,
            "provider": self.provider,
        }


def _format_customer(customer: Customer):
    return {
        "first_name": customer.first_name,
        "name": customer.full_name,
        "document_type": customer.document_type,
        "document_number": customer.document_number,
        "billing_address": customer.address.toJSON(),
    }


class PaymentBoletoService(ServiceBase):
    path = "/v1/payments/boleto"

    def create(
        self,
        amount: int,
        currency: str,
        order: Order,
        boleto: Boleto,
        customer: Customer,
    ) -> Payment:
        data = {
            "seller_id": self._api.seller_id,
            "amount": amount,
            "currency": currency,
            "order": order.toJSON(),
            "boleto": boleto.toJSON(),
            "customer": _format_customer(customer),
        }

        response = self._post(self._format_url(), json=data)

        boleto = Boleto(_base_uri=self._api.base_url, **response.pop("boleto"))

        return Payment(boleto=boleto, **response)
