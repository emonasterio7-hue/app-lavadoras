import difflib
import sys

# =========================================================================
# 1. BASE DE DATOS MAESTRA: MODELOS Y ERRORES ESPECÍFICOS (MECÁNICOS Y ELÉCTRICOS)
# =========================================================================
base_datos = {
    "modelos": [
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
    ],
    "errores_por_marca": {
        "LG": {
            "oe (no tira agua / falla de drenaje)": [
                "PASO 1: Limpiar el filtro de la bomba de drenaje en la esquina inferior frontal izquierda.",
                "PASO 2: Verificar que la manguera de desagüe trasera no esté obstruida o doblada.",
                "PASO 3: Medir con multímetro si llegan 120V a la bomba. Si llega voltaje y no drena, reemplazar bomba.",
            ],
            "ie (no entra agua / falla eléctrica de válvula)": [
                "PASO 1: Cerrar llaves de paso y limpiar los filtros de malla de las electroválvulas traseras.",
                "PASO 2: Comprobar la continuidad de las bobinas de las electroválvulas con el multímetro.",
                "PASO 3: Verificar que la presión del agua del hogar sea adecuada (mínimo 20 PSI).",
            ],
            "le (sobrecarga del motor / corto en sensor hall)": [
                "PASO 1: Desconectar por 10 minutos para reiniciar el módulo inverter de la tarjeta.",
                "PASO 2: Retirar la tapa trasera y girar la tina a mano para descartar ropa atorada entre las tinas.",
                "PASO 3: Revisar el arnés eléctrico y medir la resistencia del Sensor Hall en el estator (debe dar entre 5k y 15k ohms).",
            ],
            "ue (carga desbalanceada o amortiguador roto)": [
                "PASO 1: Abrir la puerta y redistribuir la carga de ropa pesada (cobijas o jeans).",
                "PASO 2: Comprobar con un nivel de burbuja que las patas de la lavadora estén perfectamente firmes.",
                "PASO 3: Inspeccionar los amortiguadores inferiores buscando pérdida de grasa o resortes vencidos.",
            ],
            "de o de1 (error de puerta abierta / blocapuertas)": [
                "PASO 1: Limpiar el pestillo y verificar la alineación mecánica del gancho de la puerta.",
                "PASO 2: Desmontar el interruptor de bloqueo (Door Lock Switch) y medir continuidad.",
                "PASO 3: Reemplazar el interruptor de puerta si no manda la señal de cierre a la placa principal.",
            ],
        },
        "SAMSUNG": {
            "4c o 4e (no entra agua / falla de solenoide)": [
                "PASO 1: Revisar que las llaves de agua estén completamente abiertas.",
                "PASO 2: Limpiar los filtros de malla plástica en las válvulas de entrada de agua.",
                "PASO 3: Comprobar si el cableado hacia el presostato o hacia las electroválvulas está sulfatado.",
            ],
            "5c o 5e (error de drenaje / bomba bloqueada)": [
                "PASO 1: Desmontar la manguera de desagüe trasera y limpiar obstrucciones (monedas comunes).",
                "PASO 2: Acceder a la bomba de drenaje por el frente/abajo y retirar residuos atrapados en el propulsor.",
                "PASO 3: Reemplazar la bomba de drenaje si el motor eléctrico interno se encuentra en corto.",
            ],
            "ub o dc (carga desbalanceada / varillas de suspension)": [
                "PASO 1: Asegurarse de que la lavadora no esté sobrecargada de ropa mojada.",
                "PASO 2: En modelos de carga superior, revisar las 4 varillas de suspensión trasera (amortiguadores).",
                "PASO 3: Calibrar la lavadora desde el menú digital ingresando al modo de servicio.",
            ],
            "3c o 3e (falla del motor inverter o corto en ipm)": [
                "PASO 1: Desconectar el equipo de la pared por 5 minutos para reiniciar la tarjeta de potencia (IPM).",
                "PASO 2: Medir la resistencia en los tres terminales del motor Direct Drive (deben marcar valores idénticos).",
                "PASO 3: Si el motor mide bien, la falla se encuentra en los transistores quemados de la tarjeta principal.",
            ],
        },
        "WHIRLPOOL": {
            "f5e2 (error de seguro de tapa / lid lock)": [
                "PASO 1: Revisar si el actuador o pasador del blocapuertas superior está roto o bloqueado por suciedad.",
                "PASO 2: Comprobar el solenoide del pestillo con multímetro en escala de continuidad.",
                "PASO 3: Reemplazar el ensamble del interruptor de tapa (Lid Lock Switch).",
            ],
            "f7e1 (error de sensor de velocidad / actuador de cambio)": [
                "PASO 1: Común en carga superior. Voltear la lavadora y ubicar el actuador de cambio (Shift Actuator).",
                "PASO 2: Limpiar el lente óptico del sensor del actuador que lee la polea inferior.",
                "PASO 3: Reemplazar el actuador de cambio si la lavadora no realiza la transición de lavado a exprimido.",
            ],
            "f8e1 (no llena agua / llenado lento)": [
                "PASO 1: Validar que las mangueras de agua fría y caliente no estén invertidas o dobladas.",
                "PASO 2: Limpiar sedimentos de las válvulas de entrada traseras.",
                "PASO 3: Probar los solenoides de las electroválvulas con escala de ohms.",
            ],
        },
        "MAYTAG": {
            "f5e1 (tapa abierta o switch dañado)": [
                "PASO 1: Verificar que la tapa cierre completamente sin golpear el panel de control.",
                "PASO 2: Desmontar el interruptor de bloqueo bajo la cubierta superior y probar su continuidad.",
            ],
            "f7e7 (falla de posicion del motor / correa floja)": [
                "PASO 1: Revisar si la banda de transmisión inferior se encuentra floja, rota o desgastada.",
                "PASO 2: Inspeccionar las conexiones del cableado del motor hacia la tarjeta principal.",
            ],
        },
        "GE": {
            "h2o o ih (falta de agua / electrovalvula muerta)": [
                "PASO 1: Verificar el suministro de agua del hogar y llaves de paso.",
                "PASO 2: Limpiar los filtros de malla en las entradas de agua traseras y medir voltaje en cables.",
            ],
            "not drained / no drena (filtro bloqueado)": [
                "PASO 1: Limpiar el filtro atrapapelusas integrado de la bomba en el fondo de la tina.",
                "PASO 2: Revisar voltaje de alimentación (120V) de la bomba de drenaje durante el ciclo.",
            ],
        },
    },
}

