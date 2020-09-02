import unittest
from unittest.mock import patch, MagicMock

from getnet import Client
from getnet.errors import RequestError
from getnet.services import token
from getnet.services.token.card_token import CardToken


class ClientTest(unittest.TestCase):
    def testInvalidEnvironment(self):
        with self.assertRaises(AttributeError):
            Client("a", "b", "c", 10)

    def testInvalidAuthData(self):
        with self.assertRaises(RequestError):
            Client(
                "d1c3d817-1676-4e28-a789-1e10c3af15b0",
                "d1c3d817-1676-4e28-a789-1e10c3af15b0",
                "388183f9-ab04-4c21-9234",
            )

    @patch("getnet.Client.auth", return_value=True)
    @patch("requests.Session.get", return_value=MagicMock())
    def testValidateAuthDataBeforeRequest(self, getMock, authMock):
        client = Client(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "388183f9-ab04-4c21-9234",
        )

        getMock.ok.return_value = True
        client.access_token_expired = MagicMock(return_value=False)
        client.get("/test")
        client.access_token_expired.assert_called_once()

    @patch("getnet.Client.auth", return_value=True)
    def testTokenService(self, *args):
        client = Client(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "388183f9-ab04-4c21-9234",
        )
        self.assertIsInstance(client.token_service(), token.Service)

    @patch("getnet.Client.auth", return_value=True)
    @patch.object(token.Service, "generate")
    def testGenerateTokenCardShortcut(self, tokenServiceMock, _):
        tokenServiceMock.return_value = CardToken("123")
        client = Client("id", "secret", "seller")

        response = client.generate_token_card("5155901222280001", "customer_21081826")

        self.assertEqual("123", response.number_token)
        tokenServiceMock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
