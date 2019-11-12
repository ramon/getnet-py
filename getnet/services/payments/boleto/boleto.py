from typing import Union

from datetime import date, datetime


class Boleto:
    our_number: str
    document_number: str
    expiration_date: date
    instructions: str
    provider: str

    def __init__(
        self,
        document_number: str,
        expiration_date: Union[date, str],
        our_number: str = None,
        instructions: str = None,
        provider: str = "santander",
    ) -> None:
        if len(document_number) > 15:
            raise TypeError("document_number is too long (max 15 characters)")

        if instructions is not None and len(instructions) > 1000:
            raise TypeError("instructions is too long (max: 1000 characters)")

        self.document_number = document_number
        self.expiration_date = (
            datetime.strptime(expiration_date, "%d/%m/%Y")
            if expiration_date and not isinstance(expiration_date, date)
            else expiration_date
        )
        self.instructions = instructions
        self.our_number = our_number
        self.provider = provider

    def as_dict(self):
        return {
            "our_number": self.our_number,
            "document_number": self.document_number,
            "expiration_date": self.expiration_date.strftime("%d/%m/%Y"),
            "instructions": self.instructions,
            "provider": self.provider,
        }
