from enum import Enum, unique
from typing import Union, List, Optional

from getnet.services.plans.period import Period


@unique
class ProductType(Enum):
    CASH_CARRY = "cash_carry"
    DIGITAL_CONTENT = "digital_content"
    DIGITAL_GOODS = "digital_goods"
    GIFT_CARD = "gift_card"
    PHYSICAL_GOODS = "physical_goods"
    RENEW_SUBS = "renew_subs"
    SHAREWARE = "shareware"
    SERVICE = "service"


class Plan:
    seller_id: str
    name: str
    description: str
    amount: int
    currency: str
    payment_types: List[str] = ("credit_card",)
    sales_tax: int = 0
    product_type: Optional[Union[ProductType, str]]
    period: Period

    def __init__(
        self,
        name: str,
        amount: int,
        currency: str,
        payment_types: List[str] = ("credit_card",),
        sales_tax: int = 0,
        description: Optional[str] = None,
        product_type: Optional[ProductType] = None,
        seller_id: Optional[str] = None,
        period: Optional[Union[Period, dict]] = None,
    ):
        if isinstance(product_type, str):
            try:
                product_type = ProductType[product_type.upper()]
            except Exception:
                raise AttributeError("Invalid Product Type")

        self.product_type = product_type
        self.name = name
        self.description = description
        self.amount = amount
        self.currency = currency
        self.payment_types = payment_types
        self.sales_tax = sales_tax
        self.seller_id = seller_id
        self.period = period if isinstance(period, Period) else Period(**period)

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
        data["product_type"] = self.product_type.value

        period = data.pop("period")
        data["period"] = period.as_dict()

        return data
