import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from getnet.services import Token

@mock.patch('getnet.API')
class ServiceTokenTest(unittest.TestCase):
    def test_invalid_card_number(self, APIClass):
        token = Token(APIClass)
        with self.assertRaises(AttributeError):
            token.call('123', '312')
