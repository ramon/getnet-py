import pytest

from getnet.services.plans import Period


def test_invalid_type():
    with pytest.raises(AttributeError):
        Period("Invalid", 1)


def test_require_specific_cycle_if_type_is_specific():
    with pytest.raises(AttributeError):
        Period("specific", 1)
