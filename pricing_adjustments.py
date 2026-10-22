"""Apply R4-R6 pricing adjustments without intermediate currency rounding.

Decimal operations use the caller's active context precision. Final currency
rounding belongs to R7, after all three adjustments have been applied in order.
"""

from decimal import Decimal


def apply_group_discount(subtotal: Decimal, members: int) -> Decimal:
    """Apply the R4 ten-percent discount for two or more members."""
    if members >= 2:
        return subtotal * Decimal("0.90")
    return subtotal


def apply_special_offer(amount: Decimal) -> Decimal:
    """Apply only the highest eligible R5 offer to the post-R4 amount."""
    if amount > Decimal("400"):
        return amount - Decimal("50")
    if amount > Decimal("200"):
        return amount - Decimal("20")
    return amount


def apply_premium_surcharge(amount: Decimal, has_premium_extra: bool) -> Decimal:
    """Apply the R6 fifteen-percent surcharge to the post-R5 amount."""
    if has_premium_extra:
        return amount * Decimal("1.15")
    return amount
