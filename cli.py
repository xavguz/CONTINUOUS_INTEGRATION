"""Interfaz de línea de comandos para el cotizador de membresías."""

from membership_calculator import calculate_quote
from memberships import PLANS, EXTRAS


def read_plan():
    """Leer y validar el plan seleccionado."""
    while True:
        plan = input("Plan (BASIC/STANDARD/PREMIUM): ").strip().upper()

        if plan in PLANS:
            return plan

        print("Plan inválido. Escriba BASIC, STANDARD o PREMIUM.")


def read_extras(plan):
    """Leer y normalizar los extras separados por coma según el plan."""
    allowed_extras = []

    for extra_name, extra_info in EXTRAS.items():
        if extra_info["premium"] and plan != "PREMIUM":
            continue
        allowed_extras.append(extra_name)

    if allowed_extras:
        extras_list = ", ".join(allowed_extras)
    else:
        extras_list = "ninguno"

    raw = input(
        f"Extras separados por coma ({extras_list}, Enter para ninguno): "
    ).strip()

    if not raw:
        return []

    return [
        extra.strip().upper()
        for extra in raw.split(",")
        if extra.strip()
    ]


def read_members():
    """Leer la cantidad de miembros como entero."""
    raw = input("Número de miembros: ").strip()

    try:
        return int(raw)
    except ValueError:
        return -1


def _format_amount(value):
    """Formatear un monto con dos decimales."""
    return f"{value:.2f}"


def show_quote(quote):
    """Mostrar el desglose completo de la cotización."""
    print(f"Subtotal: {_format_amount(quote['subtotal'])}")
    print(f"Descuento por grupo: {_format_amount(quote['group_discount'])}")
    print(f"Oferta especial: {_format_amount(quote['special_offer'])}")
    print(f"Recargo premium: {_format_amount(quote['surcharge'])}")
    print(f"Total: {quote['total']}")


def confirm():
    """Preguntar si se confirma la cotización (y/n)."""
    while True:
        answer = input("¿Confirmar cotización? (y/n): ").strip().lower()

        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Respuesta inválida. Escriba 'y' o 'n'.")


def run_cli():
    """Ejecutar el flujo del CLI y devolver el total o -1."""
    plan = read_plan()
    extras = read_extras(plan)
    members = read_members()

    quote = calculate_quote(plan, extras, members)

    if quote == -1:
        print("Selección inválida.")
        return -1

    show_quote(quote)

    if confirm() is False:
        return -1

    return quote["total"]
