import unittest
from unittest.mock import patch

from getnet.services.plans import Service, Plan
from getnet.services.plans.plan_response import PlanResponse
from getnet.services.service import ResponseList
from tests.getnet.services.plans.test_plan import sample

response_sample = sample.copy()
response_sample.update(
    {
        "plan_id": "51995e24-b1ae-4826-8e15-2a568a87abdd",
        "create_date": "2017-04-19T16:30:30Z",
        "status": "active",
    }
)


@patch("getnet.Client")
class ServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        data = sample.copy()
        self.sample = data

    def testCreate(self, client_mock):
        client_mock.post.return_value = response_sample

        service = Service(client_mock)
        plan = service.create(Plan(**sample))

        self.assertIsInstance(plan, Plan)
        self.assertEqual(response_sample.get("plan_id"), str(plan.plan_id))

    def testAll(self, client_mock):
        client_mock.get.return_value = {
            "plans": [response_sample, response_sample, response_sample],
            "page": 1,
            "limit": 100,
            "total": 3,
        }

        service = Service(client_mock)
        plans = service.all()

        self.assertIsInstance(plans, ResponseList)
        self.assertEqual(1, plans.page)
        self.assertEqual(3, plans.total)
        self.assertEqual(response_sample.get("plan_id"), str(plans[0].plan_id))

    def testGet(self, client_mock):
        client_mock.get.return_value = response_sample

        service = Service(client_mock)
        plan = service.get(response_sample.get("plan_id"))

        self.assertIsInstance(plan, PlanResponse)
        self.assertEqual(response_sample.get("plan_id"), str(plan.plan_id))
        client_mock.get.assert_called_once_with(
            "/v1/plans/{}".format(response_sample.get("plan_id"))
        )

    def testUpdate(self, client_mock):
        client_mock.patch.return_value = response_sample

        service = Service(client_mock)
        plan = service.update(response_sample.get("plan_id"), "Demo", "Demo Desc")

        client_mock.patch.assert_called_once_with(
            "/v1/plans/{}".format(response_sample.get("plan_id")),
            json={"name": "Demo", "description": "Demo Desc"},
        )

    def testUpdateStatus(self, client_mock):
        client_mock.patch.return_value = response_sample

        service = Service(client_mock)
        plan = service.update_status(response_sample.get("plan_id"), False)

        client_mock.patch.assert_called_once_with(
            "/v1/plans/{}/status/inactive".format(response_sample.get("plan_id")),
        )


if __name__ == "__main__":
    unittest.main()
