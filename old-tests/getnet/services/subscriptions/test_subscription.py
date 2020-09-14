import unittest

from getnet.services.plans.plan_response import PlanResponse
from getnet.services.subscriptions.credit import Credit
from getnet.services.subscriptions.customer import Customer
from getnet.services.subscriptions.subscription import Subscription
from tests.getnet.services.customers.test_customer import sample as customer_sample
from tests.getnet.services.payments.credit.test_credit import sample as credit_sample
from tests.getnet.services.plans.test_plan_response import sample as plan_sample

sample = {
    "seller_id": "eb523ac0-10e0-4acd-96b4-24436227e5b1",
    "customer_id": "customer_21081826",
    "plan_id": "51995e24-b1ae-4826-8e15-2a568a87abdd",
    "order_id": "test-99243222",
    "credit": {
        "transaction_type": "FULL",
        "number_installments": 1,
        "soft_descriptor": "LOJA*TESTE*COMPRA-123",
        "billing_address": {
            "street": "Av. Brasil",
            "number": "1000",
            "complement": "Sala 1",
            "district": "São Geraldo",
            "city": "Porto Alegre",
            "state": "RS",
            "country": "Brasil",
            "postal_code": "90230060",
        },
        "card": {
            "number_token": "dfe05208b105578c070f806c80abd3af09e246827d29b866cf4ce16c205849977c9496cbf0d0234f42339937f327747075f68763537b90b31389e01231d4d13c",
            "cardholder_name": "JOAO DA SILVA",
            "security_code": "123",
            "brand": "mastercard",
            "expiration_month": "12",
            "expiration_year": "20",
            "bin": "123412",
        },
    },
    "device": {"ip_address": "127.0.0.1", "device_id": "hash-device-id"},
}


class SubscriptionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.customer = Customer(**customer_sample)
        self.plan = PlanResponse(**plan_sample)
        self.credit = Credit(**credit_sample)
        self.obj = Subscription("123", self.customer, self.plan, self.credit)
        self.obj.seller_id = "123"

    def testInit(self):
        self.assertEqual(self.obj.customer_id, self.customer.customer_id)
        self.assertEqual(self.obj.plan_id, self.plan.plan_id)
        self.assertIsInstance(self.obj.credit, Credit)

    def testAsDict(self):
        data = self.obj.as_dict()
        self.assertDictEqual(
            self.credit.as_dict(),
            data.get("subscription").get("payment_type").get("credit"),
        )


if __name__ == "__main__":
    unittest.main()
