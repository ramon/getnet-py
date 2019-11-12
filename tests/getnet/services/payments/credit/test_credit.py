import unittest

from getnet.services.payments.credit import Credit
from getnet.services.payments.credit.card import Card
from getnet.services.payments.order import Order

sample = {
    "delayed": False,
    "authenticated": False,
    "pre_authorization": False,
    "save_card_data": False,
    "transaction_type": "FULL",
    "number_installments": 1,
    "soft_descriptor": "LOJA*TESTE*COMPRA-123",
    "dynamic_mcc": 1799,
    "card": {
        "number_token": "dfe05208b105578c070f806c80abd3af09e246827d29b866cf4ce16c205849977c9496cbf0d0234f42339937f327747075f68763537b90b31389e01231d4d13c",
        "cardholder_name": "JOAO DA SILVA",
        "security_code": "123",
        "brand": "mastercard",
        "expiration_month": "12",
        "expiration_year": "20",
    },
}


class CreditTest(unittest.TestCase):
    def testInvalidTransactionType(self):
        data = sample.copy()
        data["transaction_type"] = "BUG"
        with self.assertRaises(TypeError):
            Credit(**data)

    def testInvalidSoftDescriptor(self):
        data = sample.copy()
        data["soft_descriptor"] = "BUG" * 10
        with self.assertRaises(TypeError):
            Credit(**data)

    def testConvertDictCardAsCard(self):
        obj = Credit(**sample.copy())
        self.assertIsInstance(obj.card, Card)


if __name__ == "__main__":
    unittest.main()
