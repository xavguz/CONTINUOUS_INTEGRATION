from decimal import Decimal
from membership_calculator import calculate_quote
from validators import validate_selection


# R1: Plans
def test_valid_plan():
    assert validate_selection("BASIC", [], 1) == True


def test_invalid_plan():
    assert calculate_quote("GOLD", [], 1) == -1


# R2: Extras
def test_valid_extra():
    assert validate_selection("BASIC", ["GROUP_CLASSES"], 1) == True


def test_unknown_extra():
    assert calculate_quote("BASIC", ["POOL"], 1) == -1


def test_premium_extra_rejected_for_basic():
    assert calculate_quote("BASIC", ["SPA"], 1) == -1


def test_premium_extra_allowed_for_premium():
    assert validate_selection("PREMIUM", ["SPA"], 1) == True


def test_multiple_extras():
    quote = calculate_quote(
        "BASIC",
        ["GROUP_CLASSES", "PERSONAL_TRAINING"],
        1
    )
    assert quote["subtotal"] == 70


# R3: Subtotal and members
def test_subtotal():
    quote = calculate_quote("BASIC", ["GROUP_CLASSES"], 1)
    assert quote["subtotal"] == 45


def test_zero_members():
    assert calculate_quote("BASIC", [], 0) == -1


def test_negative_members():
    assert calculate_quote("BASIC", [], -1) == -1
