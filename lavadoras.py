import difflib
import sys
import urllib.parse
import streamlit as st

# Configuración de la pantalla del celular (Diseño responsivo móvil de alto rendimiento)
st.set_page_config(
    page_title="Asistente de Línea Blanca", page_icon="🧺", layout="centered"
)

# =========================================================================
# 1. LA GRAN BASE DE DATOS ULTRA-COMPLETA (EL 90% DE LAS REPARACIONES DEL TALLER)
# =========================================================================
CATALOGO_MAESTRO = {
    # --- MÓDULO 1: SISTEMA ELÉCTRICO Y DE POTENCIA ---
    "no enciende / no prende / pantalla muerta / muerta / cortocircuito / tumba el breaker / fusible": [
        "SÍNTOMA: El equipo no da luces, está totalmente muerto o hace saltar las protecciones eléctricas.",
        "PASO 1: Medir el voltaje AC en el tomacorriente de la pared con el multímetro (Debe marcar entre 110V y 125V AC).",
        "PASO 2: Inspeccionar visualmente el cable de alimentación, el enchufe y el Filtro de Ruido (Line Filter) trasero buscando quemaduras.",
        "PASO 3: Desmontar el panel de control y verificar el fusible principal de la tarjeta electrónica en escala de continuidad (Hz/Buzzer).",
        "PASO 4: Si el fusible está abierto, ¡CUIDADO! Mide la resistencia de la bomba de drenaje y del motor antes de cambiarlo para descartar que estén cruzados a tierra.",
        "PASO 5: Si llega voltaje correcto a la placa principal pero la pantalla sigue muerta, el regulador de la fuente conmutada falló. Reemplazar o reparar tarjeta."
    ],
    
    # --- MÓDULO 2: SISTEMA DE DRENAJE Y EVACUACIÓN ---
    "oe / 5c / 5e / no desagua / no drena / no tira agua / no bota el agua / bomba de agua / filtro bloqueado": [
        "SÍNTOMA: La lavadora se detiene con agua adentro de la tina y no realiza el vaciado.",
        "PASO 1: Acceder a la esquina inferior frontal (en carga frontal) o retirar la cubierta y limpiar por completo el filtro atrapapelusas.",
        "PASO 2: Desconectar la manguera de desagüe trasera y soplar a través de ella para asegurar que no tenga monedas, calcetines o sarro atorado.",
        "PASO 3: Colocar la lavadora en ciclo de centrifugado/drenaje y medir con el multímetro si le llegan 120V AC a los terminales de la bomba.",
        "PASO 4: Si llegan los 120V pero la bomba solo zumba, vibra o no gira el propulsor, desmóntala y reemplázala de inmediato.",
        "PASO 5: Si no llega voltaje a la bomba, verificar continuidad en el cableado que sube hacia la tarjeta principal."
    ],
    
    # --- MÓDULO 3: SISTEMA DE LLENADO Y PRESION ---
    "ie / 4c / 4e / f8e1 / h2o / ih / no entra agua / llena lento / no llena / electrovalvula / falta presion": [
        "SÍNTOMA: El equipo zumba en la parte trasera pero no ingresa agua a la tina, o el llenado tarda más de lo normal.",
        "PASO 1: Validar que las llaves de paso del hogar estén abiertas por completo y que las mangueras no estén estranguladas atrás.",
        "PASO 2: Cerrar el agua, desenroscar las mangueras de las electroválvulas y retirar con una pinza las mallas plásticas internas para limpiarlas del sarro.",
        "PASO 3: Medir la resistencia (Ohms) en las bobinas de las electroválvulas. Una lectura normal es de 1k a 1.5k ohms. Si marca 'OL' (abierto), la bobina está quemada.",
        "PASO 4: Inspeccionar la manguera transparente del presostato (sensor de nivel). Si está agrietada, rota o tiene agua atrapada, el equipo no sabrá que está vacío.",
        "PASO 5: Probar el presostato midiendo sus variaciones de frecuencia o continuidad al soplar suavemente por la manguera."
    ],
    
    # --- MÓDULO 4: TRANSMISIÓN, CENTRIFUGADO Y EXPRIMIDO ---
    "no exprime / no centrifuga / no gira / no lava / le / 3c / 3e / er / motor no gira / banda rota / polea suelta": [
        "SÍNTOMA: La lavadora drena el agua correctamente pero se queda estancada sin hacer girar la tina a alta velocidad.",
        "PASO 1: Comprobar visualmente la banda de transmisión inferior (en modelos de polea). Si está floja, deshilachada o rota, reemplazar y tensar.",
        "PASO 2: En modelos Direct Drive (sin banda), desmontar el rotor trasero y verificar el Sensor Hall acomodado en el estator. Debe medir entre 5k y 15k ohms.",
        "PASO 3: Probar los tres terminales del motor con el multímetro en escala de ohms. Las tres mediciones entre los pines deben dar valores idénticos.",
        "PASO 4: En lavadoras de carga superior Whirlpool/Maytag, inspeccionar mecánicamente el embrague (clutch) y el termoactuador que acopla la tina.",
        "PASO 5: Girar la tina con la mano en vacío. Si se siente amarrada o pesada, el daño es mecánico directo en los baleros o rodamientos centrales."
    ],
    
    # --- MÓDULO 5: BALANCE, AMORTIGUACIÓN Y ESTRUCTURA ---
    "ue / ub / dc / f0e5 / vibra mucho / ruido fuerte / golpea / se mueve / amortiguadores / varillas de suspension / nivelacion": [
        "SÍNTOMA: Al empezar a tomar velocidad en el centrifugado, la tina baila de forma violenta, golpea el mueble o se camina sola.",
        "PASO 1: Abrir la tapa y verificar que la carga de ropa no esté hecha una sola bola pesada (reacomodar jeans, toallas o cobijas de forma uniforme).",
        "PASO 2: Colocar un nivel de burbuja sobre la tapa de la lavadora y ajustar las patas roscadas inferiores hasta que quede perfectamente firme.",
        "PASO 3: En carga superior, presionar la tina hacia abajo y soltarla. Si rebota más de una vez como un trampolín, las 4 varillas de suspensión perdieron su grasa de amortiguación.",
        "PASO 4: En carga frontal, revisar las pesas de concreto superiores y los amortiguadores de pistón inferiores buscando pérdidas de aceite o fracturas.",
        "PASO 5: Mover la tina de adentro hacia arriba y hacia abajo con la mano. Si tiene juego respecto al eje, la cruz de la tina (spider arm) está rota."
    ],
    
    # --- MÓDULO 6: SEGURIDAD Y CICLOS TRABADOS ---
    "de / de1 / f5e2 / f5e1 / seguro / tapa / puerta / puerta abierta / switch / blocapuertas / lid lock / no abre": [
        "SÍNTOMA: El equipo muestra error de puerta abierta en la pantalla o se queda la puerta trabada al finalizar la reparación.",
        "PASO 1: Inspeccionar mecánicamente el gancho o pestillo plástico de la puerta. Si está fracturado, no accionará el interruptor interno.",
        "PASO 2: Desmontar el blocapuertas (Door Lock) y medir con el multímetro si le llega el pulso de voltaje desde la tarjeta al iniciar el ciclo.",
        "PASO 3: Validar la continuidad en los contactos internos del interruptor que confirman el cierre seguro hacia el procesador principal.",
        "PASO 4: Para destrabar una puerta bloqueada al final del ciclo, ubicar el cordón de liberación manual inferior al lado del filtro de drenaje."
    ],
    
    # --- MÓDULO 7: FALLAS DE PROGRAMACIÓN Y ENJUAGUE ---
    "no enjuaga / se salta ciclos / no saca el jabon / no bota el suavizante / se queda pegado / se congela el tiempo / se pausa sola": [
        "SÍNTOMA: La lavadora realiza el lavado pero se salta el enjuague, deja la ropa con jabón, o el reloj digital se queda congelado en un minuto eterno.",
        "PASO 1: Retirar por completo el cajón dispensador de plástico y lavarlo con agua caliente para remover tapones de jabón o suavizante viejo endurecido.",
        "PASO 2: Probar con el multímetro la electroválvula específica encargada del enjuague (las lavadoras modernas tienen de 3 a 4 bobinas traseras).",
        "PASO 3: Limpiar la trampa de aire que conecta la tina con la manguera del presostato; si acumula sedimentos, la tarjeta se confunde al vaciar el agua.",
        "PASO 4: Desconectar el equipo de la red eléctrica durante 15 minutos exactos para descargar por completo los capacitores y resetear la memoria de la tarjeta."
    ]
}

