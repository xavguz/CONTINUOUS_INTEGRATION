from gym import CotizadorGym


def test_cotizador_inicial():
    cotizador = CotizadorGym()
    assert cotizador.esta_servidor_listo() is True