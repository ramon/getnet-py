import re

from .base import ServiceBase


class Token(ServiceBase):
    path = '/v1/tokens/card'

    card_number_regex = re.compile(r'\A\d{13,19}\Z')

    def call(self, card_number: str, customer_id: str):
        if not self.card_number_regex.match(card_number):
            raise AttributeError('Card Number is invalid, must contain only numbers and between 13 and 19 chars')

        response = self._post(self.path, data={'card_number': card_number, 'customer_id': customer_id})

        return response.get('number_token')



