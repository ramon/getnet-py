import re
from typing import Union, List

from getnet.services.token import CardToken
from .base import ServiceBase

BRANDS = ("Mastercard", "Visa", "Amex", "Elo", "Hipercard")
CARD_STATUS = ("all", "active", "renewed")

CARDHOLDER_IDENTIFICATION_REGEX = re.compile(r"\A\d+\Z")
VERIFY_CODE = re.compile(r"\A\d{3,4}\Z")


class Card:
    card_id: str
    number_token: CardToken
    expiration_month: str
    expiration_year: str
    brand: str
    cardholder_name: str
    last_four_digits: str
    customer_id: str
    used_at: str
    created_at: str
    updated_at: str
    status: str

    def __init__(
            self,
            card_id: str,
            number_token: Union[CardToken, str],
            brand: str = None,
            cardholder_name: str = None,
            last_four_digits: str = None,
            expiration_month: str = None,
            expiration_year: str = None,
            customer_id: str = None,
            used_at=None,
            created_at=None,
            updated_at=None,
            status: str = None,
    ):
        self.last_four_digits = last_four_digits
        self.updated_at = updated_at
        self.created_at = created_at
        self.used_at = used_at
        self.customer_id = customer_id
        self.expiration_year = expiration_year
        self.expiration_month = expiration_month
        self.cardholder_name = cardholder_name
        self.brand = brand
        self.status = status
        self.card_id = card_id
        self.number_token = (
            number_token
            if isinstance(number_token, CardToken)
            else CardToken(number_token)
        )

    def __eq__(self, other: 'Card'):
        return self.card_id == other.card_id


class CardService(ServiceBase):
    path = "/v1/cards/{card_id}"

    def create(
            self,
            number_token: CardToken,
            brand: str,
            cardholder_name: str,
            cardholder_identification: str,
            security_code: str,
            expiration_month: str,
            expiration_year: str,
            customer_id: str,
            verify_card: bool = False,
    ) -> Card:
        if not brand in BRANDS:
            raise AttributeError("Brand is invalid")

        if not CARDHOLDER_IDENTIFICATION_REGEX.match(cardholder_identification):
            raise AttributeError("Cardholder identification invalid")

        if not VERIFY_CODE.match(security_code):
            raise AttributeError("Security code invalid")

        data = {
            "number_token": str(number_token),
            "brand": brand,
            "cardholder_name": cardholder_name,
            "cardholder_identification": cardholder_identification,
            "security_code": security_code,
            "expiration_month": expiration_month,
            "expiration_year": expiration_year,
            "customer_id": customer_id,
            "verify_card": verify_card,
        }

        response = self._post(self._format_url(), json=data)

        return Card(
            card_id=response.get("card_id"), number_token=response.get("number_token")
        )

    def all(self, customer_id: str = None, status: str = None) -> List[Card]:
        if status and not status in CARD_STATUS:
            raise AttributeError("Status invalid.")

        response = self._get(
            self._format_url(), params={"customer_id": customer_id, "status": status}
        )

        cards = []

        for card in response.get("cards"):
            cards.append(Card(**card))

        return cards

    def get(self, card_id: Union[CardToken, str]) -> Card:
        response = self._get(
            self._format_url(card_id=str(card_id))
        )

        return Card(**response)

    def delete(self, card_id: Union[CardToken, str]) -> None:
        response = self._delete(
            self._format_url(card_id=str(card_id))
        )
