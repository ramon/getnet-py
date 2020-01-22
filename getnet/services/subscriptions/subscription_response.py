from datetime import datetime
from typing import Union

from dateutil import parser

from getnet.services.cards.card_response import CardResponse
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


class PaymentErrorResponse:
    acquirer_transaction_id: str
    description: str
    description_detail: str
    error_code: str
    payment_id: str
    status: str
    terminal_nsu: str

    def __init__(self, error=dict):
        if 'error' in error:
            self.acquirer_transaction_id = error.pop('acquirer_transaction_id')
            self.description = error.pop('description')
            self.description_detail = error.pop('description_detail')
            self.error_code = error.pop('error_code')
            self.payment_id = error.pop('payment_id')
            self.status = error.pop('status')
            self.terminal_nsu = error.pop('terminal_nsu')

    # def __init__(self, credit: dict, payment_received_timestamp: str, **kwargs):
    #     kwargs["received_at"] = payment_received_timestamp
    #     super(PaymentResponse, self).__init__(**kwargs)
    #     if "authorization_timestamp" in credit:
    #         credit["authorized_at"] = credit.pop("authorization_timestamp")
    #     credit["card"] = None
    #     self.credit = BaseCreditResponse(**credit)


class SubscriptionResponse(Subscription):
    subscription_id: str
    create_date: datetime
    end_date: datetime
    payment_date: int
    next_scheduled_date: datetime
    plan: PlanResponse
    status: str
    payment: PaymentErrorResponse
    customer: Customer
    credit: CreditResponse

    def __init__(
        self,
        create_date: str,
        payment_date: str,
        next_scheduled_date: str,
        subscription: dict,
        plan: dict,
        status: str,
        customer: dict,
        end_date: str = None,
        payment: dict = None,
        **kwargs,
    ):
        self.create_date = parser.isoparse(create_date)
        self.end_date = end_date if end_date is None else parser.isoparse(end_date)
        self.payment_date = int(payment_date)
        self.next_scheduled_date = (
            parser.isoparse(next_scheduled_date)
            if next_scheduled_date is not None
            else next_scheduled_date
        )
        self.plan = PlanResponse(**plan)
        self.status = status
        print(payment)
        self.payment = PaymentErrorResponse(**payment) if payment is not None and 'error' not in payment else None
        self.subscription_id = subscription.get("subscription_id")
        self.customer = Customer(**customer)

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
