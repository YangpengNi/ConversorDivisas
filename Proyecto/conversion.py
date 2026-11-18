from collections.abc import Mapping


class ErrorConversion(ValueError):
    """Error producido al intentar realizar una conversión."""


def convertir(
    cantidad: float,
    moneda_origen: str,
    moneda_destino: str,
    tasas: Mapping[str, float],
) -> float:
    """
    Convierte una cantidad usando el euro como moneda puente.
    """
    if cantidad < 0:
        raise ErrorConversion(
            "La cantidad no puede ser negativa."
        )

    if moneda_origen not in tasas:
        raise ErrorConversion(
            f"No existe la tasa para {moneda_origen}."
        )

    if moneda_destino not in tasas:
        raise ErrorConversion(
            f"No existe la tasa para {moneda_destino}."
        )

    tasa_origen = tasas[moneda_origen]
    tasa_destino = tasas[moneda_destino]

    if tasa_origen <= 0 or tasa_destino <= 0:
        raise ErrorConversion(
            "Las tasas deben ser mayores que cero."
        )

    cantidad_en_euros = cantidad / tasa_origen
    resultado = cantidad_en_euros * tasa_destino

    return resultado