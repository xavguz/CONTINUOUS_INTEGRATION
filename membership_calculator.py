from decimal import Decimal, ROUND_HALF_UP
from memberships import PLANS, EXTRAS
from validators import validate_selection
from pricing_adjustments import (
    apply_group_discount,
    apply_special_offer,
    apply_premium_surcharge
)

def calculate_quote(plan, extras, members):
    if validate_selection(plan, extras, members) == False:
        return -1

    # R3: Calculate subtotal
    plan_price = Decimal(str(PLANS[plan]))

    extras_price = sum(
        (Decimal(str(EXTRAS[extra]["price"])) for extra in extras),
        Decimal("0")
    )

    subtotal = (plan_price + extras_price) * members

    # R4: Apply group discount
    amount = apply_group_discount(subtotal, members)
    group_discount = subtotal - amount

    # R5: Apply special offer
    amount_after_group_discount = amount
    amount = apply_special_offer(amount)
    special_offer = amount_after_group_discount - amount

    # R6: Apply premium surcharge
    has_premium_extra = any(
        EXTRAS[extra]["premium"] == True
        for extra in extras
    )

    amount_before_surcharge = amount
    amount = apply_premium_surcharge(amount, has_premium_extra)
    surcharge = amount - amount_before_surcharge

    # R7: Round half up only at the end
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