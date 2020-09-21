import random

import pytest

from getnet.services.plans.period import PeriodType
from getnet.services.plans.plan import ProductType


@pytest.fixture
def plan_sample():
    return {
        "seller_id": "6eb2412c-165a-41cd-b1d9-76c575d70a28",
        "name": f"Plano #{random.uniform(1,100)}",
        "description": "Plano flex",
        "amount": 19990,
        "currency": "BRL",
        "payment_types": ["credit_card"],
        "sales_tax": 0,
        "product_type": ProductType.SERVICE,
        "period": {"type": PeriodType.MONTHLY, "billing_cycle": 12, "specific_cycle_in_days": 0},
    }.copy()


@pytest.fixture
def plan_response_sample():
    return {
        "seller_id": "6eb2412c-165a-41cd-b1d9-76c575d70a28",
        "plan_id": "51995e24-b1ae-4826-8e15-2a568a87abdd",
        "name": "Plano flex",
        "description": "Plano flex",
        "amount": 19990,
        "currency": "BRL",
        "payment_types": ["credit_card"],
        "sales_tax": 0,
        "product_type": "service",
        "create_date": "2017-04-19T16:30:30Z",
        "status": "active",
        "period": {"type": "monthly", "billing_cycle": 12, "specific_cycle_in_days": 0},
    }.copy()
