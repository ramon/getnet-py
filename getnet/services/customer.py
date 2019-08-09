import re
from typing import Union

from .base import ServiceBase

DOCUMENT_TYPES = ("CPF", "CNPJ")
DOCUMENT_NUMBER_REGEX = re.compile(r"\A\d{11,15}\Z")


class CustomerAddress:
    street: str
    number: str
    complement: str
    district: str
    city: str
    state: str
    country: str
    postal_code: str

    def __init__(
        self,
        street: str,
        number: str,
        complement: str,
        district: str,
        city: str,
        state: str,
        country: str,
        postal_code: str,
    ):
        self.street = street
        self.number = number
        self.complement = complement
        self.district = district
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code

    def toJSON(self):
        return vars(self)


class Customer:
    seller_id: str
    customer_id: str
    first_name: str
    last_name: str
    document_type: str
    document_number: str
    birth_date: str
    phone_number: str
    celphone_number: str
    email: str
    observation: str
    address: CustomerAddress

    def __init__(
        self,
        first_name: str,
        last_name: str,
        document_type: str,
        document_number: str,
        birth_date: str = None,
        phone_number: str = None,
        celphone_number: str = None,
        email: str = None,
        observation: str = None,
        customer_id: str = None,
        seller_id: str = None,
        address: Union[CustomerAddress, dict] = None,
    ):
        if not document_type in DOCUMENT_TYPES:
            raise AttributeError(
                "Document Type invalid. Choices {}".format(", ".join(DOCUMENT_TYPES))
            )

        if not DOCUMENT_NUMBER_REGEX.match(document_number):
            raise AttributeError(
                "Document Number invalid, Only digits and between 11 and 15 characters"
            )

        self.seller_id = seller_id
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.document_type = document_type
        self.document_number = document_number
        self.birth_date = birth_date
        self.phone_number = phone_number
        self.celphone_number = celphone_number
        self.email = email
        self.observation = observation

        if isinstance(address, dict):
            address = CustomerAddress(**address)

        self.address = address

    def __str__(self):
        return "{} ({})".format(self.full_name, self.customer_id)

    def __eq__(self, other):
        return (self.seller_id, self.customer_id) == (
            other.seller_id,
            other.customer_id,
        )

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def toJSON(self):
        data = vars(self).copy()
        data.popitem()
        data["address"] = self.address.toJSON()
        return data


class CustomerList(list):
    def __init__(self, seq=(), page=1, limit=100, total=None):
        self.page = page
        self.limit = limit
        self.total = total
        super(CustomerList, self).__init__(seq)


class CustomerService(ServiceBase):
    path = "/v1/customers/{customer_id}"

    def create(self, customer: Customer) -> Customer:
        response = self._post(self._format_url(), json=customer.toJSON())

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

        values = [Customer(**customer) for customer in response.get("customers")]

        return CustomerList(
            values, response.get("page"), response.get("limit"), response.get("total")
        )

    def get(self, customer_id: str):
        response = self._get(self._format_url(customer_id=customer_id))

        return Customer(**response)
