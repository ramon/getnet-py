import os
import unittest

from vcr_unittest import VCRTestCase

from getnet import Environment, Client
from getnet.services.token import Service, CardNumber
from getnet.services.token.card_token import CardToken


class TokenIntegrationTest(VCRTestCase):
    def setUp(self) -> None:
        super(TokenIntegrationTest, self).setUp()
        self.client = Client(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
            Environment.HOMOLOG
        )
        self.service = Service(self.client)

    def testTokenGenerate(self):
        number_token = self.service.generate(
            CardNumber("5155901222280001", "customer_21081826")
        )

        self.assertIsInstance(number_token, CardToken)
        self.assertIsNotNone(number_token.number_token)


if __name__ == "__main__":
    unittest.main()
