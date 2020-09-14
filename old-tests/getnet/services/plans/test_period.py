import unittest

from getnet.services.plans import Period


class PeriodTest(unittest.TestCase):
    def testInvalidType(self):
        with self.assertRaises(TypeError):
            Period("Invalid", 1)

    def testRequireSpecificCycleIfTypeSpecific(self):
        with self.assertRaises(TypeError):
            Period("specific", 1)


if __name__ == "__main__":
    unittest.main()
