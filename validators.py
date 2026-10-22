"""Validate membership plan, extras, and member count."""

from memberships import PLANS, EXTRAS


def validate_selection(plan, extras, members):
    """Return True when the membership selection is valid."""
    valid = True

    if isinstance(plan, str) is False:
        valid = False
    elif plan not in PLANS:
        valid = False

    if isinstance(extras, (list, tuple)) is False:
        valid = False
    else:
        for extra in extras:
            if isinstance(extra, str) is False:
                valid = False
                break
            if extra not in EXTRAS:
                valid = False
                break
            if EXTRAS[extra]["premium"] is True and plan != "PREMIUM":
                valid = False
                break

    if isinstance(members, int) is False or isinstance(members, bool) is True:
        valid = False
    elif members < 1:
        valid = False

    return valid
