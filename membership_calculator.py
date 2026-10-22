from decimal import Decimal, ROUND_HALF_UP
from memberships import PLANS, EXTRAS
from validators import validate_selection


def calculate_quote(plan, extras, members):
    if validate_selection(plan, extras, members) == False:
        return -1

    plan_price = Decimal(str(PLANS[plan]))

    extras_price = sum(
        (Decimal(str(EXTRAS[extra]["price"])) for extra in extras),
        Decimal("0")
    )

    # R3: Calculate subtotal
    subtotal = (plan_price + extras_price) * members

