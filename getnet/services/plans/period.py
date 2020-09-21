"""
Implements Plan Period
"""
from enum import Enum, unique
from typing import Union


@unique
class PeriodType(Enum):
    """PeriodType is the enum with Plan Period options"""

    YEARLY = "yearly"
    MONTHLY = "monthly"
    BIMONTHLY = "bimonthly"
    QUARTERLY = "quarterly"
    SEMESTERLY = "semesterly"
    SPECIFIC = "specific"


class Period:
    """Period represents the Plan Period entity"""

    type: PeriodType
    billing_cycle: int
    specific_cycle_in_days: int

    def __init__(
        self,
        type: Union[PeriodType, str],
        billing_cycle: int,
        specific_cycle_in_days: int = None,
    ):

        """
        Args:
            type: (PeriodType)
            billing_cycle (int):
            specific_cycle_in_days (int):
        """
        if isinstance(type, str):
            try:
                type = PeriodType[type.upper()]
            except Exception:
                raise AttributeError("Invalid Type")

        if type == PeriodType.SPECIFIC and specific_cycle_in_days is None:
            raise AttributeError(
                "'specific_cycle_in_days' required if type is specific"
            )

        self.type = type
        self.billing_cycle = billing_cycle
        self.specific_cycle_in_days = specific_cycle_in_days

    def as_dict(self):
        """Format the data as dict to be sent to Getnet"""
        data = self.__dict__.copy()
        data["type"] = self.type.value
        data.pop("specific_cycle_in_days")

        if self.type == PeriodType.SPECIFIC:
            data["specific_cycle_in_days"] = self.specific_cycle_in_days

        return data
