from typing import Union, List
from uuid import UUID

from getnet.services.plans.period import Period

PRODUCT_TYPES = (
    "cash_carry",
    "digital_content",
    "digital_goods",
    "gift_card",
    "physical_goods",
    "renew_subs",
    "shareware",
    "service",
)


class Plan:
    seller_id: str
    name: str
    description: str
    amount: int
    currency: str
    payment_types: List[str] = ("credit_card",)
    sales_tax: int = 0
    product_type: str
    period: Period
    plan_id: UUID

    def __init__(
        self,
        name: str,
        amount: int,
        currency: str,
        payment_types: List[str] = ("credit_card",),
        sales_tax: int = 0,
        description: str = None,
        product_type: str = None,
        seller_id: str = None,
        period: Union[Period, dict] = None,
        plan_id: Union[UUID, str] = None,
    ):
        self.product_type = product_type
        self.name = name
        self.description = description
        self.amount = amount
        self.currency = currency
        self.payment_types = payment_types
        self.sales_tax = sales_tax
        self.seller_id = seller_id
        self.period = period if isinstance(period, Period) else Period(**period)
        self.plan_id = (
            plan_id if isinstance(plan_id, UUID) or plan_id is None else UUID(plan_id)
        )

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (self.seller_id, self.name, self.product_type) == (
            other.seller_id,
            other.name,
            other.product_type,
        )

    def as_dict(self):
        data = self.__dict__.copy()

        period = data.pop("period")
        data["period"] = period.as_dict()

        plan_id = data.pop("plan_id")
        if plan_id is not None:
            data["plan_id"] = str(plan_id)

        return data
