import unittest

from getnet.services.payments.credit.credit_response import CreditResponse
from getnet.services.payments.payment_response import PaymentResponse

sample = {
    "payment_id": "06f256c8-1bbf-42bf-93b4-ce2041bfb87e",
    "seller_id": "6eb2412c-165a-41cd-b1d9-76c575d70a28",
    "amount": 100,
    "currency": "BRL",
    "order_id": "6d2e4380-d8a3-4ccb-9138-c289182818a3",
    "status": "APPROVED",
    "received_at": "2017-03-19T16:30:30.764Z",
    "credit": {
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
    },
}


class CreditPaymentResponseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.obj = PaymentResponse(**sample.copy())

    def testConvertCredit(self):
        self.assertIsInstance(self.obj.credit, CreditResponse)

    def testSetCreditCardAsNone(self):
        self.assertIsNone(self.obj.credit.card)


if __name__ == "__main__":
    unittest.main()
