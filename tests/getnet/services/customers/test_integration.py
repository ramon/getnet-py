import os
import unittest

from vcr_unittest import VCRTestCase

import getnet
from getnet import NotFound
from getnet.services.base import ResponseList
from getnet.services.customers import Service, Customer
from tests.getnet.services.customers.test_customer import sample


class CustomersIntegrationTest(VCRTestCase):
    def setUp(self) -> None:
        super(CustomersIntegrationTest, self).setUp()
        self.client = getnet.Client(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
            getnet.api.HOMOLOG
        )
        self.service = Service(self.client)

    def testCreate(self):
        data = sample.copy()
        data['document_number'] = "01234567888"

        customer = self.service.create(Customer(**data))
        self.assertIsInstance(customer, Customer)
        self.assertEqual(data.get('customer_id'), customer.customer_id)

    def testInvalidCreate(self):
        with self.assertRaises(getnet.BadRequest) as err:
            self.service.create(Customer(**sample))

        self.assertEqual("Bad Request", err.exception.error_code)

    def testGet(self):
        data = sample.copy()
        data['customer_id'] = "test_integration_get"
        data['document_number'] = "01234567811"
        created_customer = self.service.create(Customer(**data))

        customer = self.service.get(created_customer.customer_id)

        self.assertIsInstance(customer, Customer)
        self.assertEqual(created_customer, customer)
        self.assertEqual(created_customer.customer_id, customer.customer_id)

    def testInvalidGet(self):
        with self.assertRaises(NotFound) as err:
            self.service.get('14a2ce5d-ebc3-49dc-a516-cb5239b02285')

        self.assertEqual("Not Found", err.exception.error_code)

    def testAll(self):
        customers = self.service.all()
        self.assertIsInstance(customers, ResponseList)
        self.assertEqual(1, customers.page)
        self.assertEqual(100, customers.limit)
        self.assertIsNotNone(customers.total)

    def testAllNotFound(self):
        cards = self.service.all(document_number="01234567855")
        self.assertEqual(0, cards.total)


if __name__ == "__main__":
    unittest.main()
