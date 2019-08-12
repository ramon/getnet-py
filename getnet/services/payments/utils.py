__all__ = ("Order", "Payment")


class Order:
    PRODUCT_TYPES = (
        "cash_carry",
        "digital_content",
        "digital_goods",
        "digital_physical",
        "gift_card",
        "physical_goods",
        "renew_subs",
        "shareware",
        "service",
    )

    order_id: str
    sales_tax: int
    product_type: str

    def __init__(self, order_id: str, sales_tax: int, product_type: str):
        if len(order_id) > 36:
            raise AttributeError("The order_id must have bellow of 32 characters")

        if not product_type in self.PRODUCT_TYPES:
            raise AttributeError("The product_type is invalid")

        self.order_id = order_id
        self.sales_tax = sales_tax
        self.product_type = product_type

    def toJSON(self):
        return {
            "order_id": self.order_id,
            "sales_tax": self.sales_tax,
            "product_type": self.product_type,
        }


class Payment:
    payment_id: str
    seller_id: str
    amount: int
    currency: str
    order_id: str
    status: str
    boleto: object = None
    credit: object = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
