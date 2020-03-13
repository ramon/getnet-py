from datetime import datetime

from dateutil import parser


class ChargeResponse:
    seller_id: str
    charge_id: str
    subscription_id: str
    customer_id: str
    plan_id: str
    payment_id: str
    amount: int
    status: str
    scheduled_date: datetime
    create_date: datetime
    retry_number: int
    payment_date: datetime
    payment_type: str
    terminal_nsu: str
    authorization_code: str
    acquirer_transaction_id: str

    def __init__(
        self,
        seller_id: str,
        charge_id: str,
        subscription_id: str,
        customer_id: str,
        plan_id: str,
        payment_id: str,
        amount: int,
        status: str,
        scheduled_date: str,
        create_date: str,
        retry_number: int,
        payment_date: str,
        payment_type: str,
        terminal_nsu: str,
        authorization_code: str,
        acquirer_transaction_id: str,
    ):
        self.seller_id = seller_id
        self.charge_id = charge_id
        self.subscription_id = subscription_id
        self.customer_id = customer_id
        self.plan_id = plan_id
        self.payment_id = payment_id
        self.amount = amount
        self.status = status
        self.scheduled_date = (
            scheduled_date
            if isinstance(scheduled_date, datetime) or scheduled_date is None
            else parser.isoparse(scheduled_date)
        )
        self.create_date = (
            create_date
            if isinstance(create_date, datetime) or create_date is None
            else parser.isoparse(create_date)
        )
        self.retry_number = retry_number
        self.payment_date = (
            payment_date
            if isinstance(payment_date, datetime) or payment_date is None
            else parser.isoparse(payment_date)
        )
        self.payment_type = payment_type
        self.terminal_nsu = terminal_nsu
        self.authorization_code = authorization_code
        self.acquirer_transaction_id = acquirer_transaction_id
