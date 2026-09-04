import streamlit as st
import difflib

# Configuración de la pantalla del celular (Diseño móvil y responsivo)
st.set_page_config(page_title="Asistente de Línea Blanca", page_icon="🧺", layout="centered")

# =========================================================================
# 1. INICIALIZACIÓN DE LA BASE DE DATOS AUTO-ACTUALIZABLE EN MEMORIA
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
            "oe (falla de drenaje / no tira agua)": [
                "PASO 1: Limpiar el filtro de la bomba de drenaje en la esquina inferior frontal izquierda.",
                "PASO 2: Verificar que la manguera de desagüe trasera no esté obstruida o doblada.",
                "PASO 3: Medir con multímetro si llegan 120V a la bomba. Si llega voltaje y no drena, reemplazar bomba."
            ],
            "ie (no entra agua / falla de válvula)": [
                "PASO 1: Cerrar llaves de paso y limpiar los filtros de malla de las electroválvulas traseras.",
                "PASO 2: Comprobar la continuidad de las bobinas de las electroválvulas con el multímetro.",
                "PASO 3: Verificar que la presión del agua del hogar sea adecuada (mínimo 20 PSI)."
            ],
            "le (sobrecarga del motor / corto en sensor hall)": [
                "PASO 1: Desconectar por 10 minutos para reiniciar el módulo inverter de la tarjeta.",
                "PASO 2: Retirar la tapa trasera y girar la tina a mano para descartar ropa atorada entre las tinas.",
                "PASO 3: Revisar el arnés eléctrico y medir la resistencia del Sensor Hall en el estator (debe dar entre 5k y 15k ohms)."
            ],
            "ue (carga desbalanceada o amortiguador roto)": [
                "PASO 1: Abrir la puerta y redistribuir la carga de ropa pesada (cobijas o jeans).",
                "PASO 2: Comprobar con un nivel de burbuja que las patas de la lavadora estén perfectamente firmes."
            ]
        },
        "SAMSUNG": {
            "4c o 4e (no entra agua)": [
                "PASO 1: Revisar que las llaves de agua estén completamente abiertas.",
                "PASO 2: Limpiar los filtros de malla plástica en las válvulas de entrada de agua."
            ],
            "5c o 5e (error de drenaje)": [
                "PASO 1: Desmontar la manguera de desagüe trasera y limpiar obstrucciones (monedas comunes).",
                "PASO 2: Acceder a la bomba de drenaje por el frente/abajo y retirar residuos atrapados en el propulsor."
            ]
        },
        "SPEED QUEEN": {
            "dl (error de bloqueo de tapa)": [
                "PASO 1: Verificar si la tapa está cerrando por completo o si hay ropa obstruyendo el pestillo.",
                "PASO 2: Desmontar el interruptor de bloqueo de tapa (Lid Lock) debajo del panel superior.",
                "PASO 3: Probar continuidad del solenoide con multímetro. Si está abierto, reemplazar el interruptor."
            ],
            "er (error de sensor de velocidad o motor)": [
                "PASO 1: Desconectar la lavadora de la corriente durante 2 minutos para reiniciar el módulo de control.",
                "PASO 2: Inclinar el equipo y revisar que la banda de transmisión no esté rota, floja o patinando."
            ]
        },
        "WHIRLPOOL": {
            "f5e2 (error de seguro de tapa)": [
                "PASO 1: Revisar si el actuador del blocapuertas superior está roto o bloqueado.",
                "PASO 2: Comprobar el solenoide del pestillo con multímetro o cambiar Lid Lock."
            ]
        }
    }

# =========================================================================
# 2. FUNCIONES DE DETECCIÓN INTELIGENTE
# =========================================================================
def detectar_marca(modelo):
    modelo_up = modelo.upper()
    if "SPEED" in modelo_up or "QUEEN" in modelo_up: return "SPEED QUEEN"
    if modelo_up.startswith("LG"): return "LG"
    if modelo_up.startswith("SAMSUNG"): return "SAMSUNG"
    if modelo_up.startswith("WHIRLPOOL"): return "WHIRLPOOL"
    if modelo_up.startswith("MAYTAG"): return "MAYTAG"
    if modelo_up.startswith("GE") or "GENERAL" in modelo_up: return "GE"
    
    palabras = modelo_up.split()
    return palabras if palabras else "OTRA"

# =========================================================================
# 3. INTERFAZ GRÁFICA MÓVIL (MENÚS TÁCTILES Y BOTONES)
# =========================================================================
st.title("🧺 Guía Inteligente de Reparación")
st.subheader("Soporte Técnico de Línea Blanca (2020-2026)")
st.write("---")

# FASE 1: ENTRADA DEL MODELO
modelo_ingresado = st.text_input("👉 Ingrese o busque el modelo de la lavadora (Ej: LG WM4000):").strip().upper()

if modelo_ingresado:
    # Buscar coincidencia elástica en la base de datos dinámica
    coincidencias = difflib.get_close_matches(modelo_ingresado, st.session_state["modelos"], n=1, cutoff=0.35)
    
    if coincidencias:
        modelo_final = coincidencias
        st.success(f"✅ Modelo reconocido en el sistema: **{modelo_final}**")
        marca_actual = detectar_marca(modelo_final)
    else:
        st.warning(f"⚠️ El modelo **'{modelo_ingresado}'** no existe en la base de datos.")
        
        # Botón interactivo táctil para añadirlo al sistema
        if st.button(f"➕ ¿Desea integrar '{modelo_ingresado}' permanentemente?"):
            st.session_state["modelos"].append(modelo_ingresado)
            st.success(f"🎉 ¡Éxito! El modelo '{modelo_ingresado}' ha sido agregado.")
            st.rerun()
            
        modelo_final = modelo_ingresado
        marca_actual = detectar_marca(modelo_final)

    st.info(f"📦 Marca de trabajo asignada: **{marca_actual}**")
    st.write("---")

    # FASE 2: CATÁLOGO DE ERRORES FILTRADO POR MARCA
    errores_marca = st.session_state["errores"].get(marca_actual, {})
    
    if errores_marca:
        # Limpiar llaves para el menú desplegable de opciones
        opciones_errores = {k.split(" (").upper(): k for k in errores_marca.keys()}
        
        error_sel = st.selectbox("👉 Seleccione el código de error:", options=["-- Seleccione el error --"] + list(opciones_errores.keys()))
        
        if error_sel != "-- Seleccione el error --":
            clave_real = opciones_errores[error_sel]
            st.write("---")
            st.warning(f"🛠️ **DIAGNÓSTICO PARA {marca_actual} | ERROR: {error_sel}**")
            
            # Imprimir los pasos de reparación ordenados en bloques limpios
            st.write("### 📋 Ruta de Reparación Recomendada:")
            for paso in errores_marca[clave_real]:
                st.info(paso)
            st.error("⚠️ **SEGURIDAD:** Corte la corriente y el agua antes de desarmar o manipular cables.")
    else:
        st.info(f"ℹ️ La marca **{marca_actual}** es nueva y no tiene códigos pre-cargados aún. Puedes agregarlos editando el código fuente.")
