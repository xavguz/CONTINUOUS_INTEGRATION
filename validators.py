from memberships import PLANS, EXTRAS

"""Validate gym membership plan, extras, and member count."""


def validate_selection(plan, extras, members):
    """Return True for a valid selection and False otherwise."""
    # Keep your existing validation logic here,
    # applying the replacements listed above.

    if isinstance(plan, str) == False or plan not in PLANS:
        return False

    if isinstance(extras, (list, tuple)) == False:
        return False

    for extra in extras:
        if isinstance(extra, str) == False or extra not in EXTRAS:
            return False

    if type(members) != int or members < 1:
        return False

    if plan != "PREMIUM":
        for extra in extras:
            if EXTRAS[extra]["premium"] == True:
                return False

    return True