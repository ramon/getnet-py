import pytest

from getnet.services.plans import Plan, Period
from getnet.services.plans.plan import ProductType


def test_period_conversion(plan_sample):
    plan = Plan(**plan_sample)
    assert isinstance(plan.period, Period)


def test_product_type_as_str(plan_sample):
    plan_sample["product_type"] = "service"
    plan = Plan(**plan_sample)
    assert isinstance(plan.product_type, ProductType)
    assert plan.product_type == ProductType.SERVICE


def test_invalid_product_type(plan_sample):
    with pytest.raises(AttributeError):
        plan_sample["product_type"] = "invalid"
        Plan(**plan_sample)
