from typing import List, Union

from getnet import GetnetException
from getnet.services.base import ServiceBase
from getnet.services.cards.card import Card
from getnet.services.cards.card_response import CardResponse
from getnet.services.token.card_token import CardToken

CARD_STATUS = ("all", "active", "renewed")

""""Getnet Cards ("Cofre") Service Endpoint

    moduleauthor:: Ramon Soares <ramonsoares@gmail.com>
"""


class Service(ServiceBase):
    path = "/v1/cards/{card_id}"

    def verify(self, card: Card) -> bool:
        response = self._post(self._format_url(card_id='verification'), json=card.as_dict())
        return response.get('status') == "VERIFIED"

    def create(self, card: Card) -> CardResponse:
        response = self._post(self._format_url(), json=card.as_dict())
        return CardResponse(**response)

    def all(self, customer_id: str = None, status: str = "all") -> List[CardResponse]:
        if status and not status in CARD_STATUS:
            raise AttributeError("Status invalid.")

        params = {"status": status}
        if customer_id is not None:
            params.update({'customer_id': customer_id})

        response = self._get(self._format_url(), params=params)

        cards = []
        for card in response.get('cards'):
            cards.append(CardResponse(**card))

        return cards

    def get(self, card_id: Union[CardToken, str]) -> CardResponse:
        response = self._get(self._format_url(card_id=str(card_id)))
        return CardResponse(**response)

    def delete(self, card_id: Union[CardToken, str]) -> bool:
        self._delete(self._format_url(card_id=str(card_id)))
        return True
