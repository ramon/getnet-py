import unittest

from getnet.services.payments.boleto.boleto_response import BoletoPaymentResponse, BoletoResponse
from getnet.services.payments.credit.credit_response import CreditResponse, CreditPaymentResponse
from getnet.services.payments.payment_response import PaymentResponse

sample_credit = {
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

sample_boleto = {
    "payment_id": "599ca35059028b001023b323",
    "seller_id": "6eb2412c-165a-41cd-b1d9-76c575d70a28",
    "amount": 100,
    "currency": "BRL",
    "order_id": "6d2e4380-d8a3-4ccb-9138-c289182818a3",
    "status": "PENDING",
    "boleto": {
        "boleto_id": "e587cefe-8832-4fc0-acff-acc83dd66e9e",
        "bank": 27,
        "status_code": 1,
        "status_label": "EM ABERTO",
        "typeful_line": "03399.58910 93000.000013 94659.801016 8 71670000030015",
        "bar_code": "03398716700000300159589193000000019465980101",
        "issue_date": "17/05/2017",
        "expiration_date": "22/05/2017",
        "our_number": "000001946598",
        "document_number": "170500000019763",
        "_links": [
            {
                "href": "/v1/payments/boleto/593948e8589f66000ed575e0/pdf",
                "rel": "boleto_pdf",
                "type": "GET"
            },
            {
                "href": "/v1/payments/boleto/593948e8589f66000ed575e0/html",
                "rel": "boleto_html",
                "type": "GET"
            }
        ]
    }
}


class CreditPaymentResponseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.obj = CreditPaymentResponse(**sample_credit.copy())

    def testConvertCredit(self):
        self.assertIsInstance(self.obj.credit, CreditResponse)

    def testSetCreditCardAsNone(self):
        self.assertIsNone(self.obj.credit.card)


class BoletoPaymentResponseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.obj = BoletoPaymentResponse(**sample_boleto.copy())

    def testConvertBoleto(self):
        self.assertIsInstance(self.obj.boleto, BoletoResponse)


if __name__ == "__main__":
    unittest.main()
