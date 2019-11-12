from datetime import date, datetime
from typing import Union, List

from getnet.services.payments.boleto.boleto import Boleto
from getnet.services.payments.payment_response import PaymentResponse


class BoletoResponse(Boleto):
    boleto_id: str
    bank: int
    issue_date: date
    status_code: int
    status_label: str
    typeful_line: str
    bar_code: str
    links: dict = {}

    def __init__(
        self,
        boleto_id: str = None,
        bank: int = None,
        issue_date: Union[date, str] = None,
        status_code: int = None,
        status_label: str = None,
        typeful_line: str = None,
        bar_code: str = None,
        _links: List[dict] = iter([]),
        _base_uri: str = "",
        **kwargs,
    ):
        super(BoletoResponse, self).__init__(**kwargs)
        self.boleto_id = boleto_id
        self.bank = bank
        self.issue_date = (
            datetime.strptime(issue_date, "%d/%m/%Y")
            if issue_date and not isinstance(issue_date, date)
            else issue_date
        )
        self.status_code = status_code
        self.status_label = status_label
        self.typeful_line = typeful_line
        self.bar_code = bar_code

        for link in _links:
            self.links[link.get("rel")] = "".join([_base_uri, link.get("href")])


class BoletoPaymentResponse(PaymentResponse):
    boleto: BoletoResponse = None

    def __init__(self, boleto: Union[BoletoResponse, dict], **kwargs):
        super(BoletoPaymentResponse, self).__init__(**kwargs)
        self.boleto = (
            boleto
            if isinstance(boleto, BoletoResponse) or boleto is None
            else BoletoResponse(**boleto)
        )
