import os
import unittest

from vcr_unittest import VCRTestCase

import getnet
from getnet import NotFound
from getnet.services.plans import Service, Plan
from getnet.services.service import ResponseList
from tests.getnet.services.plans.test_plan import sample


class PlansIntegrationTest(VCRTestCase):
    def setUp(self) -> None:
        super(PlansIntegrationTest, self).setUp()
        self.client = getnet.Client(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
            getnet.client.HOMOLOG,
        )
        self.service = Service(self.client)

    def testCreate(self):
        data = sample.copy()

        plan = self.service.create(Plan(**data))
        self.assertIsInstance(plan, Plan)
        self.assertIsNotNone(plan.plan_id)

    def testGet(self):
        data = sample.copy()
        created_plan = self.service.create(Plan(**data))

        plan = self.service.get(created_plan.plan_id)

        self.assertIsInstance(plan, Plan)
        self.assertEqual(created_plan, plan)
        self.assertEqual(created_plan.plan_id, plan.plan_id)

    def testInvalidGet(self):
        with self.assertRaises(NotFound) as err:
            self.service.get("14a2ce5d-ebc3-49dc-a516-cb5239b02285")

        self.assertEqual("Not Found", err.exception.error_code)

    def testAll(self):
        plans = self.service.all()
        self.assertIsInstance(plans, ResponseList)
        self.assertEqual(1, plans.page)
        self.assertEqual(100, plans.limit)
        self.assertIsNotNone(plans.total)

    def testAllNotFound(self):
        plans = self.service.all(name="foobarTest123")
        self.assertEqual(0, plans.total)

    def testUpdate(self):
        data = sample.copy()
        created_plan = self.service.create(Plan(**data))

        plan1 = self.service.update(
            created_plan.plan_id, "FooBar #1", created_plan.description
        )
        self.assertEqual("FooBar #1", plan1.name)

        plan2 = self.service.update(created_plan, "FooBar #2")
        self.assertEqual("FooBar #2", plan2.name)

        created_plan.name = "FooBar #3"
        plan3 = self.service.update(created_plan)
        self.assertEqual("FooBar #3", plan3.name)

    def testUpdateStatus(self):
        data = sample.copy()
        created_plan = self.service.create(Plan(**data))
        self.assertTrue(created_plan.is_active)

        plan = self.service.update_status(created_plan.plan_id, False)
        self.assertFalse(plan.is_active)


if __name__ == "__main__":
    unittest.main()
