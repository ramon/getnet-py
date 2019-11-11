import unittest

from getnet.services import CustomerService, Customer
from getnet.services.customers.customer import CustomerList

try:
    import mock
except ImportError:
    from unittest import mock

sample = {
    "seller_id": "6eb2412c-165a-41cd-b1d9-76c575d70a28",
    "customer_id": "customer_21081826",
    "first_name": "João",
    "last_name": "da Silva",
    "document_type": "CPF",
    "document_number": "78075751159",
    "birth_date": "1976-02-21",
    "phone_number": "5551999887766",
    "celphone_number": "5551999887766",
    "email": "customer@email.com.br",
    "observation": "O cliente tem interesse no plano x.",
    "address": {
        "street": "Av. Brasil",
        "number": "1000",
        "complement": "Sala 1",
        "district": "São Geraldo",
        "city": "Porto Alegre",
        "state": "RS",
        "country": "Brasil",
        "postal_code": "90230060",
    },
}


class CustomerTest(unittest.TestCase):
    def xtest_create_invalid_document_type(self):
        with self.assertRaises(AttributeError):
            data = sample.copy()
            data.update({"document_type": "Error"})
            Customer(**data)

    def xtest_create_invalid_document_number(self):
        with self.assertRaises(AttributeError):
            data = sample.copy()
            data.update({"document_number": "0123456789"})
            Customer(**data)


class CustomerServiceTest(unittest.TestCase):
    return_all_sample = {
        "customers": [
            {
                "customer_id": "customer_21081826",
                "first_name": "João",
                "last_name": "da Silva",
                "document_type": "CPF",
                "document_number": "12345678912",
                "phone_number": "5551999887766",
                "celphone_number": "5551999887766",
                "email": "customer@email.com.br",
            }
        ],
        "page": 1,
        "limit": 10,
        "total": 1,
    }

    def setUp(self) -> None:
        with mock.patch("getnet.API") as MockAPI:
            self.api_mock = MockAPI.return_value
            self.object = CustomerService(self.api_mock)

    def xtest_create(self):
        self.api_mock.seller_id.return_value = "123"
        self.object._post = mock.MagicMock(return_value=sample)

        data = Customer(**sample)
        response = self.object.create(data)

        self.object._post.assert_called_with(
            self.object._format_url(),
            json=mock.ANY,
            headers=mock.ANY
        )

        self.assertIsInstance(response, Customer)
        self.assertEqual(response.customer_id, data.customer_id)

    def xtest_all(self):
        self.object._get = mock.MagicMock(return_value=self.return_all_sample)

        response = self.object.all()

        self.assertIsInstance(response, CustomerList)
        self.assertEqual(
            response[0].customer_id,
            self.return_all_sample["customers"][0]["customer_id"],
        )

    def xtest_get(self):
        self.api_mock.seller_id.return_value = "123"

        sample = self.return_all_sample["customers"][0]
        self.object._get = mock.MagicMock(return_value=sample)

        response = self.object._get(sample.get("customer_id"))

        self.object._get.assert_called_with(
            self.object._format_url(customer_id=sample.get("customer_id")),
            headers=mock.ANY
        )
        self.assertIsInstance(response, Customer)
        self.assertEqual(response.customer_id, sample.get("customer_id"))
