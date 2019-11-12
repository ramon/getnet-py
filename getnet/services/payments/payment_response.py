from datetime import datetime
from typing import Union
from uuid import UUID

from dateutil import parser

from getnet.services.payments.credit.credit_cancel import CreditCancel
from getnet.services.payments.credit.credit_response import CreditResponse


class PaymentResponse:
    payment_id: UUID
    seller_id: UUID
    amount: int
    currency: str
    order_id: str
    status: str
    boleto: object = None
    credit: CreditResponse = None
    credit_cancel: object = None
    received_at: str

    def __init__(
        self,
        payment_id: Union[UUID, str],
        seller_id: Union[UUID, str],
        amount: int,
        currency: str,
        order_id: str,
        status: str,
        received_at: str = None,
        credit: Union[CreditResponse, dict] = None,
        boleto: Union[object, dict] = None,
        credit_cancel: Union[object, dict] = None,
    ):
        self.payment_id = (
            payment_id if isinstance(payment_id, UUID) else UUID(payment_id)
        )
        self.seller_id = seller_id if isinstance(seller_id, UUID) else UUID(seller_id)
        self.amount = amount
        self.currency = currency
        self.order_id = order_id
        self.status = status
        self.received_at = (
            received_at
            if isinstance(received_at, datetime) or received_at is None
            else parser.isoparse(received_at)
        )
        self.credit = (
            credit
            if isinstance(credit, CreditResponse) or credit is None
            else CreditResponse(**credit)
        )
        self.boleto = boleto
        self.credit_cancel = (
            credit_cancel
            if isinstance(credit_cancel, CreditCancel) or credit_cancel is None
            else CreditCancel(**credit_cancel)
        )
