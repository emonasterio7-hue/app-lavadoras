import difflib
import sys
import urllib.parse
import streamlit as st

# Configuración de la pantalla del celular (Diseño responsivo móvil)
st.set_page_config(
    page_title="Asistente de Línea Blanca", page_icon="🧺", layout="centered"
)

# =========================================================================
# 1. BASE DE DATOS INTEGRADA: MODELOS Y ERRORES DE FÁBRICA (MECÁNICOS Y ELÉCTRICOS)
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
            "no enciende / no prende / pantalla muerta": [
                "SÍNTOMA: El equipo no da señales de vida ni luces al presionar el botón de encendido.",
                "PASO 1: Medir voltaje en el tomacorriente de la pared con el multímetro (Debe estar entre 110V y 125V AC).",
                "PASO 2: Inspeccionar el cable de alimentación y el filtro de ruido (Line Filter) buscando rastros de cortocircuito o cables abiertos.",
                "PASO 3: Desmontar el panel de control y verificar con continuidad si el fusible principal de la tarjeta está quemado.",
                "PASO 4: Si el fusible está abierto, revisar si la bomba de drenaje o el motor están a tierra antes de cambiarlo.",
                "PASO 5: Si llega energía a la placa principal pero la interfaz sigue muerta, el regulador de voltaje de la fuente falló. Reemplazar tarjeta.",
            ],
            "oe": [
                "SÍNTOMA: La lavadora no desagua, no drena o no tira el agua.",
                "PASO 1: Limpiar el filtro de la bomba de drenaje en la esquina inferior frontal izquierda.",
                "PASO 2: Verificar que la manguera de desagüe trasera no esté obstruida, doblada o bloqueada.",
                "PASO 3: Medir con multímetro si llegan 120V a la bomba. Si llega voltaje y no drena, reemplazar bomba.",
            ],
            "ie": [
                "SÍNTOMA: No entra agua, llena muy lento o marca falta de presión.",
                "PASO 1: Cerrar llaves de paso y limpiar los filtros de malla de las electroválvulas traseras.",
                "PASO 2: Comprobar la continuidad de las bobinas de las electroválvulas con el multímetro.",
                "PASO 3: Verificar que la presión del agua del hogar sea adecuada (mínimo 20 PSI).",
            ],
            "le": [
                "SÍNTOMA: El motor Direct Drive no gira, se sacude bruscamente o da error de sobrecarga.",
                "PASO 1: Desconectar por 10 minutos para reiniciar el módulo inverter de la tarjeta.",
                "PASO 2: Retirar la tapa trasera y girar la tina a mano para descartar ropa atorada entre las tinas.",
                "PASO 3: Revisar el arnés eléctrico y medir la resistencia del Sensor Hall en el estator (debe dar entre 5k y 15k ohms).",
            ],
            "ue": [
                "SÍNTOMA: Vibra mucho, golpea los lados o la carga está desbalanceada en el centrifugado.",
                "PASO 1: Abrir la puerta y redistribuir la carga de ropa pesada (cobijas o jeans) que se haya amontonado.",
                "PASO 2: Comprobar con un nivel de burbuja que las patas de la lavadora estén perfectamente firmes.",
            ],
        },
        "SAMSUNG": {
            "no enciende / no prende / muerta": [
                "SÍNTOMA: No prende ninguna luz ni responde al botón de Power.",
                "PASO 1: Validar voltaje AC en el enchufe de la pared (110V-125V).",
                "PASO 2: Revisar fusibles térmicos en el cableado interno y el fusible de la tarjeta de potencia (IPM).",
                "PASO 3: Revisar capacitores de la fuente conmutada; si están inflados, requieren reemplazo.",
            ],
            "4c": [
                "SÍNTOMA: No entra agua o llena muy lento.",
                "PASO 1: Revisar que las llaves de agua estén completamente abiertas.",
                "PASO 2: Limpiar los filtros de malla plástica en las válvulas de entrada de agua.",
            ],
            "5c": [
                "SÍNTOMA: No desagua o no tira el agua.",
                "PASO 1: Desmontar la manguera de desagüe trasera y limpiar obstrucciones (monedas comunes).",
                "PASO 2: Acceder a la bomba de drenaje por el frente/abajo y retirar residuos atrapados en el propulsor.",
            ],
        },
        "SPEED QUEEN": {
            "no enciende / no prende": [
                "SÍNTOMA: Lavadora comercial o residencial de uso rudo totalmente muerta.",
                "PASO 1: Verificar el disyuntor de la casa (breaker) y el interruptor principal trasero si lo incluye.",
                "PASO 2: Comprobar el cableado hacia el temporizador mecánico o tarjeta electrónica.",
                "PASO 3: Verificar continuidad en el fusible de protección de línea interna.",
            ],
            "dl": [
                "SÍNTOMA: Falla de puerta, seguro de tapa o no exprime.",
                "PASO 1: Verificar si la tapa está cerrando por completo o si hay ropa obstruyendo el pestillo.",
                "PASO 2: Desmontar el interruptor de bloqueo de tapa (Lid Lock) debajo del panel superior.",
                "PASO 3: Probar continuidad del solenoide con multímetro. Si está abierto, reemplazar el interruptor.",
            ],
            "er": [
                "SÍNTOMA: El motor no gira o tiene falla de velocidad.",
                "PASO 1: Desconectar la lavadora de la corriente durante 2 minutos para reiniciar el módulo de control.",
                "PASO 2: Inclinar el equipo y revisar que la banda de transmisión no esté rota, floja o patinando.",
            ],
        },
        "WHIRLPOOL": {
            "no enciende / no prende": [
                "SÍNTOMA: Pantalla muerta o no responde a los botones del panel.",
                "PASO 1: Validar el suministro eléctrico general.",
                "PASO 2: Desmontar consola y chequear fusible de herradura en la entrada de la placa electrónica.",
                "PASO 3: Probar transformador de la placa buscando lecturas abiertas.",
            ],
            "f5e2": [
                "SÍNTOMA: Error de seguro de tapa o interruptor bloqueado.",
                "PASO 1: Revisar si el actuador del blocapuertas superior está roto o bloqueado.",
                "PASO 2: Comprobar el solenoide del pestillo con multímetro o cambiar Lid Lock.",
            ],
        },
    }
}

