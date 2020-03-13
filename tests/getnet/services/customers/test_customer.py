import unittest

from getnet.services.customers import Customer, Address

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
    def testAddressConversion(self):
        data = sample.copy()
        customer = Customer(**data)

        self.assertIsInstance(customer.address, Address)
        self.assertEqual(
            customer.address.postal_code, data.get("address").get("postal_code")
        )


if __name__ == "__main__":
    unittest.main()
