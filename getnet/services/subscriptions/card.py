from typing import Union

from getnet.services.cards import Card as BaseCard
from getnet.services.token.card_token import CardToken


class Card(BaseCard):
    def __init__(
        self,
        number_token: Union[CardToken, str],
        cardholder_name: str,
        expiration_month: str,
        expiration_year: str,
        brand: str = None,
        bin: str = None,
    ):
        if not 1 <= int(expiration_month) <= 12 or not 0 <= int(expiration_year) <= 99:
            raise TypeError("Expiration Month or Year must have 2 characters")

        self.number_token = (
            number_token
            if isinstance(number_token, CardToken)
            else CardToken(number_token)
        )
        self.cardholder_name = cardholder_name
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.brand = brand
        self.bin = bin

    def _as_dict(self):
        data = {
            "number_token": self.number_token.number_token,
            "cardholder_name": self.cardholder_name,
            "brand": self.brand,
            "expiration_month": str(self.expiration_month).zfill(2),
            "expiration_year": str(self.expiration_year).zfill(2),
            "bin": self.bin,
        }

        if self.brand is None:
            data.pop("brand")

        return data
