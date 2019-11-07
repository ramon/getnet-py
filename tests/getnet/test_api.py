import unittest
from unittest.mock import patch, MagicMock

import getnet
from getnet.exceptions import GetnetException


class ClientTest(unittest.TestCase):
    def testInvalidEnvironment(self):
        with self.assertRaises(GetnetException):
            getnet.API('a', 'b', 'c', 10)

    def testInvalidAuthData(self):
        with self.assertRaises(GetnetException):
            getnet.API(
                "d1c3d817-1676-4e28-a789-1e10c3af15b0",
                "d1c3d817-1676-4e28-a789-1e10c3af15b0",
                "388183f9-ab04-4c21-9234",
            )

    @patch('getnet.API.auth', return_value=True)
    @patch('requests.Session.get', return_value=True)
    def testValidateAuthDataBeforeRequest(self, getMock, authMock):
        client = getnet.API(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "388183f9-ab04-4c21-9234"
        )

        client._access_token_expired = MagicMock(return_value=False)
        client.get('/test')
        client._access_token_expired.assert_called_once()

if __name__ == "__main__":
    unittest.main()
