# import os
# import unittest
# import uuid
# from random import random
#
# from vcr_unittest import VCRTestCase
#
# import getnet
# from getnet.services import customers, plans
# from getnet.services.payments.credit import Card
# from getnet.services.subscriptions import Service, Subscription
# from getnet.services.subscriptions.credit import Credit
# from getnet.services.subscriptions.customer import Customer
# from getnet.services.subscriptions.subscription_response import SubscriptionResponse, PaymentErrorResponse, \
#     PaymentResponse
# from tests.getnet.services.cards.test_card import sample as card_sample
# from tests.getnet.services.customers.test_customer import sample as customer_sample
#
#
# class SubscriptionIntegrationTest(VCRTestCase):
#     def setUp(self) -> None:
#         super(SubscriptionIntegrationTest, self).setUp()
#         self.client = getnet.Client(
#             os.environ.get("GETNET_SELLER_ID"),
#             os.environ.get("GETNET_CLIENT_ID"),
#             os.environ.get("GETNET_CLIENT_SECRET"),
#             getnet.client.HOMOLOG,
#         )
#         self.service = Service(self.client)
#
#         customer_service = customers.Service(self.client)
#         customer = Customer(**customer_sample.copy())
#         customer.customer_id = str(uuid.uuid4())
#         customer.document_number = str(random())[2:13]
#         self.customer = customer_service.create(customer)
#
#         plan_service = plans.Service(self.client)
#         self.plan = plan_service.create(
#             plans.Plan(
#                 seller_id=self.client.seller_id,
#                 name="Plan Demo",
#                 description="Plan Demo",
#                 amount=1990,
#                 currency="BRL",
#                 product_type="service",
#                 period={"type": "monthly", "billing_cycle": 12, },
#             )
#         )
#
#         self.card = Card(**card_sample.copy())
#
#     def testCreateInvalid(self):
#         card_token = self.client.generate_token_card(
#             "5155901222270002", "customer_21081826"
#         )
#         self.card.number_token = card_token
#
#         subscription = Subscription(
#             order_id="test-{}".format(str(random())[2:10]),
#             customer_id=self.customer.customer_id,
#             plan_id=self.plan.plan_id,
#             credit=Credit(card=self.card),
#         )
#
#         response = self.service.create(subscription)
#
#         self.assertIsInstance(response, SubscriptionResponse)
#         self.assertIsNotNone(response.subscription_id)
#         self.assertEqual(response.status, "failed")
#         self.assertIsInstance(response.payment, PaymentErrorResponse)
#
#     def testCreate(self):
#         card_token = self.client.generate_token_card(
#             "5155901222280001", "customer_21081826"
#         )
#         self.card.number_token = card_token
#
#         subscription = Subscription(
#             order_id="test-{}".format(str(random())[2:10]),
#             customer_id=self.customer.customer_id,
#             plan_id=self.plan.plan_id,
#             credit=Credit(card=self.card),
#         )
#
#         response = self.service.create(subscription)
#
#         self.assertIsInstance(response, SubscriptionResponse)
#         self.assertIsNotNone(response.subscription_id)
#         self.assertEqual(response.status, "success")
#         self.assertIsInstance(response.payment, PaymentResponse)
#
#     def testCancel(self):
#         card_token = self.client.generate_token_card(
#             "5155901222280001", "customer_21081826"
#         )
#         self.card.number_token = card_token
#
#         response = self.service.create(
#             Subscription(
#                 order_id="test-{}".format(str(random())[2:10]),
#                 customer_id=self.customer.customer_id,
#                 plan_id=self.plan.plan_id,
#                 credit=Credit(card=self.card),
#             )
#         )
#
#         self.assertIsInstance(response, SubscriptionResponse)
#         self.assertIsNotNone(response.subscription_id)
#         self.assertEqual(response.status, "success")
#
#         cancel_response = self.service.cancel(response.subscription_id, "Test Cancel")
#         self.assertEqual(cancel_response.status, "canceled")
#
#
# if __name__ == "__main__":
#     unittest.main()
