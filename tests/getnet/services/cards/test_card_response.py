import unittest
import uuid

from getnet.services.cards.card_response import CardResponse
from getnet.services.token.card_token import CardToken

sample = {
    "card_id": uuid.UUID("e8ad2ae4-9e3e-4532-998f-1a5a11e56e58"),
    "number_token": CardToken("123"),
    "brand": "visa",
    "cardholder_name": "John Doe",
    "cardholder_identification": "5155901222280001",
    "security_code": "123",
    "expiration_month": "02",
    "expiration_year": "25",
    "customer_id": "johndoe",
    "verify_card": True,
    "last_four_digits": "1212",
    "used_at": "2017-04-19T16:30:30.003Z",
    "created_at": "2017-04-19T16:30:30.003Z",
    "updated_at": "2017-04-19T16:30:30.003Z",
    "status": "active",
    "bin": "123",
}


class CardResponseTest(unittest.TestCase):
    def testInvalidInitWithoutCardId(self):
        with self.assertRaises(TypeError):
            data = sample.copy()
            data.pop("card_id")
            CardResponse(**data)

    def testAsDict(self):
        data = sample.copy()
        card = CardResponse(**data)
        value = card._as_dict()
        self.assertNotIn("used_at", value)
        self.assertNotIn("created_at", value)
        self.assertNotIn("updated_at", value)


if __name__ == "__main__":
    unittest.main()
