from getnet.services.charges.charge_response import ChargeResponse
from getnet.services.service import Service, ResponseList


class Service(Service):
    path = "/v1/charges"

    def all(
        self,
        page: int = 1,
        limit: int = 100,
        charge_id: str = None,
        subscription_id: str = None,
        status: str = None,
        start_date: str = None,
        end_date: str = None,
        scheduled_date: str = None,
        retries: int = None,
        sort: str = "create_date",
        sort_type: str = "asc",
    ) -> ResponseList:
        if page <= 0:
            raise TypeError("page must be greater then 0")

        if not sort_type in ("asc", "desc"):
            raise AttributeError("sort_type invalid. Choices: asc, desc")

        params = {
            "page": page,
            "limit": limit,
            "charge_id": charge_id,
            "subscription_id": subscription_id,
            "status": status,
            "start_date": start_date,
            "end_date": end_date,
            "scheduled_date": scheduled_date,
            "retries": retries,
            "sort": sort,
            "sort_type": "asc",
        }

        response = self._get(self._format_url(), params=params)

        values = [ChargeResponse(**charge) for charge in response.get("charges")]

        return ResponseList(
            values, response.get("page"), response.get("limit"), response.get("total")
        )
