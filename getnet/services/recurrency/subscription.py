from datetime import datetime
from typing import Union

from getnet.services import Credit, Customer, Payment
from getnet.services.base import ServiceBase
from getnet.services.payments.utils import Device
from getnet.services.recurrency import Plan


class SubscriptionPlan:
    credit: Credit

    def __init__(self, credit: Credit):
        self.credit = credit

    def toJSON(self):
        return {
            "payment_type": {
                "credit": self.credit.toSubscriptionJSON()
            }
        }


class Subscription:
    seller_id: str
    customer: Customer
    plan: Plan
    order_id: str
    credit: Credit
    device: Device
    status: str
    status_details: str
    create_date: datetime
    end_date: datetime
    payment_date: datetime
    next_scheduled_date: datetime
    payment: Payment
    subscription: SubscriptionPlan

    def __init__(
        self,
        order_id: str,
        customer: Customer,
        plan: Plan,
        subscription: SubscriptionPlan,
        seller_id: str = None,
        device: Device = None,
        status: str = None,
        status_details: str = None,
        create_date: datetime = None,
        end_date: datetime = None,
        payment_date: Union[int, datetime] = None,
        next_scheduled_date: datetime = None,
        payment: Payment = None
    ):
        self.customer = customer
        self.plan = plan
        self.order_id = order_id
        self.subscription = subscription
        self.device = device
        self.seller_id = seller_id
        self.status = status
        self.status_details = status_details
        self.payment = payment
        self.create_date = (
            datetime.strptime(create_date, '%Y-%m-%dT%H:%M:%S.%f%z')
            if create_date and not isinstance(create_date, datetime)
            else create_date
        )
        self.end_date = (
            datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%f%z')
            if end_date and not isinstance(end_date, datetime)
            else end_date
        )
        self.payment_date = (
            datetime.strptime(payment_date, '%Y-%m-%dT%H:%M:%S.%f%z')
            if payment_date and not isinstance(payment_date, datetime) and not isinstance(payment_date, int)
            else payment_date
        )
        self.next_scheduled_date = (
            datetime.strptime(next_scheduled_date, '%Y-%m-%dT%H:%M:%S.%f%z')
            if next_scheduled_date and not isinstance(next_scheduled_date, datetime)
            else next_scheduled_date
        )

    def toJSON(self):
        data = {
            "seller_id": str(self.seller_id),
            "customer_id": self.customer.customer_id,
            "plan_id": self.plan.plan_id,
            "order_id": self.order_id,
            "subscription": self.subscription.toJSON()
        }

        if self.device is not None:
            data["devise"] = self.device.toJSON()

        return data

class SubscriptionList(list):
    def __init__(self, seq=(), page=1, limit=100, total=None):
        self.page = page
        self.limit = limit
        self.total = total
        super(SubscriptionList, self).__init__(seq)


class SubscriptionService(ServiceBase):
    path = "/v1/subscriptions/{plan_id}"

    def create(self, subscription: Subscription) -> Subscription:
        response = self._post(self._format_url(), json=subscription.toJSON(), headers={ 'seller_id': self._api.seller_id })

        return Subscription(**response)

    def all(
        self,
        page: int = 1,
        limit: int = 100,
        plan_id: str = None,
        status: str = "active",
        name: str = None,
        sort: str = "name",
        sort_type: str = "asc",
    ) -> SubscriptionList:
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

        response = self._get(self._format_url(), params=params, headers={ 'seller_id': self._api.seller_id })

        values = [Subscription(**subscription) for subscription in response._get("subscription")]

        return SubscriptionList(
            values, response._get("page"), response._get("limit"), response._get("total")
        )

    def _get(self, plan_id: str) -> Subscription:
        response = self._get(self._format_url(plan_id=plan_id), headers={ 'seller_id': self._api.seller_id })

        return Subscription(**response)
