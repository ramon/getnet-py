import os

from vcr_unittest import VCRTestCase

import getnet
from getnet.services.token import Service, CardNumber, CardToken


class TokenIntegrationTest(VCRTestCase):
    def setUp(self) -> None:
        super(TokenIntegrationTest, self).setUp()
        self.client = getnet.API(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
            getnet.api.HOMOLOG
        )
        self.service = Service(self.client)

    def testTokenGenerate(self):
        number_token = self.service.generate(CardNumber('5155901222280001', 'customer_21081826'))

        self.assertIsInstance(number_token, CardToken)
        self.assertIsNotNone(number_token.number_token)
