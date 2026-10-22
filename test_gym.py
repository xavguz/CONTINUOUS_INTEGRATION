"""Módulo de pruebas unitarias para el CotizadorGym."""

from gym import CotizadorGym


def test_esta_servidor_listo():
    """Verifica la respuesta correcta del estado del servidor."""
    cotizador = CotizadorGym()
    assert cotizador.esta_servidor_listo() is True