modelos = base_datos["modelos"]
errores_marcas = base_datos["errores_por_marca"]


# =========================================================================
# 2. FUNCIONES DE COMPARACIÓN Y DETECCIÓN INTELIGENTE
# =========================================================================
def buscar_coincidencia(texto, lista):
    """Analiza el texto escrito por el usuario y busca la opción más parecida."""
    coincidencias = difflib.get_close_matches(
        texto.upper(), [op.upper() for op in lista], n=1, cutoff=0.28
    )
    return coincidencias if coincidencias else None


def buscar_error_inteligente(entrada_usuario, diccionario_errores):
    """Busca el error primero por coincidencia exacta de caracteres iniciales

    y luego usa difflib si no encuentra nada directo.
    """
    entrada_limpia = entrada_usuario.strip().lower()

    # Estrategia 1: Ver si el texto del usuario está al principio de la clave (Ej: 'oe' está en 'oe (no tira agua...)')
    for clave_error in diccionario_errores.keys():
        if clave_error.startswith(entrada_limpia):
            return clave_error

    # Estrategia 2: Si no coincidió directo, usar el comparador flexible
    coincidencia = buscar_coincidencia(entrada_limpia, list(diccionario_errores.keys()))
    if coincidencia:
        return coincidencia.lower()

    return None


def detectar_marca(modelo):
    """Detecta automáticamente la marca de la lavadora por sus iniciales."""
    modelo_up = modelo.upper()
    if modelo_up.startswith("LG"):
        return "LG"
    elif modelo_up.startswith("SAMSUNG"):
        return "SAMSUNG"
    elif modelo_up.startswith("WHIRLPOOL"):
        return "WHIRLPOOL"
    elif modelo_up.startswith("MAYTAG"):
        return "MAYTAG"
    elif modelo_up.startswith("GE") or "GENERAL" in modelo_up:
        return "GE"
    return "WHIRLPOOL"


# =========================================================================
# 3. FLUJO PRINCIPAL DE EJECUCIÓN (SECUENCIAL DIRECTO)
# =========================================================================
print("=" * 72)
print(" 🧺 SISTEMA DE REPARACIÓN ASISTIDA POR CÓDIGO DE ERROR (2020-2026) 🧺")
print("=" * 72)

# FASE 1: INGRESO DEL MODELO
modelo_usuario = (
    input("👉 Ingrese el modelo de la lavadora (Ej: LG WM4000): ").strip().upper()
)

if not modelo_usuario:
    print("❌ No ingresó información del equipo. Programa cerrado.")
    sys.exit()

modelo_verificado = buscar_coincidencia(modelo_usuario, modelos)

if not modelo_verificado:
    print(f"\n⚠️ El modelo '{modelo_usuario}' no está precargado en el sistema.")
    opcion = (
        input("¿Desea forzar el sistema de diagnóstico para este modelo? (S/N): ")
        .strip()
        .lower()
    )
    if opcion == "s":
        nombre_modelo = modelo_usuario
    else:
        print("❌ Operación cancelada.")
        sys.exit()
else:
    nombre_modelo = modelo_verificado[0] if isinstance(modelo_verificado, list) else modelo_verificado
    print(f"✅ MODELO RECONOCIDO: [{nombre_modelo}]")

