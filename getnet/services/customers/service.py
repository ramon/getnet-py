import re

from getnet.services.base import ServiceBase
from getnet.services.customers.customer import Customer

DOCUMENT_TYPES = ("CPF", "CNPJ")
DOCUMENT_NUMBER_REGEX = re.compile(r"\A\d{11,15}\Z")


class CustomerList(list):
    def __init__(self, seq=(), page=1, limit=100, total=None):
        self.page = page
        self.limit = limit
        self.total = total
        super(CustomerList, self).__init__(seq)


class Service(ServiceBase):
    path = "/v1/customers/{customer_id}"

    def create(self, customer: Customer) -> Customer:
        response = self._post(self._format_url(), json=customer.as_dict())
        return Customer(**response)

    def all(
        self,
        page: int = 1,
        limit: int = 100,
        customer_id: str = None,
        document_number: str = None,
        first_name: str = None,
        last_name: str = None,
        sort: str = "last_name",
        sort_type: str = "asc",
    ) -> CustomerList:
        if page <= 0:
            raise AttributeError("page must be greater then 0")

        if not sort_type in ("asc", "desc"):
            raise AttributeError("sort_type invalid. Choices: asc, desc")

        params = {
            "page": page,
            "limit": limit,
            "customer_id": customer_id,
            "document_number": document_number,
            "first_name": first_name,
            "last_name": last_name,
            "sort": sort,
            "sort_type": "asc",
        }

        response = self._get(self._format_url(), params=params)

        values = [Customer(**customer) for customer in response._get("customers")]

        return CustomerList(
            values, response._get("page"), response._get("limit"), response._get("total")
        )

    def _get(self, customer_id: str):
        response = self._get(self._format_url(customer_id=customer_id), headers={'seller_id': self._api.seller_id})

        return Customer(**response)
