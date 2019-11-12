import os
import unittest

from vcr_unittest import VCRTestCase

import getnet
from getnet import BadRequest, BusinessError
from getnet.services.payments import Order, Customer
from getnet.services.payments.credit import Service, Card, Credit
from getnet.services.payments.credit.credit_cancel import CreditCancel
from getnet.services.payments.payment_response import PaymentResponse
from tests.getnet.services.customers.test_customer import sample as customer_sample
from tests.getnet.services.payments.credit.test_card import sample as card_sample


class PaymentCreditIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        super(PaymentCreditIntegrationTest, self).setUp()
        self.client = getnet.Client(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
            getnet.api.HOMOLOG,
        )
        self.service = Service(self.client)
        self.order = Order("6d2e4380-d8a3-4ccb-9138-c289182818a3", 0, "physical_goods")
        self.customer = Customer(**customer_sample.copy())

    def xtestCreate(self):
        card_token = self.client.generate_token_card(
            "4012001037141112", "customer_21081826"
        )
        card = Card(**card_sample.copy())
        card.number_token = card_token

        response = self.service.create(
            amount=100,
            currency="BRL",
            order=self.order,
            customer=self.customer,
            credit=Credit(card=card),
        )

        self.assertIsInstance(response, PaymentResponse)
        self.assertIsNotNone(response.payment_id)
        self.assertEqual(response.status, "APPROVED")
        self.assertIsNotNone(response.credit.transaction_id)

    def xtestCreateWithInstall(self):
        card_token = self.client.generate_token_card(
            "4012001037141112", "customer_21081826"
        )
        card = Card(**card_sample.copy())
        card.number_token = card_token

        response = self.service.create(
            amount=40606,
            currency="BRL",
            order=self.order,
            customer=self.customer,
            credit=Credit(
                card=card, transaction_type="INSTALL_NO_INTEREST", number_installments=6
            ),
        )

        self.assertIsInstance(response, PaymentResponse)
        self.assertIsNotNone(response.payment_id)
        self.assertEqual(response.status, "APPROVED")
        self.assertIsNotNone(response.credit.transaction_id)

    def xtestCreateWithInvalidInstall(self):
        card_token = self.client.generate_token_card(
            "4012001037141112", "customer_21081826"
        )
        card = Card(**card_sample.copy())
        card.number_token = card_token

        with self.assertRaises(BusinessError) as err:
            self.service.create(
                amount=40606,
                currency="BRL",
                order=self.order,
                customer=self.customer,
                credit=Credit(
                    card=card,
                    transaction_type="INSTALL_WITH_INTEREST",
                    number_installments=5,
                ),
            )

        self.assertEqual("PAYMENTS-011", err.exception.error_code)
        self.assertEqual("NOT APPROVED", err.exception.status)

    def testPaymentCancel(self):
        card_token = self.client.generate_token_card(
            "4012001037141112", "customer_21081826"
        )
        card = Card(**card_sample.copy())
        card.number_token = card_token

        response = self.service.create(
            amount=100,
            currency="BRL",
            order=self.order,
            customer=self.customer,
            credit=Credit(card=card),
        )

        self.assertIsInstance(response, PaymentResponse)
        self.assertIsNotNone(response.payment_id)
        self.assertEqual(response.status, "APPROVED")

        cancel_response = self.service.cancel(response.payment_id)
        self.assertEqual(cancel_response.status, "CANCELED")
        self.assertIsInstance(cancel_response.credit_cancel, CreditCancel)
        self.assertEqual(
            cancel_response.credit_cancel.message,
            "Credit transaction cancelled successfully",
        )


if __name__ == "__main__":
    unittest.main()
