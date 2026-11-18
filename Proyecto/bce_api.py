import xml.etree.ElementTree as ET

import requests


URL_BCE = (
    "https://www.ecb.europa.eu/stats/eurofxref/"
    "eurofxref-daily.xml"
)

ESPACIOS_NOMBRES = {
    "ecb": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"
}


class ErrorBCE(RuntimeError):
    """Error producido al descargar o procesar los datos del BCE."""


def descargar_xml() -> str:
    """
    Descarga el XML diario de tipos de cambio del BCE.

    Returns:
        El XML recibido en formato de texto.

    Raises:
        ErrorBCE: Si no se puede conectar con el BCE.
    """
    try:
        respuesta = requests.get(
            URL_BCE,
            timeout=10,
            headers={"User-Agent": "ConversorDivisas/1.0"},
        )
        respuesta.raise_for_status()
    except requests.RequestException as error:
        raise ErrorBCE(
            "No se han podido descargar los tipos de cambio del BCE."
        ) from error

    respuesta.encoding = "utf-8"
    return respuesta.text


def procesar_xml(xml: str) -> tuple[str, dict[str, float]]:
    """
    Extrae la fecha y las tasas de cambio del XML.

    El BCE indica cuántas unidades de cada moneda equivalen a un euro.

    Args:
        xml: Documento XML recibido del BCE.

    Returns:
        Una tupla con la fecha y el diccionario de tasas.

    Raises:
        ErrorBCE: Si el XML no tiene el formato esperado.
    """
    try:
        raiz = ET.fromstring(xml)
    except ET.ParseError as error:
        raise ErrorBCE("El XML recibido no es válido.") from error

    cubo_fecha = raiz.find(
        ".//ecb:Cube[@time]",
        ESPACIOS_NOMBRES,
    )

    if cubo_fecha is None:
        raise ErrorBCE(
            "No se ha encontrado la fecha de los tipos de cambio."
        )

    fecha = cubo_fecha.get("time")

    if fecha is None:
        raise ErrorBCE("La fecha del XML está vacía.")

    # El euro no aparece en el XML porque es la moneda base.
    tasas: dict[str, float] = {"EUR": 1.0}

    for elemento in cubo_fecha.findall("ecb:Cube", ESPACIOS_NOMBRES):
        moneda = elemento.get("currency")
        valor_tasa = elemento.get("rate")

        if moneda is None or valor_tasa is None:
            continue

        try:
            tasas[moneda] = float(valor_tasa)
        except ValueError as error:
            raise ErrorBCE(
                f"La tasa de la moneda {moneda} no es válida."
            ) from error

    if len(tasas) == 1:
        raise ErrorBCE(
            "No se han encontrado monedas en el XML recibido."
        )

    return fecha, tasas


def obtener_datos() -> tuple[str, dict[str, float], str]:
    """
    Descarga y procesa todos los datos necesarios para la aplicación.

    Returns:
        Fecha, diccionario de tasas y XML original.
    """
    xml = descargar_xml()
    fecha, tasas = procesar_xml(xml)

    return fecha, tasas, xml