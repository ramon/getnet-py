import requests

from getnet import services

SANDBOX = 0
HOMOLOG = 1
PRODUCTION = 2

API_URLS = {
    SANDBOX: "https://api-sandbox.getnet.com.br",
    HOMOLOG: "https://api-homologacao.getnet.com.br",
    PRODUCTION: "https://api.getnet.com.br",
}


class API:
    client_id: str = None
    client_secret: str = None
    access_token: str = None

    def __init__(self, client_id: str, client_secret: str, environment: int = SANDBOX):
        self.client_id = client_id
        self.client_secret = client_secret

        self.base_url = API_URLS[environment]

        self.request = requests.Session()

    def get(self, path, **kwargs):
        url = self.base_url + path
        response = self.request.get(url, **kwargs)
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def post(self, path: str, data: dict, **kwargs):
        url = self.base_url + path
        response = self.request.post(url, data=data, **kwargs)
        if not response.ok:
            response.raise_for_status()
        return response.json()

    def put(self, path: str, data: dict, **kwargs):
        url = self.base_url + path
        response = self.request.put(url, data, **kwargs)
        if not response.ok:
            response.raise_for_status()
        return response.json()

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
