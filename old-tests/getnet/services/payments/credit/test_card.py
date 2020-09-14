import unittest

from getnet.services.payments.credit.card import Card

sample = {
    "number_token": "dfe05208b105578c070f806c80abd3af09e246827d29b866cf4ce16c205849977c9496cbf0d0234f42339937f327747075f68763537b90b31389e01231d4d13c",
    "cardholder_name": "JOAO DA SILVA",
    "security_code": "123",
    "brand": "mastercard",
    "expiration_month": "12",
    "expiration_year": "20",
}


class CardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.obj = Card(**sample.copy())

    def testInitSetCustomerIdAndIdentification(self):
        self.assertEqual(self.obj.customer_id, "")
        self.assertIsNone(self.obj.cardholder_identification)

    def testAsDictIgnoreUselessFields(self):
        obj = self.obj._as_dict()

        self.assertNotIn("customer_id", obj)
        self.assertNotIn("verify_card", obj)
        self.assertNotIn("cardholder_identification", obj)


if __name__ == "__main__":
    unittest.main()
