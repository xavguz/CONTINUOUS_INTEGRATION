"""Check independent R4-R6 rules and their unrounded calculation sequence."""

from decimal import Decimal

import pytest

from pricing_adjustments import (
    apply_group_discount,
    apply_premium_surcharge,
    apply_special_offer,
)


@pytest.mark.parametrize(
    "subtotal,members,expected",
    [
        ("100", 1, "100"),
        ("100", 2, "90"),
        ("100", 3, "90"),
        ("249.99", 2, "224.991"),
        ("444.445", 2, "400.0005"),
    ],
)
def test_group_discount(subtotal, members, expected):
    """Group size controls eligibility, not the discount percentage."""
    result = apply_group_discount(Decimal(subtotal), members)
    assert isinstance(result, Decimal)
    assert result == Decimal(expected)


@pytest.mark.parametrize(
    "amount,expected",
    [
        ("199.9999", "199.9999"),
        ("200", "200"),
        ("200.0001", "180.0001"),
        ("201", "181"),
        ("399.9999", "379.9999"),
        ("400", "380"),
        ("400.0001", "350.0001"),
        ("401", "351"),
        ("1000", "950"),
    ],
)
def test_special_offer(amount, expected):
    """Thresholds are strict and the two offers never stack."""
    result = apply_special_offer(Decimal(amount))
    assert isinstance(result, Decimal)
    assert result == Decimal(expected)


@pytest.mark.parametrize(
    "amount,has_premium_extra,expected",
    [
        ("100", False, "100"),
        ("100", True, "115"),
        ("351", True, "403.65"),
        ("204.991", True, "235.73965"),
        ("350.0005", False, "350.0005"),
    ],
)
def test_premium_surcharge(amount, has_premium_extra, expected):
    """The surcharge preserves fractional cents until final R7 rounding."""
    result = apply_premium_surcharge(Decimal(amount), has_premium_extra)
    assert isinstance(result, Decimal)
    assert result == Decimal(expected)


@pytest.mark.parametrize(
    "subtotal,members,has_premium_extra,expected_stages",
    [
        ("444.445", 2, True, ("400.0005", "350.0005", "402.500575")),
        ("249.99", 2, True, ("224.991", "204.991", "235.73965")),
        ("401", 1, True, ("401", "351", "403.65")),
        ("400", 1, False, ("400", "380", "380")),
    ],
)
def test_adjustments_in_order(
    subtotal, members, has_premium_extra, expected_stages
):
    """R4 then R5 then R6 must not round across offer thresholds."""
    after_group = apply_group_discount(Decimal(subtotal), members)
    after_offer = apply_special_offer(after_group)
    result = apply_premium_surcharge(after_offer, has_premium_extra)

    assert isinstance(after_group, Decimal)
    assert isinstance(after_offer, Decimal)
    assert isinstance(result, Decimal)
    assert (after_group, after_offer, result) == tuple(
        Decimal(value) for value in expected_stages
    )
