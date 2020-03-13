from datetime import datetime
from typing import Union

from dateutil import parser

from getnet.services.cards.card_response import CardResponse
from getnet.services.payments.credit.credit_response import (
    CreditResponse as BaseCreditResponse,
)
from getnet.services.payments.payment_response import (
    PaymentResponse as BasePaymentResponse,
)
from getnet.services.plans.plan_response import PlanResponse
from getnet.services.subscriptions.customer import Customer
from getnet.services.subscriptions.subscription import Subscription


class CreditResponse:
    card: CardResponse
    transaction_type: str
    number_installments: int

    def __init__(self, card: Union[CardResponse, dict], **kwargs):
        card.update({"customer_id": "", "number_token": ""})
        card = (
            card
            if isinstance(card, CardResponse) or card is None
            else CardResponse(**card)
        )
        kwargs["card"] = card


class PaymentResponse(BasePaymentResponse):
    credit: BaseCreditResponse

    def __init__(self, credit: dict, payment_received_timestamp: str, **kwargs):
        kwargs["received_at"] = payment_received_timestamp
        super(PaymentResponse, self).__init__(**kwargs)
        if "authorization_timestamp" in credit:
            credit["authorized_at"] = credit.pop("authorization_timestamp")
        credit["card"] = None
        self.credit = BaseCreditResponse(**credit)


class PaymentErrorResponse:
    def __init__(self, error):
        self.message = error.pop("message")
        self.name = error.pop("name")
        self.status_code = error.pop("status_code")
        self.details = error.pop("details")[0]

    @property
    def payment_id(self):
        return self.details.get("payment_id")

    @property
    def description(self):
        return self.details.get("description")

    @property
    def description_detail(self):
        return self.details.get("description_detail")

    @property
    def acquirer_transaction_id(self):
        return self.details.get("acquirer_transaction_id")

    @property
    def status(self):
        return self.details.get("status")

    @property
    def error_code(self):
        return self.details.get("error_code") \
 \
    @property
    def terminal_nsu(self):
        return self.details.get("terminal_nsu")


class SubscriptionResponse(Subscription):
    subscription_id: str
    create_date: datetime
    end_date: datetime
    payment_date: int
    next_scheduled_date: datetime
    plan: PlanResponse
    status: str
    status_details: str
    payment: Union[PaymentResponse, PaymentErrorResponse, None]
    customer: Customer
    credit: CreditResponse

    def __init__(
        self,
        create_date: str,
        payment_date: str,
        subscription: dict,
        plan: dict,
        status: str,
        customer: dict,
        status_details: str = None,
        next_scheduled_date: str = None,
        end_date: str = None,
        payment: dict = None,
        **kwargs,
    ):
        self.create_date = parser.isoparse(create_date)
        self.end_date = end_date if end_date is None else parser.isoparse(end_date)
        self.payment_date = int(payment_date)
        self.next_scheduled_date = (
            parser.isoparse(next_scheduled_date)
            if next_scheduled_date is not None and next_scheduled_date != ''
            else next_scheduled_date
        )
        self.plan = PlanResponse(**plan)
        self.status = status
        self.status_details = status_details
        self.subscription_id = subscription.get("subscription_id")
        self.customer = Customer(**customer)

        if payment is not None:
            self.payment = PaymentResponse(**payment) if 'error' not in payment else PaymentErrorResponse(**payment)
        else:
            self.payment = None

        kwargs.update(
            {
                "customer_id": self.customer.customer_id,
                "plan_id": self.plan.plan_id,
                "credit": None,
            }
        )
        super(SubscriptionResponse, self).__init__(**kwargs)

        credit = subscription.get("payment_type").get("credit")
        self.credit = CreditResponse(**credit)

    def as_dict(self):
        data = {
            "seller_id": str(self.seller_id),
            "customer_id": str(self.customer_id),
            "plan_id": str(self.plan_id),
            "order_id": self.order_id,
            "subscription": {"payment_type": {"credit": self.credit.as_dict()}},
        }

        if self.device is not None:
            data["devise"] = self.device.as_dict()

        return data
