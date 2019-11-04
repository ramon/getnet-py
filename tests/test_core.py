import os
import unittest
import uuid
from random import random

import getnet
from getnet.exceptions import APIException
from getnet.services import Card, CardToken, Customer, PlanService, Plan
from getnet.services.payments import Order, Boleto, Payment
from getnet.services.payments.credit import Credit
from tests.test_service_customer import sample as customer_sample


class APIAuthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = getnet.API(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
            getnet.api.HOMOLOG
        )

    def testAuth(self):
        self.assertIsNone(self.client.access_token)
        self.client.auth()
        self.assertIsNotNone(self.client.access_token)

    def testInvalidAuth(self):
        client = getnet.API(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "388183f9-ab04-4c21-9234",
        )
        with self.assertRaises(APIException):
            client.auth()

    def testGenerateCardToken(self):
        client = self.client.auth()
        self.assertIsNotNone(
            client.generate_token_card(
                "5155901222280001", "customer_21081826"
            )
        )

    def testCardService(self):
        card_service = self.client.auth().cards()

        token_card = self.client.generate_token_card(
            "5155901222280001", "customer_21081826"
        )

        self.assertIsInstance(token_card, CardToken)

        verify_response = card_service.verify(
            number_token=token_card,
            brand="Mastercard",
            cardholder_name="Luciano Santos",
            expiration_month="12",
            expiration_year="20",
            security_code="123",
        )

        self.assertIsInstance(verify_response, dict)
        self.assertEqual("VERIFIED", verify_response.get("status"))

        create_response = card_service.create(
            number_token=token_card,
            brand="Mastercard",
            cardholder_name="JOAO DA SILVA",
            expiration_month="12",
            expiration_year="20",
            customer_id="customer_21081826",
            cardholder_identification="12345678912",
            verify_card=False,
            security_code="123",
        )

        self.assertIsInstance(create_response, Card)
        self.assertEqual(token_card, create_response.number_token)

        all_response = card_service.all(customer_id="customer_21081826")
        self.assertIsInstance(all_response, list)
        self.assertIn(create_response, all_response)

        get_response = card_service.get(create_response.card_id)
        self.assertIsInstance(get_response, Card)
        self.assertEqual(create_response, get_response)

        delete_response = card_service.delete(create_response.card_id)
        self.assertTrue(delete_response)
        with self.assertRaises(APIException) as e:
            card_service.get(create_response.card_id)
            self.assertFalse(e.response.ok)

    def testPaymentCreditService(self):
        payment_service = self.client.auth().payment("credit")

        customer = Customer(**customer_sample)
        order = Order("6d2e4380-d8a3-4ccb-9138-c289182818a3", 0, "physical_goods")

        token_card = self.client.generate_token_card(
            "4012001037141112", "customer_21081826"
        )

        card = Card(
            card_id="123",
            number_token=token_card,
            brand="Visa",
            cardholder_name="Luciano Santos",
            security_code="123",
            expiration_month="12",
            expiration_year="20"
        )

        full_credit = Credit(
            card=card,
            soft_descriptor="Full Credit Card"
        )

        payment_response = payment_service.create(
            amount=100,
            currency="BRL",
            order=order,
            credit=full_credit,
            customer=customer
        )

        self.assertIsInstance(payment_response, Payment)
        self.assertIsNotNone(payment_response.payment_id)
        self.assertEqual(payment_response.status, "APPROVED")
        self.assertIsNotNone(payment_response.credit.transaction_id)

        payment_cancel_response = payment_response.cancel()
        self.assertIsInstance(payment_cancel_response, Payment)
        self.assertEqual(payment_cancel_response.payment_id, payment_response.payment_id)
        self.assertEqual(payment_cancel_response.status, "CANCELED")

    def testPaymentBoletoService(self):
        payment_service = self.client.auth().payment("boleto")

        order = Order("6d2e4380-d8a3-4ccb-9138-c289182818a3", 0, "physical_goods")
        boleto = Boleto(
            document_number="44181342000120",
            expiration_date="16/11/2019",
            instructions="Não receber após o vencimento",
        )
        customer = Customer(**customer_sample)

        try:
            response = payment_service.create(
                amount=100, currency="BRL", order=order, boleto=boleto, customer=customer
            )
        except Exception as e:
            print(e.response)

        self.assertIsInstance(response, Payment)
        self.assertIsNotNone(response.payment_id)
        self.assertEqual(2, len(response.boleto.links))
        self.assertEqual(
            response.boleto.links["boleto_pdf"],
            "".join(
                [
                    self.client.base_url,
                    "/v1/payments/boleto/{}/pdf".format(response.payment_id),
                ]
            ),
        )

    def testCustomerService(self):
        customer_service = self.client.auth().customers()
        customer_data = customer_sample.copy()
        customer_id = str(uuid.uuid4())
        document_number = str(random())[2:13]
        customer_data.update({
            'seller_id': self.client.seller_id,
            'customer_id': customer_id,
            'document_number': document_number
        })

        customer = Customer(**customer_data)

        try:
            response = customer_service.create(customer)

            self.assertIsInstance(response, Customer)
            self.assertEqual(customer_id, customer.customer_id)
            self.assertEqual(document_number, customer.document_number)
        except Exception as err:
            self.fail()

    def testPlanService(self):

        service = PlanService(self.client.auth())
        response = service.create(Plan(
            seller_id=self.client.seller_id,
            name="Plan Demo",
            description="Plan Demo",
            amount=1990,
            currency='BRL',
            product_type='service',
            period={
                'type': 'monthly',
                'billing_cycle': 12,
            }
        ))

        self.assertIsInstance(response, Plan)
        self.assertIsNotNone(response.plan_id)

        plans = service.all()
        self.assertEqual(plans[0].plan_id, response.plan_id)

        plan = service.get(response.plan_id)

        self.assertEqual(response.plan_id, plan.plan_id)

    def xtestSubscriptionService(self):
        pass