modelos_lista = st.session_state["modelos"]
errores_marcas = st.session_state["errores"]


# =========================================================================
# 2. FUNCIONES DE DETECCIÓN INTELIGENTE Y RASTREO EN INTERNET
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
# 3. INTERFAZ GRÁFICA MÓVIL
# =========================================================================
st.title("🧺 Guía Inteligente de Reparación")
st.subheader("Soporte Técnico Especializado")
st.write("---")

# FASE 1: ENTRADA DEL MODELO
modelo_ingresado = (
    st.text_input("👉 Ingrese o busque el modelo de la lavadora:").strip().upper()
)

if modelo_ingresado:
    coincidencias = difflib.get_close_matches(
        modelo_ingresado, modelos_lista, n=1, cutoff=0.3
    )

    if coincidencias:
        modelo_final = coincidencias[0]
        st.success(f"✅ Modelo reconocido en el sistema: **{modelo_final}**")
        marca_actual = detectar_marca(modelo_final)
    else:
        st.warning(
            f"⚠️ El modelo **'{modelo_ingresado}'** no existe en la base de datos."
        )
        if st.button(f"➕ ¿Desea integrar '{modelo_ingresado}' permanentemente?"):
            st.session_state["modelos"].append(modelo_ingresado)
            st.success(f"🎉 ¡Éxito! El modelo '{modelo_ingresado}' ha sido agregado.")
            st.rerun()
        modelo_final = modelo_ingresado
        marca_actual = detectar_marca(modelo_final)

    st.info(f"📦 Marca de trabajo asignada: **{marca_actual}**")
    st.write("---")

    # FASE 2: PANEL DUAL DE TRABAJO
    errores_marca = errores_marcas.get(marca_actual, {})

    st.write("### 🔍 Buscador de Fallas")

    codigos_lista = ["-- Seleccione un código de error --"] + [
        c.upper() for c in errores_marca.keys() if len(c) <= 5
    ]
    error_seleccionado = st.selectbox(
        "🎛️ Opción A: Por Código de Error de la pantalla:", options=codigos_lista
    )

    falla_escrita = (
        st.text_input(
