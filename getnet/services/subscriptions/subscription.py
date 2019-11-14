from typing import Union
from uuid import UUID

from getnet.services.plans.plan_response import PlanResponse
from getnet.services.subscriptions.credit import Credit
from getnet.services.subscriptions.customer import Customer
from getnet.services.utils import Device


class Subscription:
    seller_id: str
    customer_id: str
    plan_id: str
    order_id: str
    credit: Credit
    device: Device

    def __init__(
        self,
        order_id: str,
        customer_id: Union[Customer, str],
        plan_id: Union[PlanResponse, UUID, str],
        credit: Union[Credit, dict],
        device: Union[Device, dict] = None,
        seller_id: str = None,
    ):
        self.customer_id = (
            customer_id.customer_id
            if isinstance(customer_id, Customer)
            else customer_id
        )
        self.plan_id = (
            plan_id.plan_id if isinstance(plan_id, PlanResponse) else str(plan_id)
        )
        self.order_id = order_id
        self.credit = (
            credit if isinstance(credit, Credit) or credit is None else Credit(**credit)
        )
        self.device = (
            device if isinstance(device, Device) or device is None else Device(**device)
        )
        self.seller_id = seller_id

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
