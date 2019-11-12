from typing import Union
from uuid import UUID

from getnet.services.customers import Customer
from getnet.services.plans import Plan


class Subscription:
    seller_id: UUID
    customer_id: str
    plan_id: UUID
    order_id: str
    payment_type: str
    device: str

    def __init__(
        self,
        customer: Union[Customer, UUID, str],
        plan: Union[Plan, UUID, str],
        order_id: str,
        payment_type: str,
        device: str,
    ):
        self.customer = customer
        self.plan = plan
        self.order_id = order_id
        self.payment_type = payment_type
        self.device = device
