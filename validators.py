from memberships import PLANS, EXTRAS

def validate_selection(plan, extras, members):
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