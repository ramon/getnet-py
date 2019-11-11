import unittest
from unittest.mock import patch, MagicMock

from requests import Response

import getnet
from getnet.exceptions import GetnetException
from getnet.services.token import Service
from getnet.services.token.card_token import CardToken


class ClientTest(unittest.TestCase):
    def testInvalidEnvironment(self):
        with self.assertRaises(TypeError):
            getnet.Client('a', 'b', 'c', 10)

    def testInvalidAuthData(self):
        with self.assertRaises(GetnetException):
            getnet.Client(
                "d1c3d817-1676-4e28-a789-1e10c3af15b0",
                "d1c3d817-1676-4e28-a789-1e10c3af15b0",
                "388183f9-ab04-4c21-9234",
            )

    @patch('getnet.Client.auth', return_value=True)
    @patch('requests.Session.get', return_value=MagicMock())
    def testValidateAuthDataBeforeRequest(self, getMock, authMock):
        client = getnet.Client(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "388183f9-ab04-4c21-9234"
        )

        getMock.ok.return_value = True
        client._access_token_expired = MagicMock(return_value=False)
        client.get('/test')
        client._access_token_expired.assert_called_once()

    @patch('getnet.Client.auth', return_value=True)
    @patch.object(Service, 'generate')
    def testGenerateTokenCardShortcut(self, tokenServiceMock, clientMock):
        tokenServiceMock.return_value = CardToken("123")
        client = getnet.Client("id", "secret","seller")

        token = client.generate_token_card("5155901222280001", "customer_21081826")

        self.assertEqual("123", token.number_token)
        tokenServiceMock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
