import os
import random
import unittest

import getnet
from getnet.exceptions import APIException
from getnet.services import Card, CardToken


class APIAuthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = getnet.API(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
        )

    def testAuth(self):
        self.assertIsNone(self.client.access_token)
        self.client.auth()
        self.assertIsNotNone(self.client.access_token)

    def testInvalidAuth(self):
        client = getnet.API(
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "d1c3d817-1676-4e28-a789-1e10c3af15b0",
            "388183f9-ab04-4c21-9234",
        )
        with self.assertRaises(APIException):
            client.auth()

    def testGenerateCardToken(self):
        client = self.client.auth()
        self.assertIsNotNone(
            client.generate_token_card(
                "5155901222280001", "buyer-{}".format(random.randint(1, 1000))
            )
        )

    def testCardService(self):
        card_service = self.client.auth().cards()

        token_card = self.client.generate_token_card(
            "5155901222280001", "customer_21081826"
        )

        self.assertIsInstance(token_card, CardToken)

        verify_response = card_service.verify(
            number_token=token_card,
            brand="Mastercard",
            cardholder_name="JOAO DA SILVA",
            expiration_month="12",
            expiration_year="20",
            security_code="123"
        )

        self.assertIsInstance(verify_response, dict)
        self.assertEqual(verify_response.get('status'), "VERIFIED")

        create_response = card_service.create(
            number_token=token_card,
            brand="Mastercard",
            cardholder_name="JOAO DA SILVA",
            expiration_month="12",
            expiration_year="20",
            customer_id="customer_21081826",
            cardholder_identification="12345678912",
            verify_card=False,
            security_code="123",
        )
        self.assertIsInstance(create_response, Card)
        self.assertEqual(create_response.number_token, token_card)

        all_response = card_service.all(customer_id="customer_21081826")
        self.assertIsInstance(all_response, list)
        self.assertIn(create_response, all_response)

        get_response = card_service.get(create_response.card_id)
        self.assertIsInstance(get_response, Card)
        self.assertEqual(get_response, create_response)

        delete_response = card_service.delete(create_response.card_id)
        self.assertTrue(delete_response)
        with self.assertRaises(APIException) as e:
            card_service.get(create_response.card_id)
            self.assertFalse(e.response.ok)
