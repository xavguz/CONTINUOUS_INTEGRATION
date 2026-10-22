from decimal import Decimal

import pytest

from membership_calculator import calculate_quote
from validators import validate_selection


# R1: Plans

def test_valid_plan():
    assert validate_selection("BASIC", [], 1) == True
    assert validate_selection("STANDARD", [], 1) == True
    assert validate_selection("PREMIUM", [], 1) == True


def test_invalid_plan():
    assert calculate_quote("GOLD", [], 1) == -1

# R2: Extras

def test_valid_extra():
    assert validate_selection(
        "BASIC", ["GROUP_CLASSES"], 1
    ) == True


def test_multiple_extras():
    quote = calculate_quote(
        "BASIC",
        ["GROUP_CLASSES", "PERSONAL_TRAINING"],
        1
    )

    assert quote["subtotal"] == Decimal("70")
    assert quote["total"] == 70


def test_unknown_extra():
    assert calculate_quote("BASIC", ["POOL"], 1) == -1


def test_premium_extra_rejected_for_basic():
    assert calculate_quote("BASIC", ["SPA"], 1) == -1


def test_premium_extra_rejected_for_standard():
    assert calculate_quote(
        "STANDARD", ["SPECIALIZED_PROGRAM"], 1
    ) == -1


def test_premium_extra_allowed_for_premium():
    assert validate_selection(
        "PREMIUM", ["SPA"], 1
    ) == True


# R3: Subtotal

def test_subtotal():
    quote = calculate_quote("BASIC", ["GROUP_CLASSES"], 1)

    assert quote["subtotal"] == Decimal("45")


def test_no_extras():
    quote = calculate_quote("BASIC", [], 1)

    assert quote["subtotal"] == Decimal("30")
    assert quote["total"] == 30


def test_zero_members():
    assert calculate_quote("BASIC", [], 0) == -1


def test_negative_members():
    assert calculate_quote("BASIC", [], -1) == -1


# R4: Group discount integration

def test_group_discount_in_quote():
    quote = calculate_quote("BASIC", [], 2)

    assert quote["subtotal"] == Decimal("60")
    assert quote["group_discount"] == Decimal("6")
    assert quote["total"] == 54


def test_no_group_discount_for_one_member():
    quote = calculate_quote("BASIC", [], 1)

    assert quote["group_discount"] == Decimal("0")


# R5: Special offer integration

def test_twenty_dollar_offer_in_quote():
    quote = calculate_quote("STANDARD", [], 5)

    assert quote["subtotal"] == Decimal("225")
    assert quote["group_discount"] == Decimal("22.50")
    assert quote["special_offer"] == Decimal("20")
    assert quote["total"] == 183


def test_fifty_dollar_offer_in_quote():
    quote = calculate_quote("PREMIUM", [], 7)

    assert quote["subtotal"] == Decimal("490")
    assert quote["group_discount"] == Decimal("49.00")
    assert quote["special_offer"] == Decimal("50")
    assert quote["total"] == 391


def test_no_special_offer_in_quote():
    quote = calculate_quote("BASIC", [], 1)

    assert quote["special_offer"] == Decimal("0")


# R6: Premium surcharge integration

def test_premium_surcharge_in_quote():
    quote = calculate_quote("PREMIUM", ["SPA"], 1)

    assert quote["subtotal"] == Decimal("100")
    assert quote["special_offer"] == Decimal("0")
    assert quote["surcharge"] == Decimal("15")
    assert quote["total"] == 115


def test_no_premium_surcharge_in_quote():
    quote = calculate_quote("BASIC", ["GROUP_CLASSES"], 1)

    assert quote["surcharge"] == Decimal("0")


# R7: Final rounding

def test_round_half_up():
    quote = calculate_quote("PREMIUM", ["SPECIALIZED_PROGRAM"], 1)

    # Subtotal: 110
    # Special offer: 0 (amount is not over 200)
    # Amount before surcharge: 110
    # Surcharge: 16.5
    # Final amount: 126.5, rounded half up to 127

    assert quote["subtotal"] == Decimal("110")
    assert quote["special_offer"] == Decimal("0")
    assert quote["surcharge"] == Decimal("16.50")
    assert quote["total"] == 127

def test_invalid_selection_returns_minus_one():
    assert calculate_quote("INVALID", [], 1) == -1


# R8: Return a complete quote breakdown

def test_quote_contains_all_required_fields():
    quote = calculate_quote("BASIC", [], 1)

    assert isinstance(quote, dict)
    assert "subtotal" in quote
    assert "group_discount" in quote
    assert "special_offer" in quote
    assert "surcharge" in quote
    assert "total" in quote


def test_calculator_does_not_return_none():
    quote = calculate_quote("BASIC", [], 1)

    assert quote is not None
    assert quote["total"] == 30


# R9: Complete quote with multiple members and extras

def test_complete_quote():
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