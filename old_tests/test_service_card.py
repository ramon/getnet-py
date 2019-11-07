import unittest

from getnet.services import CardService, Card
from getnet.services.token import CardToken

try:
    import mock
except ImportError:
    from unittest import mock


class CardServiceTest(unittest.TestCase):
    sample = {
        "number_token": CardToken("123"),
        "brand": "Visa",
        "cardholder_name": "John Doe",
        "cardholder_identification": "5155901222280001",
        "security_code": "123",
        "expiration_month": "02",
        "expiration_year": "25",
        "customer_id": "johndoe",
        "verify_card": True,
    }

    return_sample = {
        "card_id": "e8ad2ae4-9e3e-4532-998f-1a5a11e56e58",
        "number_token": "dfe05208b105578c070f806c80abd3af09e246827d29b866cf4ce16c205849977c9496cbf0d0234f42339937f327747075f68763537b90b31389e01231d4d13c",
    }

    return_all_sample = {
        "cards": [
            {
                "card_id": "e8ad2ae4-9e3e-4532-998f-1a5a11e56e58",
                "last_four_digits": "1212",
                "expiration_month": "12",
                "expiration_year": "20",
                "brand": "Mastercard",
                "cardholder_name": "JOAO DA SILVA",
                "customer_id": "customer_21081826",
                "number_token": "dfe05208b105578c070f806c80abd3af09e246827d29b866cf4ce16c205849977c9496cbf0d0234f42339937f327747075f68763537b90b31389e01231d4d13c",
                "used_at": "2017-04-19T16:30:30Z",
                "created_at": "2017-04-19T16:30:30Z",
                "updated_at": "2017-04-19T16:30:30Z",
                "status": "active",
            }
        ]
    }

    sample_verify = {
        "number_token": "dfe05208b105578c070f806c80abd3af09e246827d29b866cf4ce16c205849977c9496cbf0d0234f42339937f327747075f68763537b90b31389e01231d4d13c",
        "brand": "Mastercard",
        "cardholder_name": "JOAO DA SILVA",
        "expiration_month": "12",
        "expiration_year": "20",
        "security_code": "123",
    }

    return_verify = {
        "status": "VERIFIED",
        "verification_id": "ae267804-503c-4163-b1b1-f5da5120b74e",
        "authorization_code": "6964722471672911",
    }

    def setUp(self) -> None:
        self.api_mock = mock.patch("getnet.API")

        self.object = CardService(self.api_mock)

    def xtest_create_invalid_brand(self):
        with self.assertRaises(AttributeError):
            data = self.sample.copy()
            data.update({"brand": "mybrand"})
            self.object.create(**data)

    def xtest_create_invalid_cardholder_identification(self):
        with self.assertRaises(AttributeError):
            data = self.sample.copy()
            data.update({"cardholder_identification": "mybrand"})
            self.object.create(**data)

    def xtest_create_invalid_security_code(self):
        with self.assertRaises(AttributeError):
            data = self.sample.copy()
            data.update({"security_code": "12"})
            self.object.create(**data)

    def xtest_create(self):
        self.object._post = mock.MagicMock(return_value=self.return_sample)
        response = self.object.create(**self.sample)

        self.assertIsInstance(response, Card)

    def xtest_all(self):
        self.object._get = mock.MagicMock(return_value=self.return_all_sample)

        response = self.object.all()

        self.assertIsInstance(response, list)
        self.assertEqual(
            response[0].customer_id, self.return_all_sample["cards"][0]["customer_id"]
        )

    def xtest_get(self):
        sample = self.return_all_sample["cards"][0]
        self.object._get = mock.MagicMock(return_value=sample)

        response = self.object.get(sample.get("card_id"))

        self.object._get.assert_called_with(
            self.object._format_url(card_id=sample.get("card_id"))
        )
        self.assertIsInstance(response, Card)
        self.assertEqual(response.card_id, sample.get("card_id"))

    def xtest_delete(self):
        sample = self.return_all_sample["cards"][0]
        self.object._delete = mock.MagicMock(return_value=sample)

        self.object.delete(sample.get("card_id"))
        self.object._delete.assert_called_with(
            self.object._format_url(card_id=sample.get("card_id"))
        )

    def xtest_verify(self):
        self.object._post = mock.MagicMock(return_value=self.return_verify)
        self.object.verify(**self.sample_verify)
        self.object._post.assert_called_with(
            self.object._format_url(card_id="verification"), json=mock.ANY
        )
