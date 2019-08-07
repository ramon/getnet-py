import re

from getnet.services.token import CardToken
from .base import ServiceBase

BRANDS = ("Mastercard", "Visa", "Amex", "Elo", "Hipercard")
CARD_STATUS = ("all", "active", "renewed")

CARDHOLDER_IDENTIFICATION_REGEX = re.compile(r"\A\d+\Z")
VERIFY_CODE = re.compile(r"\A\d{3,4}\Z")


class Card:
    card_id: str
    number_token: CardToken


class CardService(ServiceBase):
    path = "/v1/cards/{card_id}"

    def create(
        self,
        number: CardToken,
        brand: str,
        cardholder_name: str,
        cardholder_identification: str,
        security_code: str,
        expiration_month: str,
        expiration_year: str,
        customer_id: str,
        verify_card: bool = False,
    ):
        pass

    def all(self, customer_id: str, status: str):
        pass

    def get(self, card_id: str):
        pass

    def delete(self, card_id):
        pass
