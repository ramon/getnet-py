from typing import Union
from uuid import UUID

from getnet.services.base import ServiceBase, ResponseList
from getnet.services.plans.plan import Plan
from getnet.services.plans.plan_response import PlanResponse


class Service(ServiceBase):
    path = "/v1/plans/{plan_id}"

    def create(self, plan: Plan) -> PlanResponse:
        plan.seller_id = self._client.seller_id
        response = self._post(self._format_url(), json=plan.as_dict())
        return PlanResponse(**response)

    def all(
        self,
        page: int = 1,
        limit: int = 100,
        plan_id: str = None,
        status: str = "active",
        name: str = None,
        sort: str = "name",
        sort_type: str = "asc",
    ) -> ResponseList:
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

        values = [PlanResponse(**plan) for plan in response.get("plans")]

        return ResponseList(
            values, response.get("page"), response.get("limit"), response.get("total")
        )

    def get(self, plan_id: Union[UUID, str]):
        response = self._get(self._format_url(plan_id=str(plan_id)))

        return PlanResponse(**response)

    def update(
        self, plan: Union[Plan, UUID, str], name: str = None, description: str = None
    ) -> PlanResponse:
        if isinstance(plan, str):
            plan_id = UUID(plan)
        elif isinstance(plan, Plan):
            plan_id = plan.plan_id
        else:
            plan_id = plan

        data = {
            "name": name or (plan.name if isinstance(plan, Plan) else ""),
            "description": description
            or (plan.description if isinstance(plan, Plan) else ""),
        }

        response = self._patch(self._format_url(plan_id=plan_id), json=data)
        return PlanResponse(**response)

    def update_status(
        self, plan: Union[Plan, UUID, str], active: bool = True
    ) -> PlanResponse:
        if isinstance(plan, str):
            plan_id = UUID(plan)
        elif isinstance(plan, Plan):
            plan_id = plan.plan_id
        else:
            plan_id = plan

        url = self._format_url(plan_id=plan_id) + "/status/{}".format(
            "active" if active else "inactive"
        )
        response = self._patch(url)
        return PlanResponse(**response)
