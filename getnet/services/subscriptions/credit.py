from typing import Union

from getnet.services.customers import Address
from getnet.services.payments.credit import Credit as BaseCredit


class Credit(BaseCredit):
    billing_address: Address

    def __init__(self, billing_address: Union[Address, dict] = None, **kwargs):
        self.billing_address = (
            billing_address
            if isinstance(billing_address, Address) or billing_address is None
            else Address(**billing_address)
        )
        super(Credit, self).__init__(**kwargs)

    def as_dict(self):
        data = {
            "transaction_type": self.transaction_type,
            "number_installments": self.number_installments,
            "card": self.card._as_dict(),
        }

        if self.billing_address is not None:
            data["billing_address"] = self.billing_address.as_dict()

        if self.soft_descriptor is not None:
            data["soft_descriptor"] = self.soft_descriptor

        return data
