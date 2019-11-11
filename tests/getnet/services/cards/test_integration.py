import os
import unittest

from vcr_unittest import VCRTestCase

import getnet
from getnet import NotFound, GetnetException
from getnet.services.base import ResponseList
from getnet.services.cards import Service, Card
from getnet.services.cards.card_response import NewCardResponse
from tests.getnet.services.cards.test_card import sample


class CardsIntegrationTest(VCRTestCase):
    def setUp(self) -> None:
        super(CardsIntegrationTest, self).setUp()
        self.client = getnet.Client(
            os.environ.get("GETNET_SELLER_ID"),
            os.environ.get("GETNET_CLIENT_ID"),
            os.environ.get("GETNET_CLIENT_SECRET"),
            getnet.api.HOMOLOG
        )
        self.number_token = self.client.generate_token_card('5155901222280001', 'customer_01')
        self.service = Service(self.client)

    def testCreate(self):
        data = sample.copy()
        data['number_token'] = self.number_token
        card = self.service.create(Card(**data))

        self.assertIsInstance(card, NewCardResponse)
        self.assertEqual(self.number_token, card.number_token.number_token)

    def testInvalidCreate(self):
        with self.assertRaises(getnet.exceptions.BadRequest) as err:
            data = sample.copy()
            data['number_token'] = '123'
            self.service.create(Card(**data))

        self.assertEqual("TOKENIZATION-400", err.exception.error_code)

    def testGet(self):
        data = sample.copy()
        data['number_token'] = self.number_token
        sample_card = self.service.create(Card(**data))

        card = self.service.get(sample_card.card_id)

        self.assertIsInstance(card, Card)
        self.assertEqual(card, card)
        self.assertEqual(sample_card.card_id, card.card_id)

    def testInvalidGet(self):
        with self.assertRaises(getnet.exceptions.NotFound) as err:
            self.service.get('14a2ce5d-ebc3-49dc-a516-cb5239b02285')

        self.assertEqual("404", err.exception.error_code)

    def testAll(self):
        with self.assertRaises(TypeError):
            cards = self.service.all()

        cards = self.service.all(sample.get('customer_id'))
        self.assertIsInstance(cards, ResponseList)
        self.assertIsNone(cards.page)
        self.assertIsNone(cards.limit)
        self.assertIsNotNone(cards.total)

    def testAll404(self):
        with self.assertRaises(NotFound) as err:
            cards = self.service.all("foobar")

        self.assertEqual("404", err.exception.error_code)

    def testDelete(self):
        data = sample.copy()
        data['number_token'] = self.client.generate_token_card('5155901222280001', 'customer_01')

        try:
            created_card = self.service.create(Card(**data))
            card = self.service.get(created_card.card_id)

            resp = self.service.delete(card.card_id)
            self.assertTrue(resp)
        except GetnetException as err:
            self.fail("deu chabu")

    def testDelete404(self):
        with self.assertRaises(NotFound) as err:
            cards = self.service.delete("72402c54-6bd3-4895-a6b4-adfded0c11dc")

        self.assertEqual("VAULT-404", err.exception.error_code)


if __name__ == "__main__":
    unittest.main()
