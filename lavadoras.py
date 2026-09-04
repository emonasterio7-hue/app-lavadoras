import difflib
import sys
import urllib.parse
import streamlit as st

# Configuración de la pantalla del celular (Diseño responsivo móvil)
st.set_page_config(
    page_title="Asistente de Línea Blanca", page_icon="🧺", layout="centered"
)

# =========================================================================
# 1. BASE DE DATOS INTEGRADA: MODELOS Y ERRORES DE FÁBRICA (2020-2026)
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
            "oe": [
                "SÍNTOMA: La lavadora no desagua o no tira el agua.",
                "PASO 1: Limpiar el filtro de la bomba de drenaje en la esquina inferior frontal izquierda.",
                "PASO 2: Verificar que la manguera de desagüe trasera no esté obstruida, doblada o bloqueada.",
                "PASO 3: Medir con multímetro si llegan 120V a la bomba. Si llega voltaje y no drena, reemplazar bomba.",
            ],
            "ie": [
                "SÍNTOMA: No entra agua o llena muy lento.",
                "PASO 1: Cerrar llaves de paso y limpiar los filtros de malla de las electroválvulas traseras.",
                "PASO 2: Comprobar la continuidad de las bobinas de las electroválvulas con el multímetro.",
                "PASO 3: Verificar que la presión del agua del hogar sea adecuada (mínimo 20 PSI).",
            ],
            "le": [
                "SÍNTOMA: El motor no gira o da error de sobrecarga.",
                "PASO 1: Desconectar por 10 minutos para reiniciar el módulo inverter de la tarjeta.",
                "PASO 2: Retirar la tapa trasera y girar la tina a mano para descartar ropa atorada entre las tinas.",
                "PASO 3: Revisar el arnés eléctrico y medir la resistencia del Sensor Hall en el estator (debe dar entre 5k y 15k ohms).",
            ],
            "ue": [
                "SÍNTOMA: Vibra mucho o la carga está desbalanceada.",
                "PASO 1: Abrir la puerta y redistribuir la carga de ropa pesada (cobijas o jeans).",
                "PASO 2: Comprobar con un nivel de burbuja que las patas de la lavadora estén perfectamente firmes.",
            ],
        },
        "SAMSUNG": {
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
            "f5e2": [
                "SÍNTOMA: Error de seguro de tapa o interruptor bloqueado.",
                "PASO 1: Revisar si el actuador del blocapuertas superior está roto o bloqueado.",
                "PASO 2: Comprobar el solenoide del pestillo con multímetro o cambiar Lid Lock.",
            ]
        },
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
        c.upper() for c in errores_marca.keys()
    ]
    error_seleccionado = st.selectbox(
        "🎛️ Opción A: Por Código de Error de la pantalla:", options=codigos_lista
    )

    falla_escrita = (
        st.text_input(
            "✍️ Opción B: O describa el síntoma con sus palabras (Ej: 'no drena', 'ruido'):"
        )
        .strip()
        .lower()
    )

    ruta_a_mostrar = None
    falla_detectada_nombre = ""
    termino_busqueda_internet = ""

    # Evaluation of Entrance
    if error_seleccionado != "-- Seleccione un código de error --":
        clave_real = error_seleccionado.lower()
        ruta_a_mostrar = errores_marca.get(clave_real)
        falla_detectada_nombre = f"CÓDIGO {error_seleccionado}"
        termino_busqueda_internet = error_seleccionado

    elif falla_escrita:
        termino_busqueda_internet = falla_escrita
        claves_disponibles = list(errores_marca.keys())

        for clave, pasos in errores_marca.items():
            texto_completo_pasos = " ".join(pasos).lower()
            if falla_escrita in texto_completo_pasos or falla_escrita in clave:
                ruta_a_mostrar = pasos
                falla_detectada_nombre = (
                    f"SÍNTOMA ASOCIADO AL ERROR '{clave.upper()}'"
                )
                break

        if not ruta_a_mostrar:
            coincidencia_flexible = difflib.get_close_matches(
                falla_escrita, claves_disponibles, n=1, cutoff=0.2
            )
            if coincidencia_flexible:
                clave_flex = coincidencia_flexible[0]
                ruta_a_mostrar = errores_marca.get(clave_flex)
                falla_detectada_nombre = (
                    f"SÍNTOMA ASOCIADO AL ERROR '{clave_flex.upper()}'"
                )

    # FASE 3: IMPRESIÓN DE SOLUCIONES INTERNAS O BÚSQUEDA EN INTERNET
    if ruta_a_mostrar:
        st.write("---")
        st.warning(f"🛠️ **DIAGNÓSTICO AUTOMÁTICO | {falla_detectada_nombre}**")
        st.write("### 📋 Ruta de Reparación Recomendada:")
        for paso in ruta_a_mostrar:
            st.info(paso)
        st.error(
            "⚠️ **SEGURIDAD:** Corte la corriente y el agua antes de manipular componentes."
        )

        st.write("---")
        st.write("🌐 **¿Necesitas más información técnica de este modelo?**")
        url_manual, url_error = generar_enlaces_busqueda(
            modelo_final, termino_busqueda_internet
        )

        col1, col2 = st.columns(2)
        col1.link_button("📘 Buscar Manual PDF", url_manual, use_container_width=True)
        col2.link_button(
            "🔍 Soluciones en Internet", url_error, use_container_width=True
        )

    elif falla_escrita or (
