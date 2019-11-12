"""
    module:: card
    :synopsis: Getnet Safe ("Cofre") Card entity
"""

import re
from typing import Union

from getnet.services.token.card_token import CardToken

BRANDS = ("mastercard", "visa", "amex", "elo", "hipercard")
CARDHOLDER_IDENTIFICATION_REGEX = re.compile(r"\A\d+\Z")
VERIFY_CODE = re.compile(r"\A\d{3,4}\Z")


class Card:
    customer_id: str
    number_token: CardToken
    brand: str = None
    cardholder_name: str
    expiration_month: str
    expiration_year: str
    cardholder_identification: str
    security_code: str
    verify_card: bool = False

    def __init__(
        self,
        customer_id: str,
        number_token: Union[CardToken, str],
        cardholder_name: str,
        expiration_month: int,
        expiration_year: int,
        cardholder_identification: str,
        security_code: str,
        verify_card: bool = False,
        brand: str = None,
    ):
        if brand is not None and brand not in BRANDS:
            raise TypeError("Brand is invalid")

        if not 1 <= int(expiration_month) <= 12 or not 0 <= int(expiration_year) <= 99:
            raise TypeError("Expiration Month or Year must have 2 characters")

        if len(customer_id) > 100:
            raise TypeError("CustomerID must have bellow 100 characters.")

        if (
            cardholder_identification is not None
            and not CARDHOLDER_IDENTIFICATION_REGEX.match(cardholder_identification)
        ):
            raise TypeError("Cardholder identification invalid")

        if security_code is not None and not VERIFY_CODE.match(security_code):
            raise TypeError("Security code must have 3 or 4 characters")

        self.customer_id = customer_id
        self.number_token = (
            number_token
            if isinstance(number_token, CardToken)
            else CardToken(number_token)
        )
        self.cardholder_name = cardholder_name
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.cardholder_identification = cardholder_identification
        self.security_code = security_code
        self.verify_card = verify_card
        self.brand = brand

    def as_dict(self):
        data = self.__dict__
        data["number_token"] = self.number_token.number_token
        data["expiration_month"] = str(self.expiration_month).zfill(2)
        data["expiration_year"] = str(self.expiration_year).zfill(2)
        return data
