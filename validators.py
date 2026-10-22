
"""Validate membership plan, extras, and member count."""

from memberships import PLANS, EXTRAS


def validate_selection(plan, extras, members):
    """Return True when the membership selection is valid."""
    if isinstance(plan, str) is False:
        return False

    if plan not in PLANS:
        return False

    if isinstance(extras, (list, tuple)) is False:
        return False

    for extra in extras:
        if isinstance(extra, str) is False:
            return False

        if extra not in EXTRAS:
            return False

        if EXTRAS[extra]["premium"] is True and plan != "PREMIUM":
            return False

    if isinstance(members, int) is False or isinstance(members, bool) is True:
        return False

    if members < 1:
        return False

    return True
