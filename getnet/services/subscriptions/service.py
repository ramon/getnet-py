from typing import Union
from uuid import UUID

from getnet.services.service import Service, ResponseList
from getnet.services.subscriptions.card import Card
from getnet.services.subscriptions.subscription import Subscription
from getnet.services.subscriptions.subscription_response import SubscriptionResponse


class Service(Service):
    path = "/v1/subscriptions/{subscription_id}"

    def create(self, subscription: Subscription) -> SubscriptionResponse:
        subscription.seller_id = self._client.seller_id
        response = self._post(self._format_url(), json=subscription.as_dict())
        return SubscriptionResponse(**response)

    def all(
        self,
        page: int = 1,
        limit: int = 100,
        customer_id: str = None,
        plan_id: str = None,
        subscription_id: str = None,
        status: str = None,
        sort: str = "create_date",
        sort_type: str = "asc",
    ) -> ResponseList:
        if page <= 0:
            raise TypeError("page must be greater then 0")

        if not sort_type in ("asc", "desc"):
            raise TypeError("sort_type invalid. Choices: asc, desc")

        params = {
            "page": page,
            "limit": limit,
            "customer_id": customer_id,
            "plan_id": plan_id,
            "subscription_id": subscription_id,
            "status": status,
            "sort": sort,
            "sort_type": sort_type,
        }

        response = self._get(self._format_url(), params=params)

        values = [
            SubscriptionResponse(**subscription)
            for subscription in response.get("subscriptions")
        ]

        return ResponseList(
            values, response.get("page"), response.get("limit"), response.get("total")
        )

    def get(self, subscription_id: Union[UUID, str]) -> SubscriptionResponse:
        response = self._get(self._format_url(subscription_id=str(subscription_id)))
        return SubscriptionResponse(**response)

    def cancel(
        self, subscription_id: Union[UUID, str], details: str = None
    ) -> SubscriptionResponse:
        data = {"seller_id": self._client.seller_id, "status_details": details}

        response = self._post(
            self._format_url(path="/cancel", subscription_id=str(subscription_id)),
            json=data,
        )
        return SubscriptionResponse(**response)

    def change_payment_date(
        self, subscription_id: Union[UUID, str], day: int
    ) -> SubscriptionResponse:
        data = {"day": day}

        response = self._patch(
            self._format_url(path="/paymentDate", subscription_id=str(subscription_id)),
            json=data,
        )
        return SubscriptionResponse(**response)

    def change_payment_data(self, subscription_id: Union[UUID, str], card: Card):
        response = self._patch(
            self._format_url(
                path="/paymentType/credit/card", subscription_id=str(subscription_id)
            ),
            json=card._as_dict(),
        )

        return SubscriptionResponse(**response)
