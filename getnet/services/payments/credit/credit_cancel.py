from typing import Union

from datetime import datetime

from dateutil import parser

from getnet.services.payments.credit.card import Card


class CreditCancel:
    canceled_at: datetime
    message: str

    def __init__(self, canceled_at: datetime, message: str):

        self.canceled_at = (
            canceled_at
            if isinstance(canceled_at, datetime)
            else parser.isoparse(canceled_at)
        )
        self.message = message
