"""Calculate gym membership quotes and apply pricing adjustments."""

from decimal import Decimal, ROUND_HALF_UP
from memberships import PLANS, EXTRAS
from validators import validate_selection
from pricing_adjustments import (
    apply_group_discount,
    apply_special_offer,
    apply_premium_surcharge
)


def calculate_quote(plan, extras, members):
    """Calculate the final quote, including discounts and surcharges."""
    if validate_selection(plan, extras, members) is False:
        return -1

    # R3: Calculate subtotal
    plan_price = Decimal(str(PLANS[plan]))

    extras_price = sum(
        (
            Decimal(str(EXTRAS[extra]["price"]))
            for extra in extras
        ),
        Decimal("0")
    )

    subtotal = (plan_price + extras_price) * members

    """Apply group discount"""
    amount = apply_group_discount(subtotal, members)
    group_discount = subtotal - amount

    """Apply special offer"""
    amount_before_offer = amount
    amount = apply_special_offer(amount)
    special_offer = amount_before_offer - amount

    """Apply premium surcharge"""
    has_premium_extra = any(
        EXTRAS[extra]["premium"] is True
        for extra in extras
    )

    amount_before_surcharge = amount
    amount = apply_premium_surcharge(
        amount,
        has_premium_extra
    )
    surcharge = amount - amount_before_surcharge

    """Round half up only at the end"""
    total = int(
        amount.quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP
        )
    )

    return {
        "subtotal": subtotal,
        "group_discount": group_discount,
        "special_offer": special_offer,
        "surcharge": surcharge,
        "total": total
    }