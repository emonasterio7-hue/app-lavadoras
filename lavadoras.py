import difflib
import sys
import urllib.parse
import streamlit as st

# Configuración de la pantalla del celular (Diseño responsivo móvil)
st.set_page_config(
    page_title="Asistente de Línea Blanca", page_icon="🧺", layout="centered"
)

# =========================================================================
# 1. BASE DE DATOS MAESTRA: MODELOS Y ERRORES DE FÁBRICA
# =========================================================================
if "modelos" not in st.session_state:
    st.session_state["modelos"] = [
        "LG WM4000HVA", "LG WM3600HWA", "LG WM3400CW", "LG WT7300CW", "LG WT8400CW",
        "WHIRLPOOL WFW5620HW", "WHIRLPOOL WTW5057LW", "WHIRLPOOL WTW4816FW",
        "SAMSUNG WF45T6000AW", "SAMSUNG WA50R5400AW", "MAYTAG MVW6200KW", "MAYTAG MVW7230HW",
        "GE APPLIANCES GFW850SSNWW", "GE APPLIANCES GTW465ASNWW",
        "SPEED QUEEN TC5003WN", "SPEED QUEEN TR7003WN"
    ]

if "errores" not in st.session_state:
    st.session_state["errores"] = {
        "LG": {
            "no enciende / no prende / pantalla muerta": [
                "SÍNTOMA: El equipo no da señales de vida ni luces al presionar el botón de encendido.",
                "PASO 1: Medir voltaje en el tomacorriente de la pared con el multímetro (Debe estar entre 110V y 125V AC).",
                "PASO 2: Inspeccionar el cable de alimentación y el filtro de ruido (Line Filter) buscando rastros de cortocircuito.",
                "PASO 3: Desmontar el panel de control y verificar con continuidad si el fusible principal de la tarjeta está quemado.",
                "PASO 4: Si el fusible está abierto, revisar si la bomba de drenaje o el motor están a tierra antes de cambiarlo.",
                "PASO 5: Si llega energía a la placa principal pero la interfaz sigue muerta, reemplazar tarjeta principal."
            ],
            "oe (no desagua / no drena / bomba)": [
                "SÍNTOMA: La lavadora no desagua, no drena o no tira el agua.",
                "PASO 1: Limpiar el filtro de la bomba de drenaje en la esquina inferior frontal izquierda.",
                "PASO 2: Verificar que la manguera de desagüe trasera no esté obstruida, doblada o bloqueada.",
                "PASO 3: Medir con multímetro si llegan 120V a la bomba. Si llega voltaje y no drena, reemplazar bomba."
            ],
            "ie (no entra agua)": [
                "SÍNTOMA: No entra agua, llena muy lento o marca falta de presión.",
                "PASO 1: Cerrar llaves de paso y limpiar los filtros de malla de las electroválvulas traseras.",
                "PASO 2: Comprobar la continuidad de las bobinas de las electroválvulas con el multímetro.",
                "PASO 3: Verificar que la presión del agua del hogar sea adecuada (mínimo 20 PSI)."
            ],
            "le (motor no gira)": [
                "SÍNTOMA: El motor Direct Drive no gira, se sacude bruscamente o da error de sobrecarga.",
                "PASO 1: Desconectar por 10 minutos para reiniciar el módulo inverter de la tarjeta.",
                "PASO 2: Retirar la tapa trasera y girar la tina a mano para descartar ropa atorada entre las tinas.",
                "PASO 3: Revisar el arnés eléctrico y medir la resistencia del Sensor Hall en el estator (debe dar entre 5k y 15k ohms)."
            ]
        },
        "SAMSUNG": {
            "no enciende / no prende / muerta": [
                "SÍNTOMA: No prende ninguna luz ni responde al botón de Power.",
                "PASO 1: Validar voltaje AC en el enchufe de la pared (110V-125V).",
                "PASO 2: Revisar fusibles térmicos en el cableado interno."
            ],
            "4c": [
                "SÍNTOMA: No entra agua o llena muy lento.",
                "PASO 1: Limpiar los filtros de malla plástica."
            ],
            "5c": [
                "SÍNTOMA: No desagua o no tira el agua.",
                "PASO 1: Desmontar la manguera de desagüe trasera."
            ]
        },
        "WHIRLPOOL": {
            "no enciende / no prende": [
                "SÍNTOMA: Pantalla muerta o no responde a los botones del panel.",
                "PASO 1: Validar el suministro eléctrico general."
            ]
        }
    }

modelos_lista = st.session_state["modelos"]
errores_marcas = st.session_state["errores"]

# =========================================================================
# 2. FUNCIONES DE DETECCIÓN INTELIGENTE Y RASTREO EN INTERNET
# =========================================================================
def detectar_marca(modelo):
    modelo_up = str(modelo).upper()
    if "SPEED" in modelo_up or "QUEEN" in modelo_up: return "SPEED QUEEN"
    if "LG" in modelo_up: return "LG"
    if "SAMSUNG" in modelo_up: return "SAMSUNG"
    if "WHIRLPOOL" in modelo_up: return "WHIRLPOOL"
    return "WHIRLPOOL"

