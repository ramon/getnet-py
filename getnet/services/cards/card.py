"""
    module:: card
    :synopsis: Getnet Safe ("Cofre") Card entity
"""

import re
from typing import Union

from getnet.services.token.card_token import CardToken

BRANDS = ("Mastercard", "Visa", "Amex", "Elo", "Hipercard")
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

    def __init__(self,
                 customer_id: str,
                 number_token: Union[CardToken, str],
                 cardholder_name: str,
                 expiration_month: str,
                 expiration_year: str,
                 cardholder_identification: str,
                 security_code: str,
                 verify_card: bool = False,
                 brand: str = None):
        if brand is not None and brand not in BRANDS:
            raise AttributeError("Brand is invalid")

        if len(expiration_month) != 2 or len(expiration_year) != 2:
            raise AttributeError('Expiration Month or Year must have 2 characters')

        if len(customer_id) > 100:
            raise AttributeError('CustomerID must have bellow 100 characters.')

        if not CARDHOLDER_IDENTIFICATION_REGEX.match(cardholder_identification):
            raise AttributeError("Cardholder identification invalid")

        if not VERIFY_CODE.match(security_code):
            raise AttributeError("Security code must have 3 or 4 characters")

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
        return self.__dict__
