import os
import unittest

from vcr_unittest import VCRTestCase

import getnet
from getnet import BusinessError
from getnet.services.payments import Order, Customer
from getnet.services.payments.boleto import Boleto, Service
from getnet.services.payments.payment_response import PaymentResponse
from tests.getnet.services.customers.test_customer import sample as customer_sample


class PaymentBoletoIntegrationTest(VCRTestCase):
    def setUp(self) -> None:
        super(PaymentBoletoIntegrationTest, self).setUp()
        self.client = getnet.Client(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
            getnet.api.HOMOLOG,
        )
        self.service = Service(self.client)
        self.order = Order("6d2e4380-d8a3-4ccb-9138-c289182818a3", 0, "physical_goods")
        self.customer = Customer(**customer_sample.copy())

    def testCreate(self):
        boleto = Boleto(
            document_number="44181342000120",
            expiration_date="16/11/2019",
            instructions="Não receber após o vencimento",
        )

        response = self.service.create(
            amount=1000,
            currency="BRL",
            order=self.order,
            customer=self.customer,
            boleto=boleto,
        )

        self.assertIsInstance(response, PaymentResponse)
        self.assertIsNotNone(response.payment_id)
        self.assertEqual(response.status, "PENDING")
        self.assertIsNotNone(response.boleto.boleto_id)

    def testInvalidCreate(self):
        boleto = Boleto(
            document_number="44181342000120",
            expiration_date="16/11/2010",
            instructions="Não receber após o vencimento",
        )

        with self.assertRaises(BusinessError) as err:
            self.service.create(
                amount=1000,
                currency="BRL",
                order=self.order,
                customer=self.customer,
                boleto=boleto,
            )

        self.assertEqual("PAYMENTS-402", err.exception.error_code)
        self.assertEqual("DENIED", err.exception.status)


if __name__ == "__main__":
    unittest.main()
