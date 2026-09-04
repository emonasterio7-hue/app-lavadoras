import urllib.parse
import streamlit as st

# Configuración de la pantalla del celular (Diseño responsivo móvil)
st.set_page_config(
    page_title="Asistente de Línea Blanca", page_icon="🧺", layout="centered"
)

# 1. BASE DE DATOS LOCAL SIMPLIFICADA (MECÁNICA Y ELÉCTRICA)
CATALOGO = {
    "LG": {
        "no enciende / no prende / pantalla muerta / electrico": [
            "SÍNTOMA: El equipo no da señales de vida ni luces al presionar el botón de encendido.",
            "PASO 1: Medir voltaje en el tomacorriente de la pared con el multímetro (Debe estar entre 110V y 125V AC).",
            "PASO 2: Inspeccionar el cable de alimentación y el filtro de ruido (Line Filter) buscando rastros de cortocircuito.",
            "PASO 3: Desmontar el panel de control y verificar con continuidad si el fusible principal de la tarjeta está quemado.",
            "PASO 4: Si el fusible está abierto, revisar si la bomba de drenaje o el motor están a tierra antes de cambiarlo.",
            "PASO 5: Si llega energía a la placa principal pero la interfaz sigue muerta, reemplazar tarjeta principal."
        ],
        "oe / no desagua / no drena / no tira agua / bomba": [
            "SÍNTOMA: La lavadora no desagua, no drena o no tira el agua.",
            "PASO 1: Limpiar el filtro de la bomba de drenaje en la esquina inferior frontal izquierda.",
            "PASO 2: Verificar que la manguera de desagüe trasera no esté obstruida, doblada o bloqueada.",
            "PASO 3: Medir con multímetro si llegan 120V a la bomba. Si llega voltaje y no drena, reemplazar bomba."
        ],
        "no enjuaga / se salta ciclos / no suaviza / jabon": [
            "SÍNTOMA: El equipo se salta el ciclo de enjuague, deja jabón o no dosifica el suavizante.",
            "PASO 1: Revisar que el cajón dispensador de jabón no esté obstruido con detergente seco endurecido.",
            "PASO 2: Probar la electroválvula específica del enjuague (válvula de suavizante) con multímetro.",
            "PASO 3: Comprobar la manguera del presostato (sensor de nivel) por obstrucciones de sarro."
        ]
    },
    "SAMSUNG": {
        "no enciende / no prende / muerta": [
            "SÍNTOMA: No prende ninguna luz ni responde al botón de Power.",
            "PASO 1: Validar voltaje AC en el enchufe de la pared (110V-125V).",
            "PASO 2: Revisar fusibles térmicos en el arnés interno y el fusible de la tarjeta de potencia."
        ]
    },
    "WHIRLPOOL": {
        "no enciende / no prende": [
            "SÍNTOMA: Pantalla muerta o no responde a los botones del panel.",
            "PASO 1: Validar el suministro eléctrico general y chequear fusible de la placa electrónica."
        ]
    }
}

# =========================================================================
# 2. INTERFAZ GRÁFICA MÓVIL DIRECTA (SIN FILTROS DE MEMORIA TRABADOS)
# =========================================================================
st.title("🧺 Guía Inteligente de Reparación")
st.subheader("Soporte Técnico Especializado (2020-2026)")
st.write("---")

# Entrada del modelo
modelo_ingresado = st.text_input("👉 Ingrese el modelo de la lavadora (Ej: LG WM4000):").strip().upper()

if modelo_ingresado:
    # Detectar marca analizando el texto de forma directa
    modelo_str = str(modelo_ingresado)
    if "SPEED" in modelo_str or "QUEEN" in modelo_str:
        marca_actual = "SPEED QUEEN"
    elif "LG" in modelo_str:
        marca_actual = "LG"
    elif "SAMSUNG" in modelo_str:
        marca_actual = "SAMSUNG"
    else:
        marca_actual = "WHIRLPOOL"

    st.success(f"✅ MODELO CONFIGURADO: **{modelo_str}**")
    st.info(f"📦 Marca asignada al diagnóstico: **{marca_actual}**")
    st.write("---")

    st.write("### 🔍 Buscador de Fallas")
    falla_escrita = st.text_input("✍️ Describa el síntoma o código de error (Ej: 'no drena', 'no prende', 'oe'):").strip().lower()

    if falla_escrita:
        errores_marca = CATALOGO.get(marca_actual, {})
        ruta_a_mostrar = None
        falla_detectada_nombre = ""

        # Buscar coincidencia de palabras clave en las llaves del catálogo local
        for clave, pasos in errores_marca.items():
            if falla_escrita in clave or any(p in clave for p in falla_escrita.split() if len(p) > 2):
                ruta_a_mostrar = pasos
                falla_detectada_nombre = clave.upper()
                break

        # Si se encuentra de forma local, se imprime
        if ruta_a_mostrar:
            st.write("---")
            st.warning(f"🛠️ **DIAGNÓSTICO AUTOMÁTICO | {falla_detectada_nombre}**")
            for paso in ruta_a_mostrar:
                st.info(paso)
            st.error("⚠️ **SEGURIDAD:** Corte la corriente y el agua antes de manipular componentes.")

        # SI LA FALLA ES NUEVA, SE ACTIVA AUTOMÁTICAMENTE EL RASTREADOR TÁCTIL EN INTERNET
        else:
            st.write("---")
            st.error(f"❌ La falla '{falla_escrita.upper()}' no está en la base de datos local para {marca_actual}.")
            st.warning("🚀 **ACTIVANDO BÚSQUEDA EN INTERNET: Consiguiendo diagramas técnicos en la red...**")
            
            # Motores de búsqueda elástica para PDFs de servicio
            consulta_manual = f"{modelo_str} service manual filetype:pdf"
            consulta_error = f"{modelo_str} error {falla_escrita} repair"
            url_manual = "https://google.com" + urllib.parse.quote(consulta_manual)
            url_error = "https://google.com" + urllib.parse.quote(consulta_error)

            st.link_button(f"📥 Descargar Manual de Servicio para {modelo_str}", url_manual, type="primary", use_container_width=True)
            st.link_button(f"🔎 Ver Soluciones y Foros de Reparación en Internet", url_error, use_container_width=True)
