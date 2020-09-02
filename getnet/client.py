import logging
from datetime import datetime, timedelta
from typing import Union

import requests

from getnet.environment import Environment
from getnet.services import token
from getnet.services.token.card_token import CardToken
from getnet.utils import handler_request, handler_request_exception

__all__ = ["Client"]

LOGGER = logging.getLogger(__name__)


class Client(object):
    """Return an SDK client"""
    request: requests.Session
    seller_id: str = None
    client_id: str = None
    client_secret: str = None
    environment: Environment = Environment.SANDBOX
    access_token: str = None
    access_token_expires: int = None

    def __init__(
        self,
        seller_id: str,
        client_id: str,
        client_secret: str,
        environment: Environment = Environment.SANDBOX,
    ):
        """
        Args:
            seller_id (str):
            client_id (str):
            client_secret (str):
            environment (Environment):
        """
        self.seller_id = seller_id
        self.client_id = client_id
        self.client_secret = client_secret

        if not isinstance(environment, Environment):
            raise AttributeError('Invalid environment')

        self.environment = environment
        self.base_url = environment.base_url()

        self._setup_client()

    def _setup_client(self):
        self.request = requests.Session()
        self.request.headers.update(
            {"user-agent": "getnet-py/1.1", "seller_id": self.seller_id}
        )
        self.auth()

    def _handler_request(self):
        return handler_request(self)

    def access_token_expired(self):
        """Returns true if have a expired token

        Returns:
            bool
        """
        return (
            self.access_token is not None
            and self.access_token_expires < datetime.timestamp(datetime.now())
        )

    def auth(self) -> None:
        if not self.access_token or self.access_token_expired():
            path = "/auth/oauth/v2/token"
            data = {"scope": "oob", "grant_type": "client_credentials"}

            response = self.request.post(
                self.base_url + path,
                data=data,
                auth=(self.client_id, self.client_secret),
            )
            if not response.ok:
                raise handler_request_exception(response)

            response_data = response.json()

            self.access_token = response_data.get("access_token")
            self.access_token_expires = int(
                datetime.timestamp(
                    datetime.now() + timedelta(seconds=response_data.get("expires_in"))
                )
            )
            self.request.headers.update(
                {"Authorization": "Bearer {}".format(self.access_token)}
            )

    def get(self, path, **kwargs) -> dict:
        """
        Args:
            path:
            **kwargs:
        """
        with handler_request(self, LOGGER):
            url = self.base_url + path
            response = self.request.get(url, **kwargs)
            if not response.ok:
                raise handler_request_exception(response)
            return response.json()

    def post(self, path: str, **kwargs) -> dict:
        """
        Args:
            path (str):
            **kwargs:
        """
        with handler_request(self, LOGGER):
            url = self.base_url + path
            response = self.request.post(url, **kwargs)
            if not response.ok:
                raise handler_request_exception(response)
            return response.json()

    def patch(self, path: str, **kwargs) -> dict:
        """
        Args:
            path (str):
            **kwargs:
        """
        with handler_request(self, LOGGER):
            url = self.base_url + path
            response = self.request.patch(url, **kwargs)
            if not response.ok:
                raise handler_request_exception(response)
            return response.json()

    def delete(self, path: str, **kwargs) -> Union[bool, dict]:
        """
        Args:
            path (str):
            **kwargs:
        """
        with handler_request(self, LOGGER):
            url = self.base_url + path
            response = self.request.delete(url, **kwargs)
            if not response.ok:
                raise handler_request_exception(response)

            return True

    def token_service(self) -> token.Service:
        """Return a instance of token service"""
        return token.Service(self)

    def generate_token_card(self, card_number: str, customer_id: str) -> CardToken:
        """Shortcut to card token generation

        Args:
            card_number (str): credit card number
            customer_id (str): Customer identify

        Raises:
            * AttributeError, RequestError
        """
        return self.token_service().generate(token.CardNumber(card_number, customer_id))
