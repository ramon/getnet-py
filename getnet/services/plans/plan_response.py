from datetime import datetime
from typing import Union
from uuid import UUID

from dateutil import parser

from getnet.services.plans.plan import Plan


class PlanResponse(Plan):
    create_date: Union[datetime, str] = None
    status: str = None

    def __init__(
        self, plan_id: Union[UUID, str], create_date: int, status: str, **kwargs
    ):
        self.create_date = (
            parser.isoparse(create_date)
            if not isinstance(create_date, datetime)
            else create_date
        )
        self.status = status

        kwargs.update({"plan_id": plan_id})
        super(PlanResponse, self).__init__(**kwargs)

    @property
    def is_active(self):
        return self.status == "active"

    def as_dict(self):
        data = __dict__.copy()
        data.pop("created_date")
        data.pop("status")

        return data