# Modelos oficiales registrados para ayuda visual
MODELOS_TALLER = [
    "LG WM4000HVA", "LG WM3600HWA", "LG WM3400CW", "LG WT7300CW", "LG WT8400CW",
    "WHIRLPOOL WFW5620HW", "WHIRLPOOL WTW5057LW", "WHIRLPOOL WTW4816FW",
    "SAMSUNG WF45T6000AW", "SAMSUNG WA50R5400AW", "MAYTAG MVW6200KW", "MAYTAG MVW7230HW",
    "GE APPLIANCES GFW850SSNWW", "GE APPLIANCES GTW465ASNWW",
    "SPEED QUEEN TC5003WN", "SPEED QUEEN TR7003WN"
]

# =========================================================================
# 2. PROCESADOR DE ENLACES EXTERNOS DE RESPALDO
# =========================================================================
def generar_enlaces_busqueda(modelo, error_falla):
    consulta_manual = f"{modelo} service manual filetype:pdf"
    consulta_error = f"{modelo} error {error_falla} repair"
    url_manual = "https://google.com" + urllib.parse.quote(consulta_manual)
    url_error = "https://google.com" + urllib.parse.quote(consulta_error)
    return url_manual, url_error

# =========================================================================
# 3. INTERFAZ GRÁFICA PROFESIONAL PARA DISPOSITIVOS MÓVILES
# =========================================================================
st.title("🧰 Sistema Experto de Reparación")
st.subheader("Base de Diagnóstico Avanzado para Técnicos")
st.write("---")

# FASE 1: CAPTURA DEL MODELO
modelo_usuario = st.text_input("👉 Ingrese el modelo del equipo (Ej: LG WM4000, Whirlpool WFW):").strip().upper()

if modelo_usuario:
    # Buscar aproximación del modelo
    coincidencias = difflib.get_close_matches(modelo_usuario, MODELOS_TALLER, n=1, cutoff=0.25)
    modelo_final = coincidencias[0] if coincidencias else modelo_usuario
    
    st.success(f"🤖 **Equipo configurado:** {modelo_final}")
    st.write("---")
    
    st.write("### 🔍 Buscador Inteligente de Síntomas y Códigos")
    falla_usuario = st.text_input("✍️ Describa la falla o el código de error (Ej: 'no drena', 'ruido', 'oe', 'f5e2'):").strip().lower()
    
    if falla_usuario:
        ruta_reparacion = None
        falla_detectada_nombre = ""
        
