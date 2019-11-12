import unittest

from getnet.services.payments.boleto import Boleto

sample = {
    "our_number": "000001946598",
    "document_number": "170500000019763",
    "expiration_date": "16/11/2017",
    "instructions": "Não receber após o vencimento",
    "provider": "santander"
}


class BoletoTest(unittest.TestCase):
    def testInvalidDocumentNumber(self):
        data = sample.copy()
        data["document_number"] = "BUG"*10
        with self.assertRaises(TypeError):
            Boleto(**data)

    def testInvalidInstructions(self):
        data = sample.copy()
        data["instructions"] = "BUG" * 1000
        with self.assertRaises(TypeError):
            Boleto(**data)



if __name__ == "__main__":
    unittest.main()
