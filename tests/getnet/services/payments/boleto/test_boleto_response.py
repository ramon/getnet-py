import unittest

from getnet.services.payments.boleto.boleto_response import BoletoResponse

sample = {
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
            "type": "GET",
        },
        {
            "href": "/v1/payments/boleto/593948e8589f66000ed575e0/html",
            "rel": "boleto_html",
            "type": "GET",
        },
    ],
}


class CreditResponseTest(unittest.TestCase):
    def testLinks(self):
        obj = BoletoResponse(**sample.copy())
        self.assertIsNotNone(obj.links["boleto_pdf"])
        self.assertIsNotNone(obj.links["boleto_html"])


if __name__ == "__main__":
    unittest.main()
