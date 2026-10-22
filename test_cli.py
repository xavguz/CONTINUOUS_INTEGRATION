"""Unit tests for CLI."""

from cli import read_extras, run_cli


def test_read_extras_basic(monkeypatch):
    """Extras mostrados para BASIC: solo no premium."""
    monkeypatch.setattr("builtins.input", lambda _: "GROUP_CLASSES")
    extras = read_extras("BASIC")
    assert extras == ["GROUP_CLASSES"]


def test_read_extras_standard(monkeypatch):
    """Extras mostrados para STANDARD: solo no premium."""
    monkeypatch.setattr("builtins.input", lambda _: "PERSONAL_TRAINING")
    extras = read_extras("STANDARD")
    assert extras == ["PERSONAL_TRAINING"]


def test_read_extras_premium(monkeypatch):
    """Extras mostrados para PREMIUM: pueden incluir premium."""
    monkeypatch.setattr("builtins.input", lambda _: "SPA")
    extras = read_extras("PREMIUM")
    assert extras == ["SPA"]


def test_read_extras_enter_returns_empty(monkeypatch):
    """Enter sin extras devuelve lista vacía."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    extras = read_extras("BASIC")
    assert extras == []


def test_read_extras_multiple(monkeypatch):
    """Extras múltiples separados por coma."""
    monkeypatch.setattr("builtins.input", lambda _: "GROUP_CLASSES, PERSONAL_TRAINING")
    extras = read_extras("STANDARD")
    assert extras == ["GROUP_CLASSES", "PERSONAL_TRAINING"]


def test_run_cli_confirm_yes(monkeypatch, capsys):
    """Si confirma con y, devuelve el total."""
    inputs = iter([
        "BASIC",        # plan
        "",             # extras
        "1",            # miembros
        "y"             # confirmación
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = run_cli()
    captured = capsys.readouterr()

    assert result == 30
    assert "Subtotal" in captured.out
    assert "Total: 30" in captured.out


def test_run_cli_confirm_no(monkeypatch, capsys):
    """Si confirma con n, devuelve -1."""
    inputs = iter([
        "BASIC",
        "",
        "1",
        "n"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = run_cli()
    captured = capsys.readouterr()

    assert result == -1
    assert "Subtotal" in captured.out


def test_run_cli_invalid_plan(monkeypatch, capsys):
    """Plan inválido seguido de uno válido."""
    inputs = iter([
        "GOLD",  # inválido
        "BASIC", # válido
        "",
        "1",
        "y"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = run_cli()
    captured = capsys.readouterr()

    assert result == 30
    assert "Plan inválido" in captured.out
    assert "Total: 30" in captured.out


def test_run_cli_invalid_selection_returns_minus_one(monkeypatch, capsys):
    """Selección inválida retorna -1."""
    inputs = iter([
        "BASIC",
        "SPA",  # premium no permitido para BASIC
        "1",
        "y"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = run_cli()
    captured = capsys.readouterr()

    assert result == -1
    assert "Selección inválida" in captured.out
