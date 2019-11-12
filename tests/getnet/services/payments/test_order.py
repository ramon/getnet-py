import unittest

from getnet.services.payments.order import Order
from getnet.services.token import CardNumber


class OrderTest(unittest.TestCase):
    def testInvalidOrderId(self):
        with self.assertRaises(TypeError):
            Order("1" * 40, 0, "service")

    def testInvalidProductType(self):
        with self.assertRaises(TypeError):
            Order("123", 0, "fail")

    def testAsDict(self):
        object = Order("123", 0, "service")
        self.assertDictEqual(
            {"order_id": "123", "sales_tax": 0, "product_type": "service"},
            object.as_dict(),
        )


if __name__ == "__main__":
    unittest.main()
