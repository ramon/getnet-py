import re

from getnet.services.base import ServiceBase, ResponseList
from getnet.services.customers.customer import Customer
from getnet.services.customers.customer_response import CustomerResponse

DOCUMENT_TYPES = ("CPF", "CNPJ")
DOCUMENT_NUMBER_REGEX = re.compile(r"\A\d{11,15}\Z")


class Service(ServiceBase):
    path = "/v1/customers/{customer_id}"

    def create(self, customer: Customer) -> Customer:
        customer.seller_id = self._client.seller_id

        response = self._post(self._format_url(), json=customer.as_dict())
        return CustomerResponse(**response)

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
    ) -> ResponseList:
        if page <= 0:
            raise TypeError("page must be greater then 0")

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

        values = [
            CustomerResponse(**customer) for customer in response.get("customers")
        ]

        return ResponseList(
            values, response.get("page"), response.get("limit"), response.get("total")
        )

    def get(self, customer_id: str):
        response = self._get(self._format_url(customer_id=customer_id))

        return CustomerResponse(**response)
