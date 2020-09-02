import unittest
from unittest.mock import patch

from getnet.services.cards import Service, Card
from getnet.services.cards.card_response import NewCardResponse
from getnet.services.service import ResponseList
from tests.getnet.services.cards.test_card import sample
from tests.getnet.services.cards.test_card_response import sample as response_sample


@patch("getnet.Client")
class ServiceTest(unittest.TestCase):
    def testCreate(self, client_mock):
        client_mock.post.return_value = {
            "card_id": "e8ad2ae4-9e3e-4532-998f-1a5a11e56e58",
            "number_token": "123",
        }

        service = Service(client_mock)
        card = service.create(Card(**sample))

        self.assertIsInstance(card, NewCardResponse)
        self.assertEqual("e8ad2ae4-9e3e-4532-998f-1a5a11e56e58", str(card.card_id))
        self.assertEqual("123", card.number_token)

    def testAll(self, client_mock):
        client_mock.get.return_value = {
            "cards": [response_sample, response_sample, response_sample]
        }

        service = Service(client_mock)
        cards = service.all("client_id")

        self.assertIsInstance(cards, ResponseList)
        self.assertIsNone(cards.page)
        self.assertEqual(3, cards.total)
        self.assertEqual(response_sample.get("card_id"), cards[0].card_id)

    def testDelete(self, client_mock):
        client_mock.delete.return_value = True

        service = Service(client_mock)
        card = service.delete(card_id="123")

        self.assertTrue(card)
        client_mock.delete.assert_called_once_with("/v1/cards/123")

    def testVerify(self, client_mock):
        client_mock.post.return_value = {"status": "VERIFIED"}

        service = Service(client_mock)
        response = service.verify(Card(**sample))

        self.assertIsInstance(response, bool)
        self.assertTrue(response)


if __name__ == "__main__":
    unittest.main()
