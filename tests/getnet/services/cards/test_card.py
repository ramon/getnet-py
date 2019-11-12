import unittest

from getnet.services.cards.card import Card
from getnet.services.token.card_token import CardToken

sample = {
    "number_token": CardToken("123"),
    "brand": "visa",
    "cardholder_name": "John Doe",
    "cardholder_identification": "5155901222280001",
    "security_code": "123",
    "expiration_month": "02",
    "expiration_year": "25",
    "customer_id": "johndoe",
    "verify_card": False,
}


class CardTest(unittest.TestCase):
    def testInvalidExpirationMonth(self):
        with self.assertRaises(TypeError):
            data = sample.copy()
            data["expiration_month"] = 13
            Card(**data)

    def testInvalidExpirationYear(self):
        with self.assertRaises(TypeError):
            data = sample.copy()
            data["expiration_year"] = 100
            Card(**data)

    def testInvalidCustomerId(self):
        with self.assertRaises(TypeError):
            data = sample.copy()
            data["customer_id"] = "1" * 101
            Card(**data)

    def testInvalidSecurityCode2(self):
        with self.assertRaises(TypeError):
            data = sample.copy()
            data["security_code"] = "12"
            Card(**data)

    def testInvalidSecurityCode5(self):
        with self.assertRaises(TypeError):
            data = sample.copy()
            data["security_code"] = "12345"
            Card(**data)

    def testNumberTokenAsStr(self):
        data = sample.copy()
        data["number_token"] = "12345"
        card = Card(**data)

        self.assertIsInstance(card.number_token, CardToken)
        self.assertEqual(card.number_token.number_token, "12345")

    def testInvalidBrand(self):
        with self.assertRaises(TypeError):
            data = sample.copy()
            data["brand"] = "12345"
            Card(**data)

    def testAsDict(self):
        card = Card(**sample)
        self.assertDictEqual(card.as_dict(), sample)


if __name__ == "__main__":
    unittest.main()
