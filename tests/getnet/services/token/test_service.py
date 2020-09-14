import unittest
from unittest.mock import patch

import pytest
from pytest_mock import MockFixture

from getnet.services.token import Service, CardNumber
from getnet.services.token.card_token import CardToken


@pytest.fixture
def client(mocker: MockFixture):
    return mocker.patch("getnet.Client")

@pytest.fixture
def card_number():
    return CardNumber("5155901222280001", "customer_21081826")


def test_token_generate(client, card_number):
    client.post.return_value = {"number_token": "123456789"}

    service = Service(client)
    token = service.generate(card_number)

    assert isinstance(token, CardToken)
    assert "123456789" == token.number_token

