import unittest
from unittest.mock import patch

from getnet.services.base import ResponseList
from getnet.services.customers import Service, Customer
from tests.getnet.services.customers.test_customer import sample


@patch("getnet.Client")
class ServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        data = sample.copy()
        data['status'] = 'active'
        self.sample = data

    def testCreate(self, client_mock):
        client_mock.post.return_value = self.sample

        service = Service(client_mock)
        customer = service.create(Customer(**sample))

        self.assertIsInstance(customer, Customer)
        self.assertEqual(sample.get('customer_id'), customer.customer_id)

    def testAll(self, client_mock):
        client_mock.get.return_value = {
            "customers": [self.sample, self.sample, self.sample],
            "page": 1,
            "limit": 100,
            "total": 3
        }

        service = Service(client_mock)
        customers = service.all()

        self.assertIsInstance(customers, ResponseList)
        self.assertEqual(1, customers.page)
        self.assertEqual(3, customers.total)
        self.assertEqual(sample.get('customer_id'), customers[0].customer_id)

    def testGet(self, client_mock):
        client_mock.get.return_value = self.sample

        service = Service(client_mock)
        customer = service.get(sample.get('customer_id'))

        self.assertIsInstance(customer, Customer)
        self.assertEqual(sample.get('customer_id'), customer.customer_id)
        client_mock.get.assert_called_once_with('/v1/customers/{}'.format(sample.get('customer_id')))


if __name__ == "__main__":
    unittest.main()
