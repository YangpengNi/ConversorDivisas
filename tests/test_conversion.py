import pytest

from Proyecto.conversion import ErrorConversion, convertir


TASAS_PRUEBA = {
    "EUR": 1.0,
    "USD": 1.2,
    "JPY": 180.0,
    "GBP": 0.8,
}


def test_convertir_euros_a_dolares():
    resultado = convertir(
        100,
        "EUR",
        "USD",
        TASAS_PRUEBA,
    )

    assert resultado == pytest.approx(120.0)


def test_conversion_cruzada_dolares_a_yenes():
    resultado = convertir(
        100,
        "USD",
        "JPY",
        TASAS_PRUEBA,
    )

    assert resultado == pytest.approx(15000.0)


def test_conversion_misma_moneda():
    resultado = convertir(
        50,
        "GBP",
        "GBP",
        TASAS_PRUEBA,
    )

    assert resultado == pytest.approx(50.0)


def test_cantidad_cero():
    resultado = convertir(
        0,
        "EUR",
        "USD",
        TASAS_PRUEBA,
    )

    assert resultado == pytest.approx(0.0)


def test_cantidad_negativa():
    with pytest.raises(
        ErrorConversion,
        match="La cantidad no puede ser negativa",
    ):
        convertir(
            -20,
            "EUR",
            "USD",
            TASAS_PRUEBA,
        )


def test_moneda_origen_inexistente():
    with pytest.raises(
        ErrorConversion,
        match="No existe la tasa para ABC",
    ):
        convertir(
            100,
            "ABC",
            "EUR",
            TASAS_PRUEBA,
        )


def test_moneda_destino_inexistente():
    with pytest.raises(
        ErrorConversion,
        match="No existe la tasa para XYZ",
    ):
        convertir(
            100,
            "EUR",
            "XYZ",
            TASAS_PRUEBA,
        )