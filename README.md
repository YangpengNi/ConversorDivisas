# Conversor de Divisas

Aplicación web desarrollada con **Python** y **Streamlit** para convertir importes entre las monedas publicadas diariamente por el [Banco Central Europeo (BCE)](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

La aplicación descarga el XML oficial del BCE, utiliza el euro como moneda puente y muestra tanto el resultado de la conversión como la tabla completa de tipos de cambio disponibles.

## Funcionalidades

- Conversión entre cualquiera de las monedas incluidas en el feed diario del BCE.
- EUR y USD seleccionados por defecto cuando están disponibles.
- Visualización del tipo de cambio aplicado y de la fecha oficial de los datos.
- Tabla con todas las tasas, expresadas como unidades de cada moneda por 1 EUR.
- Consulta opcional del XML original recibido del BCE.
- Caché de los datos durante una hora para evitar peticiones innecesarias.
- Validación de cantidades, monedas y tasas de cambio.
- Mensajes claros ante errores de conexión o datos no válidos.

## Requisitos

- Python 3.10 o superior.
- Conexión a Internet para descargar los tipos de cambio.

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/YangpengNi/ConversorDivisas.git
   cd ConversorDivisas
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   ```

   En Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   En macOS o Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Uso

Inicia la aplicación desde la raíz del proyecto:

```bash
python -m streamlit run Proyecto/app.py
```

Streamlit abrirá la interfaz en el navegador. Introduce una cantidad, elige las monedas de origen y destino y pulsa **Calcular conversión**.

## Cómo funciona la conversión

El BCE publica sus tasas tomando el euro como base. Para convertir una cantidad entre dos monedas, primero se obtiene su valor en euros y después se aplica la tasa de la moneda de destino:

```text
cantidad_en_euros = cantidad / tasa_origen
resultado = cantidad_en_euros × tasa_destino
```

Por ejemplo, si 1 EUR equivale a 1,20 USD y a 180 JPY, una conversión de 100 USD a JPY se calcula así:

```text
100 / 1,20 × 180 = 15.000 JPY
```

> [!NOTE]
> Los tipos de referencia del BCE suelen actualizarse una vez por día laborable. La fecha mostrada en la aplicación corresponde a la indicada en el XML oficial, no necesariamente al día actual.

## Pruebas

El módulo de conversión cuenta con pruebas para conversiones directas y cruzadas, la misma moneda, el importe cero y los principales casos de error.

Ejecuta la suite desde la raíz del proyecto:

```bash
python -m pytest
```

## Estructura del proyecto

```text
ConversorDivisas/
├── Proyecto/
│   ├── app.py          # Interfaz de usuario con Streamlit
│   ├── bce_api.py      # Descarga y procesamiento del XML del BCE
│   ├── conversion.py   # Lógica y validaciones de conversión
│   └── __init__.py
├── tests/
│   └── test_conversion.py
├── requirements.txt
└── README.md
```

## Fuente de los datos

Los tipos de cambio proceden del feed diario oficial del BCE:

`https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml`

La disponibilidad de monedas y tasas depende de los datos publicados por el BCE. Las cifras son tipos de referencia informativos y pueden diferir de los aplicados por bancos, casas de cambio o proveedores de pago.
