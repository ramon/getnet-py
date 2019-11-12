import ipaddress
import unittest

from getnet.services.utils import Device


class DeviceTest(unittest.TestCase):
    def testInvalidDeviceId(self):
        with self.assertRaises(TypeError):
            Device("127.0.0.1", "A" * 81)

    def testInvalidPDeviceUD(self):
        with self.assertRaises(ipaddress.AddressValueError):
            Device("127.0.0.300", "ABC")

    def testAsDict(self):
        object = Device("127.0.0.3", "ABC")
        self.assertDictEqual(
            {"ip_address": "127.0.0.3", "device_id": "ABC"}, object.as_dict(),
        )


if __name__ == "__main__":
    unittest.main()
