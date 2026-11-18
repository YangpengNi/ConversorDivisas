import streamlit as st

from bce_api import ErrorBCE, obtener_datos
from conversion import ErrorConversion, convertir


st.set_page_config(
    page_title="Conversor de Divisas",
    page_icon="💶",
    layout="centered",
)


@st.cache_data(ttl=3600, show_spinner=False)
def cargar_datos():
    """
    Descarga los datos del BCE y los guarda durante una hora.

    Esto evita descargar el XML cada vez que el usuario pulsa
    un botón o cambia un desplegable.
    """
    return obtener_datos()


st.title("💶 Conversor de Divisas (BCE)")

st.write(
    "Esta aplicación utiliza los tipos de cambio publicados "
    "por el Banco Central Europeo."
)


# Carga automática de los datos al iniciar la aplicación.
try:
    with st.spinner("Descargando tipos de cambio del BCE..."):
        fecha, tasas, xml_original = cargar_datos()

except ErrorBCE as error:
    st.error(str(error))
    st.info(
        "Comprueba tu conexión a Internet y vuelve a cargar la página."
    )
    st.stop()


# Información sobre los datos descargados.
st.success(
    f"Datos cargados correctamente. Fecha oficial: {fecha}"
)


# Apartado opcional para consultar el XML completo.
with st.expander("🔍 Ver estructura XML recibida"):
    st.code(xml_original, language="xml")


# Lista de monedas ordenada alfabéticamente.
monedas = sorted(tasas.keys())

indice_euro = monedas.index("EUR")

if "USD" in monedas:
    indice_destino = monedas.index("USD")
else:
    indice_destino = 0


# Campos de la interfaz.
columna_cantidad, columna_origen, columna_destino = st.columns(3)

with columna_cantidad:
    cantidad = st.number_input(
        "Cantidad",
        min_value=0.0,
        value=100.0,
        step=1.0,
        format="%.2f",
    )

with columna_origen:
    moneda_origen = st.selectbox(
        "De",
        monedas,
        index=indice_euro,
    )

with columna_destino:
    moneda_destino = st.selectbox(
        "A",
        monedas,
        index=indice_destino,
    )


# El cálculo solo se realiza cuando el usuario pulsa el botón.
if st.button(
    "Calcular conversión",
    type="primary",
    use_container_width=True,
):
    try:
        resultado = convertir(
            cantidad,
            moneda_origen,
            moneda_destino,
            tasas,
        )

        tipo_cambio = convertir(
            1,
            moneda_origen,
            moneda_destino,
            tasas,
        )

        st.caption(f"Valor en {moneda_destino}")

        st.metric(
            label="Resultado",
            value=f"{resultado:,.2f} {moneda_destino}",
        )

        st.info(
            f"1 {moneda_origen} = "
            f"{tipo_cambio:,.6f} {moneda_destino}"
        )

    except ErrorConversion as error:
        st.error(str(error))


# Tabla con todas las tasas disponibles.
st.divider()

st.subheader("📊 Tabla de tipos de cambio")

st.caption(
    "Las tasas muestran cuántas unidades de cada moneda "
    "equivalen a 1 EUR."
)

tabla_tasas = [
    {
        "Moneda": moneda,
        "Tasa para 1 EUR": tasas[moneda],
    }
    for moneda in monedas
]

st.dataframe(
    tabla_tasas,
    hide_index=True,
    use_container_width=True,
)