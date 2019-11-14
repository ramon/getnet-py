from datetime import datetime
from typing import Union
from uuid import UUID

from dateutil import parser

from getnet.services.plans.plan import Plan


class PlanResponse(Plan):
    plan_id: UUID
    create_date: Union[datetime, str] = None
    status: str = None

    def __init__(
        self, plan_id: Union[UUID, str], status: str, create_date: str = None, **kwargs
    ):
        self.plan_id = (
            plan_id if isinstance(plan_id, UUID) or plan_id is None else UUID(plan_id)
        )
        self.create_date = (
            parser.isoparse(create_date)
            if not isinstance(create_date, datetime) and create_date is not None
            else create_date
        )
        self.status = status
        super(PlanResponse, self).__init__(**kwargs)

    @property
    def is_active(self):
        return self.status == "active"

    def as_dict(self):
        data = __dict__.copy()
        data.pop("created_date")
        data.pop("status")

        plan_id = data.pop("plan_id")
        if plan_id is not None:
            data["plan_id"] = str(plan_id)

        return data
