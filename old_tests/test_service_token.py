import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from getnet.services import TokenCardService


@mock.patch("getnet.API")
class ServiceTokenTest(unittest.TestCase):
    def xtest_invalid_card_number(self, APIClass):
        token = TokenCardService(APIClass)
        with self.assertRaises(AttributeError):
            token.create("123", "312")
