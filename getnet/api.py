import requests
from requests import HTTPError

from getnet import services
from getnet.exceptions import APIException
from getnet.services.payments import PaymentBoletoService

SANDBOX = 0
HOMOLOG = 1
PRODUCTION = 2

API_URLS = {
    SANDBOX: "https://api-sandbox.getnet.com.br",
    HOMOLOG: "https://api-homologacao.getnet.com.br",
    PRODUCTION: "https://api.getnet.com.br",
}


class API:
    seller_id: str = None
    client_id: str = None
    client_secret: str = None
    access_token: str = None

    def __init__(
        self,
        seller_id: str,
        client_id: str,
        client_secret: str,
        environment: int = SANDBOX,
    ):
        self.seller_id = seller_id
        self.client_id = client_id
        self.client_secret = client_secret

        self.base_url = API_URLS[environment]

        self.request = requests.Session()
        self.request.headers.update({"user-agent": "getnet-py/0.1.0"})

    def _process_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except HTTPError as error:
            if 400 <= error.response.status_code < 500:
                message = u"{} {} ({})".format(
                    error.response.status_code,
                    error.response.json().get("message"),
                    error.response.url,
                )
                raise APIException(message, response=response)

    def get(self, path, **kwargs):
        url = self.base_url + path
        response = self.request.get(url, **kwargs)
        return self._process_response(response)

    def post(self, path: str, **kwargs):
        url = self.base_url + path
        response = self.request.post(url, **kwargs)
        return self._process_response(response)

    def put(self, path: str, data: dict, **kwargs):
        url = self.base_url + path
        response = self.request.put(url, data, **kwargs)
        return self._process_response(response)

    def delete(self, path: str, **kwargs) -> bool:
        url = self.base_url + path
        response = self.request.delete(url, **kwargs)
        if response.status_code != 204:
            return self._process_response(response)

        return True

    def auth(self) -> "API":
        if not self.access_token:
            path = "/auth/oauth/v2/token"
            data = {"scope": "oob", "grant_type": "client_credentials"}

            response = self.post(
                path, data=data, auth=(self.client_id, self.client_secret)
            )

            self.access_token = response.get("access_token")
            self.request.headers.update(
                {"Authorization": "Bearer {}".format(self.access_token)}
            )

        return self

    def generate_token_card(self, card_number: str, customer_id: str):
        return services.TokenCardService(self).create(card_number, customer_id)

    def cards(self):
        return services.CardService(self)

    def customers(self):
        return services.CustomerService(self)

    def payment(self, type: str):
        if type == "boleto":
            return PaymentBoletoService(self)
