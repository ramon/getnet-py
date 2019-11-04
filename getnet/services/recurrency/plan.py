import re
from typing import Union, List

from datetime import datetime

from getnet.services.base import ServiceBase

PRODUCT_TYPES = (
    "cash_carry",
    "digital_content",
    "digital_goods",
    "gift_card",
    "physical_goods",
    "renew_subs",
    "shareware",
    "service"
)

PERIOD_TYPES = (
    "yearly",
    "monthly",
    "bimonthly",
    "quarterly",
    "semesterly",
    "specific"
)

class Period:
    type: str
    billing_cycle: int
    specific_cycle_in_days: int

    def __init__(
        self,
        type: str,
        billing_cycle: int,
        specific_cycle_in_days: int = None
    ):
        if type not in PERIOD_TYPES:
            raise AttributeError('Invalid Type')

        if type == 'specific' and specific_cycle_in_days is None:
            raise AttributeError("'specific_cycle_in_days' required is type is specific")

        self.type = type
        self.billing_cycle = billing_cycle
        self.specific_cycle_in_days = specific_cycle_in_days

    def toJSON(self):
        data = vars(self).copy()
        data.popitem()

        if self.type == 'specific':
            data['specific_cycle_in_days'] = self.specific_cycle_in_days

        return data


class Plan:
    seller_id: str
    name: str
    description: str
    amount: int
    currency: str
    payment_types: List[str] = ('credit_card',)
    sales_tax: int = 0
    product_type: str
    period: Period
    status: str

    def __init__(
        self,

        name: str,
        amount: int,
        currency: str,
        payment_types: List[str] = ('credit_card',),
        sales_tax: int = 0,
        description: str = None,
        product_type: str = None,
        seller_id: str = None,
        period: Union[Period, dict] = None,
        plan_id: str = None,
        create_date: Union[datetime, str] = None,
        status: str = None,
    ):
        self.product_type = product_type
        self.name = name
        self.description = description
        self.amount = amount
        self.currency = currency
        self.payment_types = payment_types
        self.sales_tax = sales_tax
        self.seller_id = seller_id
        self.plan_id = plan_id
        self.create_date = (
            datetime.strptime(create_date, '%Y-%m-%dT%H:%M:%S.%j%z')
            if create_date and not isinstance(create_date, datetime)
            else create_date
        )
        self.status = status

        if isinstance(period, dict):
            period = Period(**period)

        self.period = period

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (self.seller_id, self.name, self.product_type) == (
            other.seller_id,
            other.name,
            other.product_type,
        )

    def toJSON(self):
        data = vars(self).copy()
        data.popitem()
        data.popitem()
        data.popitem()
        data.popitem()

        data["period"] = self.period.toJSON()
        return data


class PlanList(list):
    def __init__(self, seq=(), page=1, limit=100, total=None):
        self.page = page
        self.limit = limit
        self.total = total
        super(PlanList, self).__init__(seq)


class PlanService(ServiceBase):
    path = "/v1/plans/{plan_id}"

    def create(self, plan: Plan) -> Plan:
        response = self._post(self._format_url(), json=plan.toJSON())

        return Plan(**response)

    def all(
        self,
        page: int = 1,
        limit: int = 100,
        plan_id: str = None,
        status: str = "active",
        name: str = None,
        sort: str = "name",
        sort_type: str = "asc",
    ) -> PlanList:
        if page <= 0:
            raise AttributeError("page must be greater then 0")

        if not sort_type in ("asc", "desc"):
            raise AttributeError("sort_type invalid. Choices: asc, desc")

        params = {
            "page": page,
            "limit": limit,
            "plan_id": plan_id,
            "status": status,
            "name": name,
            "sort": sort,
            "sort_type": "asc",
        }

        response = self._get(self._format_url(), params=params)

        values = [Plan(**plan) for plan in response.get("plans")]

        return PlanList(
            values, response.get("page"), response.get("limit"), response.get("total")
        )

    def get(self, plan_id: str):
        response = self._get(self._format_url(plan_id=plan_id))

        return Plan(**response)
