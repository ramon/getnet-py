import uuid
from datetime import datetime
from typing import Union

from getnet.services.cards.card import Card


class CardResponse(Card):
    card_id: uuid.UUID
    last_four_digits: str
    used_at: datetime
    created_at: datetime
    updated_at: datetime
    status: str

    def __init__(self,
                 card_id: Union[uuid.UUID, str],
                 last_four_digits: str = None,
                 used_at: datetime = None,
                 created_at: datetime = None,
                 updated_at: datetime = None,
                 status: str = None,
                 **kwargs):
        self.card_id = (
            card_id
            if isinstance(card_id, uuid.UUID)
            else uuid.UUID(card_id)
        )
        self.last_four_digits = last_four_digits
        self.used_at = datetime.strptime(used_at, '%Y-%m-%dT%H:%M:%S%z') if used_at else None
        self.created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z') if created_at else None
        self.updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S%z') if updated_at else None
        self.status = status

        super(CardResponse, self).__init__(**kwargs)

    def as_dict(self):
        data = super(CardResponse, self).as_dict()
        data['used_at'] = self.used_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        data['created_at'] = self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        data['updated_at'] = self.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        return data
