PERIOD_TYPES = (
    "yearly",
    "monthly",
    "bimonthly",
    "quarterly",
    "semesterly",
    "specific"
)

class Period:
    type: str
    billing_cycle: int
    specific_cycle_in_days: int

    def __init__(
        self,
        type: str,
        billing_cycle: int,
        specific_cycle_in_days: int = None
    ):
        if type not in PERIOD_TYPES:
            raise TypeError('Invalid Type')

        if type == 'specific' and specific_cycle_in_days is None:
            raise TypeError("'specific_cycle_in_days' required is type is specific")

        self.type = type
        self.billing_cycle = billing_cycle
        self.specific_cycle_in_days = specific_cycle_in_days

    def as_dict(self):
        data = self.__dict__.copy()
        data.pop('specific_cycle_in_days')

        if self.type == 'specific':
            data['specific_cycle_in_days'] = self.specific_cycle_in_days

        return data
