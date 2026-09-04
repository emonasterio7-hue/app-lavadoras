import difflib
import sys
import urllib.parse
import streamlit as st

# Configuración de la pantalla del celular (Diseño responsivo móvil)
st.set_page_config(
    page_title="Asistente de Línea Blanca", page_icon="🧺", layout="centered"
)

# =========================================================================
# 1. BASE DE DATOS MAESTRA TOTAL: ELÉCTRICA, MECÁNICA Y CICLOS
# =========================================================================
if "modelos" not in st.session_state:
    st.session_state["modelos"] = [
        "LG WM4000HVA",
        "LG WM3600HWA",
        "LG WM3400CW",
        "LG WT7300CW",
        "LG WT8400CW",
        "WHIRLPOOL WFW5620HW",
        "WHIRLPOOL WTW5057LW",
        "WHIRLPOOL WTW4816FW",
        "SAMSUNG WF45T6000AW",
        "SAMSUNG WA50R5400AW",
        "MAYTAG MVW6200KW",
        "MAYTAG MVW7230HW",
        "GE APPLIANCES GFW850SSNWW",
        "GE APPLIANCES GTW465ASNWW",
        "SPEED QUEEN TC5003WN",
        "SPEED QUEEN TR7003WN",
    ]

if "errores" not in st.session_state:
    st.session_state["errores"] = {
        "LG": {
            "no enciende / no prende / pantalla muerta / electrico": [
                "SÍNTOMA: El equipo no da señales de vida ni luces al presionar el botón de encendido.",
                "PASO 1: Medir voltaje en el tomacorriente de la pared con el multímetro (Debe estar entre 110V y 125V AC).",
                "PASO 2: Inspeccionar el cable de alimentación y el filtro de ruido (Line Filter) buscando rastros de cortocircuito.",
                "PASO 3: Desmontar el panel de control y verificar con continuidad si el fusible principal de la tarjeta está quemado.",
                "PASO 4: Si el fusible está abierto, revisar si la bomba de drenaje o el motor están a tierra antes de cambiarlo.",
                "PASO 5: Si llega energía a la placa principal pero la interfaz sigue muerta, reemplazar tarjeta principal.",
            ],
            "oe / no desagua / no drena / no tira agua / bomba": [
                "SÍNTOMA: La lavadora no desagua, no drena o no tira el agua.",
                "PASO 1: Limpiar el filtro de la bomba de drenaje en la esquina inferior frontal izquierda.",
                "PASO 2: Verificar que la manguera de desagüe trasera no esté obstruida, doblada o bloqueada.",
                "PASO 3: Medir con multímetro si llegan 120V a la bomba. Si llega voltaje y no drena, reemplazar bomba.",
            ],
            "ie / no entra agua / llena lento / electrovalvula": [
                "SÍNTOMA: No entra agua, llena muy lento o marca falta de presión.",
                "PASO 1: Cerrar llaves de paso y limpiar los filtros de malla de las electroválvulas traseras.",
                "PASO 2: Comprobar la continuidad de las bobinas de las electroválvulas con el multímetro.",
                "PASO 3: Verificar que la presión del agua del hogar sea adecuada (mínimo 20 PSI).",
            ],
            "le / motor no gira / no lava / no exprime / sensor hall": [
                "SÍNTOMA: El motor Direct Drive no gira, se sacude bruscamente o da error de sobrecarga.",
                "PASO 1: Desconectar por 10 minutos para reiniciar el módulo inverter de la tarjeta.",
                "PASO 2: Retirar la tapa trasera y girar la tina a mano para descartar ropa atorada entre las tinas.",
                "PASO 3: Revisar el arnés eléctrico y medir la resistencia del Sensor Hall en el estator (debe dar entre 5k y 15k ohms).",
            ],
            "ue / vibra mucho / ruido fuerte / golpea / suspension": [
                "SÍNTOMA: Vibra mucho, golpea los lados o la carga está desbalanceada en el centrifugado.",
                "PASO 1: Abrir la puerta y redistribuir la carga de ropa pesada (cobijas o jeans) que se haya amontonado.",
                "PASO 2: Comprobar con un nivel de burbuja que las patas de la lavadora estén perfectamente firmes.",
                "PASO 3: En carga superior, revisar las varillas de suspensión trasera; si están flojas, reemplazarlas.",
            ],
            "de / de1 / puerta abierta / switch / seguro / tapa": [
                "SÍNTOMA: No inicia ciclos porque detecta la puerta o tapa abierta.",
                "PASO 1: Limpiar el pestillo y verificar la alineación mecánica del gancho de la puerta.",
                "PASO 2: Desmontar el interruptor de bloqueo (Door Lock Switch) y medir continuidad.",
            ],
            "no enjuaga / se salta ciclos / no suaviza / jabon": [
                "SÍNTOMA: El equipo se salta el ciclo de enjuague, deja jabón o no dosifica el suavizante.",
                "PASO 1: Revisar que el cajón dispensador de jabón no esté obstruido con detergente seco endurecido.",
                "PASO 2: Probar la electroválvula específica del enjuague (válvula secundaria o de suavizante) con multímetro.",
                "PASO 3: Comprobar el presostato (sensor de nivel); si lee mal el nivel de vaciado previo, saltará el enjuague.",
            ],
        },
        "SAMSUNG": {
            "no enciende / no prende / muerta / electrico": [
                "SÍNTOMA: No prende ninguna luz ni responde al botón de Power.",
                "PASO 1: Validar voltaje AC en el enchufe de la pared (110V-125V).",
                "PASO 2: Revisar fusibles térmicos en el cableado interno y el fusible de la tarjeta de potencia (IPM).",
            ],
            "4c / 4e / no entra agua / electrovalvula": [
                "SÍNTOMA: No entra agua o llena muy lento.",
                "PASO 1: Revisar que las llaves de agua estén completamente abiertas y limpiar filtros de malla.",
            ],
            "5c / 5e / no desagua / no drena / bomba": [
                "SÍNTOMA: No desagua o no tira el agua.",
                "PASO 1: Desmontar la manguera de desagüe trasera y limpiar obstrucciones.",
                "PASO 2: Acceder a la bomba de drenaje por el frente/abajo y retirar residuos.",
            ],
            "ub / dc / vibra mucho / suspension / desbalance": [
                "SÍNTOMA: Carga desbalanceada o vibración extrema en exprimido.",
                "PASO 1: Acomodar la ropa de forma uniforme. En carga superior, revisar las 4 varillas de suspensión.",
            ],
            "no enjuaga / se detiene / suavizante": [
                "SÍNTOMA: Se queda congelada antes del enjuague o no vierte el suavizante.",
                "PASO 1: Limpiar el cajón de distribución y probar solenoides de las electroválvulas de llenado de enjuague.",
            ],
        },
        "SPEED QUEEN": {
            "no enciende / no prende": [
                "SÍNTOMA: Lavadora comercial o residencial de uso rudo totalmente muerta.",
                "PASO 1: Verificar el disyuntor de la casa (breaker) y el interruptor principal trasero.",
            ],
            "dl / seguro / puerta / tapa": [
                "SÍNTOMA: Falla de puerta, seguro de tapa o no exprime.",
                "PASO 1: Verificar si la tapa está cerrando por completo o si hay ropa obstruyendo el pestillo.",
                "PASO 2: Desmontar el interruptor de bloqueo de tapa (Lid Lock) debajo del panel superior.",
            ],
            "er / no gira / motor": [
                "SÍNTOMA: El motor no gira o tiene falla de velocidad.",
                "PASO 1: Desconectar la lavadora de la corriente durante 2 minutos para reiniciar el módulo de control.",
                "PASO 2: Inclinar el equipo y revisar que la banda de transmisión no esté rota, floja o patinando.",
            ],
        },
        "WHIRLPOOL": {
            "no enciende / no prende": [
                "SÍNTOMA: Pantalla muerta o no responde a los botones del panel.",
                "PASO 1: Validar el suministro eléctrico general y chequear fusible de la placa electrónica.",
            ],
            "f5e2 / seguro / tapa / lid lock": [
                "SÍNTOMA: Error de seguro de tapa o interruptor bloqueado.",
                "PASO 1: Revisar si el actuador del blocapuertas superior está roto o bloqueado.",
            ],
            "no desagua / no drena / f5e1": [
                "SÍNTOMA: No saca el agua de la tina.",
                "PASO 1: Revisar bomba de drenaje inferior y limpiar monedas o pasadores atorados.",
            ],
            "no enjuaga / no exprime / actuador / shift": [
                "SÍNTOMA: Lava bien pero se traba al pasar a enjuagar o exprimir.",
                "PASO 1: Voltear la lavadora por debajo y revisar el Actuador de Cambio (Shift Actuator).",
                "PASO 2: Limpiar el sensor óptico del actuador o reemplazar la pieza si el motorcito no acopla la transmisión.",
            ],
        },
    }
}

modelos_lista = st.session_state["modelos"]
errores_marcas = st.session_state["errores"]


# =========================================================================
# 2. CORE LOGIC: PROCESADOR ELÁSTICO AVANZADO POR RAÍZ DE PALABRAS
# =========================================================================
def detectar_marca(modelo):
    modelo_up = str(modelo).upper()
    if "SPEED" in modelo_up or "QUEEN" in modelo_up:
        return "SPEED QUEEN"
    if "LG" in modelo_up:
        return "LG"
    if "SAMSUNG" in modelo_up:
        return "SAMSUNG"
    if "WHIRLPOOL" in modelo_up:
        return "WHIRLPOOL"
    if "MAYTAG" in modelo_up:
        return "MAYTAG"
    if "GE" in modelo_up or "GENERAL" in modelo_up:
        return "GE"
    return "WHIRLPOOL"


def generar_enlaces_busqueda(modelo, error_falla):
    consulta_manual = f"{modelo} service manual filetype:pdf"
    consulta_error = f"{modelo} error {error_falla} repair"
    url_manual = "https://google.com" + urllib.parse.quote(
        consulta_manual
    )
    url_error = "https://google.com" + urllib.parse.quote(
        consulta_error
    )
    return url_manual, url_error


# =========================================================================
