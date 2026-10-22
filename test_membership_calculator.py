
"""Unit tests for gym membership quote calculations."""

from decimal import Decimal

from membership_calculator import calculate_quote
from validators import validate_selection


# R1: Plans
def test_valid_plans():
    """Accept all three membership plans."""
    assert validate_selection("BASIC", [], 1) is True
    assert validate_selection("STANDARD", [], 1) is True
    assert validate_selection("PREMIUM", [], 1) is True


def test_invalid_plan():
    """Reject an invalid membership plan."""
    assert calculate_quote("GOLD", [], 1) == -1


# R2: Extras
def test_valid_extra():
    """Accept an extra allowed for the selected plan."""
    assert validate_selection("BASIC", ["GROUP_CLASSES"], 1) is True


def test_multiple_extras():
    """Calculate the subtotal for multiple extras."""
    quote = calculate_quote(
        "BASIC",
        ["GROUP_CLASSES", "PERSONAL_TRAINING"],
        1
    )

    assert quote["subtotal"] == Decimal("70")
    assert quote["total"] == 70


def test_unknown_extra():
    """Reject an extra that does not exist."""
    assert calculate_quote("BASIC", ["POOL"], 1) == -1


def test_premium_extra_rejected_for_basic():
    """Reject premium extras for the Basic plan."""
    assert calculate_quote("BASIC", ["SPA"], 1) == -1


def test_premium_extra_rejected_for_standard():
    """Reject premium extras for the Standard plan."""
    assert calculate_quote(
        "STANDARD", ["SPECIALIZED_PROGRAM"], 1
    ) == -1


def test_premium_extra_allowed_for_premium():
    """Accept premium extras for the Premium plan."""
    assert validate_selection(
        "PREMIUM", ["SPA"], 1
    ) is True


# R3: Subtotal
def test_subtotal():
    """Calculate the subtotal using the plan and extra prices."""
    quote = calculate_quote("BASIC", ["GROUP_CLASSES"], 1)

    assert quote["subtotal"] == Decimal("45")


def test_no_extras():
    """Calculate the subtotal when no extras are selected."""
    quote = calculate_quote("BASIC", [], 1)

    assert quote["subtotal"] == Decimal("30")
    assert quote["total"] == 30


def test_zero_members():
    """Reject a membership quote for zero members."""
    assert calculate_quote("BASIC", [], 0) == -1


def test_negative_members():
    """Reject a membership quote for negative members."""
    assert calculate_quote("BASIC", [], -1) == -1


# R4: Group discount integration
def test_group_discount_in_quote():
    """Apply the group discount for two members."""
    quote = calculate_quote("BASIC", [], 2)

    assert quote["subtotal"] == Decimal("60")
    assert quote["group_discount"] == Decimal("6")
    assert quote["total"] == 54


def test_no_group_discount_for_one_member():
    """Do not apply the group discount for one member."""
    quote = calculate_quote("BASIC", [], 1)

    assert quote["group_discount"] == Decimal("0")


# R5: Special offer integration
def test_twenty_dollar_offer_in_quote():
    """Apply the twenty-dollar offer after the group discount."""
    quote = calculate_quote("STANDARD", [], 5)

    assert quote["subtotal"] == Decimal("225")
    assert quote["group_discount"] == Decimal("22.50")
    assert quote["special_offer"] == Decimal("20")
    assert quote["total"] == 183


def test_fifty_dollar_offer_in_quote():
    """Apply the fifty-dollar offer when the amount exceeds 400."""
    quote = calculate_quote("PREMIUM", [], 7)

    assert quote["subtotal"] == Decimal("490")
    assert quote["group_discount"] == Decimal("49.00")
    assert quote["special_offer"] == Decimal("50")
    assert quote["total"] == 391


def test_no_special_offer_in_quote():
    """Do not apply a special offer when the amount is too low."""
    quote = calculate_quote("BASIC", [], 1)

    assert quote["special_offer"] == Decimal("0")


# R6: Premium surcharge integration
def test_premium_surcharge_in_quote():
    """Apply the premium surcharge when a premium extra is selected."""
    quote = calculate_quote("PREMIUM", ["SPA"], 1)

    assert quote["subtotal"] == Decimal("100")
    assert quote["special_offer"] == Decimal("0")
    assert quote["surcharge"] == Decimal("15")
    assert quote["total"] == 115


def test_no_premium_surcharge_in_quote():
    """Do not apply the surcharge when no premium extra is selected."""
    quote = calculate_quote("BASIC", ["GROUP_CLASSES"], 1)

    assert quote["surcharge"] == Decimal("0")


# R7: Final rounding
def test_round_half_up():
    """Round a final amount ending in 0.50 up to the next integer."""
    quote = calculate_quote("PREMIUM", ["SPECIALIZED_PROGRAM"], 1)

    # Subtotal: 110
    # Special offer: 0 (amount is not over 200)
    # Amount before surcharge: 110
    # Surcharge: 16.50
    # Final amount: 126.50, rounded half up to 127

    assert quote["subtotal"] == Decimal("110")
    assert quote["special_offer"] == Decimal("0")
    assert quote["surcharge"] == Decimal("16.50")
    assert quote["total"] == 127


def test_invalid_selection_returns_minus_one():
    """Return -1 when the membership selection is invalid."""
    assert calculate_quote("INVALID", [], 1) == -1


# R8: Return a complete quote breakdown
def test_quote_contains_all_required_fields():
    """Return all required quote breakdown fields."""
    quote = calculate_quote("BASIC", [], 1)

    assert isinstance(quote, dict)
    assert "subtotal" in quote
    assert "group_discount" in quote
    assert "special_offer" in quote
    assert "surcharge" in quote
    assert "total" in quote


def test_calculator_does_not_return_none():
    """Return a quote dictionary for a valid selection."""
    quote = calculate_quote("BASIC", [], 1)

    assert quote is not None
    assert quote["total"] == 30


# R9: Complete quote with multiple members and extras
def test_complete_quote():
    """Calculate a complete quote with members and multiple extras."""
    quote = calculate_quote(
        "PREMIUM",
        ["SPA", "GROUP_CLASSES"],
        2
    )

    # Subtotal: (70 + 30 + 15) * 2 = 230
    # Group discount: 23
    # After group discount: 207
    # Special offer: 20
    # After special offer: 187
    # Premium surcharge: 28.05
    # Final amount: 215.05, rounded to 215

    assert quote["subtotal"] == Decimal("230")
    assert quote["group_discount"] == Decimal("23.00")
    assert quote["special_offer"] == Decimal("20")
    assert quote["surcharge"] == Decimal("28.05")
    assert quote["total"] == 215
