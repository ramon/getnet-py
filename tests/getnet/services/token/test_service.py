import unittest
from unittest.mock import patch

from getnet.services.token import Service, CardNumber, CardToken


@patch("getnet.API")
class ServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.card_number = CardNumber('5155901222280001', 'customer_21081826')

    def testGenerate(self, clientMock):
        clientMock.post.return_value = {'number_token': '123456789'}

        service = Service(clientMock)
        token = service.generate(self.card_number)

        self.assertIsInstance(token, CardToken)
        self.assertEqual(token.number_token, '123456789')


if __name__ == "__main__":
    unittest.main()
