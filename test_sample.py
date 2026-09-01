from app import sample

def test_ruta_principal():
    cliente = sample.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200 # nosec B101
