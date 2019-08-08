import re

from .base import ServiceBase


class CardToken:
    number: str

    def __init__(self, number: str):
        self.number = number

    def __str__(self):
        return self.number


class TokenCardService(ServiceBase):
    path = "/v1/tokens/card"

    card_number_regex = re.compile(r"\A\d{13,19}\Z")

    def create(self, card_number: str, customer_id: str) -> CardToken:
        if not self.card_number_regex.match(card_number):
            raise AttributeError(
                "Card Number is invalid, must contain only numbers and between 13 and 19 chars"
            )

        response = self._post(
            self.path, json={"card_number": card_number, "customer_id": customer_id}
        )

        return CardToken(response.get("number_token"))
