from datetime import datetime

from getnet.services.plans import Period
from getnet.services.plans.plan import ProductType
from getnet.services.plans.plan_response import PlanResponse


def test_attributes_conversion(plan_response_sample: dict):
    plan = PlanResponse(**plan_response_sample)
    assert isinstance(plan.period, Period)
    assert isinstance(plan.product_type, ProductType)
    assert isinstance(plan.create_date, datetime)
