from getnet.services.base import ServiceBase
from getnet.services.token.card_number import CardNumber
from getnet.services.token.card_token import CardToken

class Service(ServiceBase):
    path = "/v1/tokens/card"

    def generate(self, card: CardNumber):
        response = self._post(self.path, json=card.as_dict())
        return CardToken(response.get('number_token'))
