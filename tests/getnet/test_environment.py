import unittest

from getnet import Environment


class EnvironmentTest(unittest.TestCase):
    def test_base_url(self):
        self.assertEqual("https://api-sandbox.getnet.com.br", Environment.SANDBOX.base_url())
        self.assertEqual("https://api-homologacao.getnet.com.br", Environment.HOMOLOG.base_url())
        self.assertEqual("https://api.getnet.com.br", Environment.PRODUCTION.base_url())


if __name__ == "__main__":
    unittest.main()
