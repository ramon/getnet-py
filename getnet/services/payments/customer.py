from getnet.services.customers import Customer as BaseCustomer


class Customer(BaseCustomer):
    def as_dict(self):
        data = super(Customer, self).as_dict()
        data.pop("seller_id")
        data.pop("birth_date")
        data.pop("celphone_number")
        data.pop("observation")
        data["name"] = self.full_name
        data["billing_address"] = data.pop("address")
        return data