def generar_enlaces_busqueda(modelo, error_falla):
    consulta_manual = f"{modelo} service manual filetype:pdf"
    consulta_error = f"{modelo} error {error_falla} repair"
    url_manual = "https://google.com" + urllib.parse.quote(consulta_manual)
    url_error = "https://google.com" + urllib.parse.quote(consulta_error)
    return url_manual, url_error

# =========================================================================
# 3. INTERFAZ GRÁFICA MÓVIL
# =========================================================================
st.title("🧺 Guía Inteligente de Reparación")
st.subheader("Soporte Técnico Especializado")
st.write("---")

modelo_ingresado = st.text_input("👉 Ingrese o busque el modelo de la lavadora:").strip().upper()

if modelo_ingresado:
    coincidencias = difflib.get_close_matches(modelo_ingresado, modelos_lista, n=1, cutoff=0.3)

    if coincidencias:
        modelo_final = coincidencias[0]
        st.success(f"✅ Modelo reconocido en el sistema: **{modelo_final}**")
        marca_actual = detectar_marca(modelo_final)
    else:
        st.warning(f"⚠️ El modelo **'{modelo_ingresado}'** no existe en la base de datos.")
        if st.button(f"➕ ¿Desea integrar '{modelo_ingresado}' permanentemente?"):
            st.session_state["modelos"].append(modelo_ingresado)
            st.success(f"🎉 ¡Éxito! El modelo '{modelo_ingresado}' ha sido agregado.")
            st.rerun()
        modelo_final = modelo_ingresado
        marca_actual = detectar_marca(modelo_final)

    st.info(f"📦 Marca de trabajo asignada: **{marca_actual}**")
    st.write("---")

    errores_marca = errores_marcas.get(marca_actual, {})
    st.write("### 🔍 Buscador de Fallas")

    codigos_lista = ["-- Seleccione un código de error --"] + [c.upper() for c in errores_marca.keys() if len(c) <= 5]
    error_seleccionado = st.selectbox("🎛️ Opción A: Por Código de Error de la pantalla:", options=codigos_lista)

    falla_escrita = st.text_input("✍️ Opción B: O describa el síntoma con sus palabras:").strip().lower()

    ruta_a_mostrar = None
    falla_detectada_nombre = ""
    termino_busqueda_internet = ""

    if error_seleccionado != "-- Seleccione un código de error --":
        clave_real = error_seleccionado.lower()
        ruta_a_mostrar = errores_marca.get(clave_real)
        falla_detectada_nombre = f"CÓDIGO {error_seleccionado}"
        termino_busqueda_internet = error_seleccionado

    elif falla_escrita:
        termino_busqueda_internet = falla_escrita
        claves_disponibles = list(errores_marca.keys())

        # NUEVA LÓGICA PRECIAS POR PALABRA CLAVE COMPLETA (Busca coincidencias directas en la llave)
        for clave in claves_disponibles:
            palabras_clave = clave.replace("/", " ").replace("(", " ").replace(")", " ").split()
            if any(palabra in palabras_clave for palabra in falla_escrita.split() if len(palabra) > 2):
                ruta_a_mostrar = errores_marca[clave]
                falla_detectada_nombre = f"SÍNTOMA ASOCIADO A '{clave.upper()}'"
                break

        # Búsqueda secundaria si no hizo match en el título
        if not ruta_a_mostrar:
            for clave, pasos in errores_marca.items():
                texto_completo_pasos = " ".join(pasos).lower()
                if falla_escrita in texto_completo_pasos:
                    ruta_a_mostrar = pasos
                    falla_detectada_nombre = f"SÍNTOMA ENCONTRADO EN LA RUTA '{clave.upper()}'"
                    break

    if ruta_a_mostrar:
        st.write("---")
        st.warning(f"🛠️ **DIAGNÓSTICO AUTOMÁTICO | {falla_detectada_nombre}**")
        st.write("### 📋 Ruta de Reparación Recomendada:")
        for paso in ruta_a_mostrar:
            st.info(paso)
        st.error("⚠️ **SEGURIDAD:** Corte la corriente y el agua antes de manipular componentes.")

        st.write("---")
        st.write("🌐 **¿Necesitas más información técnica de este modelo?**")
        url_manual, url_error = generar_enlaces_busqueda(modelo_final, termino_busqueda_internet)

        st.link_button("📘 Buscar Manual PDF en Internet", url_manual, use_container_width=True)
        st.link_button("🔍 Soluciones Extras en Foros", url_error, use_container_width=True)

    elif falla_escrita or error_seleccionado != "-- Seleccione un código de error --":
        st.write("---")
        st.error(f"❌ La falla '{termino_busqueda_internet.upper()}' no está registrada localmente.")
        url_manual, url_error = generar_enlaces_busqueda(modelo_final, termino_busqueda_internet)
        st.link_button(f"📥 Descargar Manual de Servicio para {modelo_final}", url_manual, type="primary", use_container_width=True)
