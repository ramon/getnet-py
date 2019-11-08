import unittest
from unittest.mock import patch

from getnet.services.cards import Service, Card
from getnet.services.cards.card_response import CardResponse
from tests.getnet.services.cards.test_card import sample
from tests.getnet.services.cards.test_card_response import sample as response_sample


@patch("getnet.Client")
class ServiceTest(unittest.TestCase):
    def testCreate(self, client_mock):
        client_mock.post.return_value = response_sample

        service = Service(client_mock)
        card = service.create(Card(**sample))

        self.assertIsInstance(card, CardResponse)
        self.assertEqual(response_sample.get('card_id'), card.card_id)

    def testAll(self, client_mock):
        client_mock.get.return_value = {"cards": [response_sample, response_sample, response_sample]}

        service = Service(client_mock)
        cards = service.all()

        self.assertIsInstance(cards, list)
        self.assertEqual(3, len(cards))
        self.assertEqual(response_sample.get('card_id'), cards[0].card_id)

    def testDelete(self, client_mock):
        client_mock.delete.return_value = True

        service = Service(client_mock)
        card = service.delete(card_id="123")

        self.assertTrue(card)
        client_mock.delete.assert_called_once_with('/v1/cards/123')

    def testVerify(self, client_mock):
        client_mock.post.return_value = { "status": "VERIFIED" }

        service = Service(client_mock)
        response = service.verify(Card(**sample))

        self.assertIsInstance(response, bool)
        self.assertTrue(response)


if __name__ == "__main__":
    unittest.main()
