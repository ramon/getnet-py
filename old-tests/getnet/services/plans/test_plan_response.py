import unittest

from getnet.services.plans import Period
from getnet.services.plans.plan_response import PlanResponse

sample = {
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
}


class PlanResponseTest(unittest.TestCase):
    def testPeriodConversion(self):
        plan = PlanResponse(**sample)
        self.assertIsInstance(plan.period, Period)


if __name__ == "__main__":
    unittest.main()
