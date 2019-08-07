import random
import unittest

from requests import HTTPError

import getnet


class APIAuthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = getnet.API(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "388183f9-ab04-4c21-9234-5bddeb381d7a",
        )

    def testAuth(self):
        self.assertIsNone(self.client.access_token)
        self.client.auth()
        self.assertIsNotNone(self.client.access_token)

    def testInvalidAuth(self):
        client = getnet.API(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0", "388183f9-ab04-4c21-9234"
        )
        with self.assertRaises(HTTPError):
            client.auth()

    def testGenerateCardToken(self):
        client = self.client.auth()
        self.assertIsNotNone(
            client.generate_token_card(
                "5155901222280001", "buyer-{}".format(random.randint(1, 1000))
            )
        )
