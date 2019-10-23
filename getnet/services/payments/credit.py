import re
from datetime import datetime
from typing import Union

from getnet.services import Customer, Card
from getnet.services.payments import Order, Payment
from ..base import ServiceBase

BRANDS = ("Mastercard", "Visa", "Amex", "Elo", "Hipercard")
CARD_STATUS = ("all", "active", "renewed")

CARDHOLDER_IDENTIFICATION_REGEX = re.compile(r"\A\d+\Z")
VERIFY_CODE = re.compile(r"\A\d{3,4}\Z")


def _format_customer(customer: Customer):
    return {
        "customer_id": customer.customer_id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "name": customer.full_name,
        "email": customer.email,
        "document_type": customer.document_type,
        "document_number": customer.document_number,
        "billing_address": customer.address.toJSON(),
    }


def _format_card(card: Card):
    data = {
        "number_token": str(card.number_token),
        "cardholder_name": card.cardholder_name,
        "security_code": card.security_code,
        "expiration_month": str(card.expiration_month),
        "expiration_year": str(card.expiration_year)
    }

    if card.brand is not None:
        data['brand'] = card.brand

    return data


class Credit:
    TRANSACTION_FULL = "FULL"
    TRANSACTION_INSTALL = "INSTALL_NO_INTEREST"
    TRANSACTION_INSTALL_WITH_INTEREST = "INSTALL_WITH_INTEREST"

    card: Card
    delayed: bool
    authenticated: bool
    pre_authorization: bool
    save_card_data: bool
    transaction_type: str
    number_installments: int
    soft_descriptor: str
    dynamic_mcc: int
    authorization_code: str
    authorized_at: datetime
    reason_code: int
    reason_message: str
    acquirer: str
    acquirer_transaction_id: str
    terminal_nsu: str
    transaction_id: str
    brand: str

    def __init__(
        self,
        card: Card = None,
        delayed: bool = False,
        authenticated: bool = False,
        pre_authorization: bool = False,
        save_card_data: bool = False,
        transaction_type: str = TRANSACTION_FULL,
        number_installments: int = 1,
        soft_descriptor: str = None,
        dynamic_mcc: int = None,
        authorization_code: str = None,
        authorized_at: Union[datetime, str] = None,
        reason_code: int = None,
        reason_message: str = None,
        acquirer: str = None,
        acquirer_transaction_id: str = None,
        terminal_nsu: str = None,
        transaction_id: str = None,
        brand: str = None
    ) -> None:
        if len(soft_descriptor) > 22:
            raise AttributeError("The soft_descriptor must have bellow 23 characters")

        self.card = card
        self.delayed = delayed
        self.authenticated = authenticated
        self.pre_authorization = pre_authorization
        self.save_card_data = save_card_data
        self.transaction_type = transaction_type
        self.number_installments = number_installments
        self.dynamic_mcc = dynamic_mcc
        self.authorization_code = authorization_code
        self.authorized_at = (
            datetime.strptime(authorized_at, '%Y-%m-%dT%H:%M:%S%z')
            if authorized_at and not isinstance(authorized_at, datetime)
            else authorized_at
        )
        self.reason_code = reason_code
        self.reason_message = reason_message
        self.acquirer = acquirer
        self.acquirer_transaction_id = acquirer_transaction_id
        self.terminal_nsu = terminal_nsu
        self.transaction_id = transaction_id
        self.brand = brand

    def toJSON(self):
        data = {
            "delayed": self.delayed,
            "authenticated": self.authenticated,
            "pre_authorization": self.pre_authorization,
            "save_card_data": self.save_card_data,
            "transaction_type": self.transaction_type,
            "number_installments": self.number_installments,
            "card": _format_card(self.card)
        }

        if self.dynamic_mcc is not None:
            data["dynamic_mcc"] = self.dynamic_mcc

        return data


class CreditCancel:
    canceled_at: datetime
    message: str

    def __init__(self, canceled_at: Union[datetime, str], message: str):
        self.message = message
        self.canceled_at = (
            datetime.strptime(canceled_at, '%Y-%m-%dT%H:%M:%S.%f%z')
            if canceled_at and not isinstance(canceled_at, datetime)
            else canceled_at
        )


class PaymentCreditService(ServiceBase):
    path = "/v1/payments/credit"

    def create(
        self,
        amount: int,
        currency: str,
        order: Order,
        credit: Credit,
        customer: Customer
    ) -> Payment:
        data = {
            "seller_id": self._api.seller_id,
            "amount": amount,
            "currency": currency,
            "order": order.toJSON(),
            "credit": credit.toJSON(),
            "customer": _format_customer(customer),
        }

        response = self._post(self._format_url(), json=data)

        credit = Credit(**response.pop("credit"))

        return Payment(credit=credit, service=self, **response)

    def cancel(self, payment_id: str):
        response = self._post(self._format_url(path="/{payment_id}/cancel", payment_id=payment_id))

        credit_cancel = CreditCancel(**response.pop("credit_cancel"))

        return Payment(credit_cancel=credit_cancel, **response)
