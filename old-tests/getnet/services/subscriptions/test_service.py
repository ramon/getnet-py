import unittest
from unittest.mock import patch

from getnet.services.service import ResponseList
from getnet.services.subscriptions import Service, Subscription
from getnet.services.subscriptions.subscription_response import SubscriptionResponse
from tests.getnet.services.subscriptions.test_subscription import sample
from tests.getnet.services.subscriptions.test_subscription_response import (
    sample as response_sample,
)


@patch("getnet.Client")
class ServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        data = sample.copy()
        self.sample = data

    def testCreate(self, client_mock):
        client_mock.post.return_value = response_sample

        service = Service(client_mock)
        response = service.create(Subscription(**sample))

        self.assertIsInstance(response, SubscriptionResponse)
        self.assertIsNotNone(response_sample.get("create_date"))

    def testAll(self, client_mock):
        client_mock.get.return_value = {
            "subscriptions": [response_sample, response_sample, response_sample],
            "page": 1,
            "limit": 100,
            "total": 3,
        }

        service = Service(client_mock)
        responses = service.all()

        self.assertIsInstance(responses, ResponseList)
        self.assertEqual(1, responses.page)
        self.assertEqual(3, responses.total)
        self.assertEqual(sample.get("order_id"), str(responses[0].order_id))

    def testGet(self, client_mock):
        client_mock.get.return_value = response_sample

        service = Service(client_mock)
        response = service.get(
            response_sample.get("subscription").get("subscription_id")
        )

        self.assertIsInstance(response, SubscriptionResponse)
        self.assertEqual(sample.get("order_id"), str(response.order_id))
        client_mock.get.assert_called_once_with(
            "/v1/subscriptions/{}".format(
                response_sample.get("subscription").get("subscription_id")
            )
        )

    def testCancel(self, client_mock):
        client_mock.post.return_value = response_sample

        service = Service(client_mock)
        response = service.cancel(
            response_sample.get("subscription").get("subscription_id"), "Cancel Message"
        )

        self.assertIsInstance(response, SubscriptionResponse)
        self.assertEqual(sample.get("order_id"), str(response.order_id))
        client_mock.post.assert_called_once_with(
            "/v1/subscriptions/{}/cancel".format(
                response_sample.get("subscription").get("subscription_id")
            ),
            json=unittest.mock.ANY,
        )


if __name__ == "__main__":
    unittest.main()
