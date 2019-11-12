import unittest

from getnet.services.plans import Plan, Period

sample = {
    "seller_id": "6eb2412c-165a-41cd-b1d9-76c575d70a28",
    "name": "Plano flex",
    "description": "Plano flex",
    "amount": 19990,
    "currency": "BRL",
    "payment_types": ["credit_card"],
    "sales_tax": 0,
    "product_type": "service",
    "period": {"type": "monthly", "billing_cycle": 12, "specific_cycle_in_days": 0},
}


class PlanTest(unittest.TestCase):
    def testPeriodConversion(self):
        plan = Plan(**sample)
        self.assertIsInstance(plan.period, Period)


if __name__ == "__main__":
    unittest.main()
