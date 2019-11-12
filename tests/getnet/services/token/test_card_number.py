import unittest

from getnet.services.token import CardNumber


class CardNumberTest(unittest.TestCase):
    def testInvalidCardNumber(self):
        with self.assertRaises(AttributeError):
            CardNumber("123", "123")

    def testInvalidCustomerId(self):
        with self.assertRaises(AttributeError):
            CardNumber("5155901222280001", "a" * 101)

    def testAsDict(self):
        object = CardNumber("5155901222280001", "customer_21081826")
        self.assertDictEqual(
            {"card_number": "5155901222280001", "customer_id": "customer_21081826"},
            object.as_dict(),
        )


if __name__ == "__main__":
    unittest.main()
