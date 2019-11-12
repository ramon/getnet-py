import unittest

from getnet.services.payments.credit.credit_response import CreditResponse

sample = {
    "delayed": False,
    "authorization_code": "000000099999",
    "authorized_at": "2017-03-19T16:30:30Z",
    "reason_code": 0,
    "reason_message": "transaction approved",
    "acquirer": "GETNET",
    "soft_descriptor": "Descrição para fatura",
    "brand": "Mastercard",
    "terminal_nsu": "0099999",
    "acquirer_transaction_id": "10000024",
    "transaction_id": "1002217281190421",
}


class CreditResponseTest(unittest.TestCase):
    def testSetCardAsNone(self):
        obj = CreditResponse(**sample.copy())

        self.assertIsNone(obj.card)


if __name__ == "__main__":
    unittest.main()
