# ============================================================
# ORDENAMIENTO_COLUMNAS.PY
# ============================================================
# Ordenamiento de columnas en grupos temáticos y lógicos.
# Establece estructura estandarizada: demográficos, políticos,
# electorales, items IP, variables calculadas y control.
# También aplica renombramientos de prefijos para redes
# sociales y medios de prensa.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from typing import Dict, List


# ============================================================
# CONSTANTES - ORDEN DE COLUMNAS
# ============================================================

# Orden estándar de columnas para análisis.
ORDEN_COLUMNAS_ESTANDAR = [

    'ID',

    # ============================================================
    # DEMOGRÁFICOS
    # ============================================================

    # Edad.
    'Edad',
    'Edad_Agrupada',
    'Edad_Agrupada_0_18',
    'Edad_Agrupada_19_35',
    'Edad_Agrupada_36_50',
    'Edad_Agrupada_51_70',
    'Edad_Agrupada_71_100',

    # Género.
    'Genero',
    'Genero_Femenino',
    'Genero_Masculino',
    'Genero_Otro',

    # Estrato social.
    'Estrato_Social',
    'Estrato_Social_Alto',
    'Estrato_Social_Bajo',
    'Estrato_Social_Bajo_Medio',
    'Estrato_Social_Medio',
    'Estrato_Social_Medio_Alto',

    # Nivel educativo.
    'Nivel_Educativo',
    'Nivel_Educativo_Primario',
    'Nivel_Educativo_Secundario',
    'Nivel_Educativo_Terciario',
    'Nivel_Educativo_Universitario',
    'Nivel_Educativo_Posgrado',

    # Fuente de ingreso.
    'Fuente_Ingreso',
    'Fuente_Ingreso_Trabajo',
    'Fuente_Ingreso_Ama_De_Casa',
    'Fuente_Ingreso_Asistencia_Social',
    'Fuente_Ingreso_Beca',
    'Fuente_Ingreso_Desocupado',
    'Fuente_Ingreso_Emprendimiento',
    'Fuente_Ingreso_Empresa',
    'Fuente_Ingreso_Jubilacion',
    'Fuente_Ingreso_Pension',
    'Fuente_Ingreso_Renta',
    'Fuente_Ingreso_Sustento_Familiar',
    'Fuente_Ingreso_Otro',

    # Inmueble de residencia.
    'Inmueble_Residencia',
    'Inmueble_Residencia_Alquilo',
    'Inmueble_Residencia_Cedido',
    'Inmueble_Residencia_Familiar',
    'Inmueble_Residencia_Prestado',
    'Inmueble_Residencia_Propio',
    'Inmueble_Residencia_Otro',

    # Residencia.
    'Provincia',
    'Region',
    'Region_BsAs',
    'Region_CABA',
    'Region_Centro',
    'Region_Cuyo',
    'Region_Norte',
    'Region_Patagonia',

    # Datos demográficos básicos.
    'Nacionalidad',


    # ============================================================
    # ELECTORALES
    # ============================================================

    # Voto 2019.
    'Voto_2019',
    'Voto_2019_Alberto_Fernandez',
    'Voto_2019_JL_Espert',
    'Voto_2019_J_Gomez_Centurion',
    'Voto_2019_Mauricio_Macri',
    'Voto_2019_Nicolas_Del_Caño',
    'Voto_2019_Roberto_Lavagna',
    'Voto_2019_Voto_En_Blanco',
    'Voto_2019_No_Vote',
    'Voto_2019_Prefiero_No_Decirlo',

    # Voto PASO 2023.
    'Voto_PASO_2023',
    'Voto_PASO_2023_Si',
    'Voto_PASO_2023_No',
    'Voto_PASO_2023_Prefiero_No_Decirlo',

    # Candidato PASO 2023.
    'Candidato_PASO_2023',
    'Candidato_PASO_2023_Sergio_Massa',
    'Candidato_PASO_2023_Javier_Milei',
    'Candidato_PASO_2023_Myriam_Bregman',
    'Candidato_PASO_2023_Horacio_Rodriguez_Larreta',
    'Candidato_PASO_2023_Patricia_Bullrich',
    'Candidato_PASO_2023_Juan_Grabois',
    'Candidato_PASO_2023_Juan_Schiaretti',
    'Candidato_PASO_2023_Gabriel_Solano',
    'Candidato_PASO_2023_Guillermo_Moreno',
    'Candidato_PASO_2023_Jesus_Escobar',
    'Candidato_PASO_2023_Julio_Barbaro',
    'Candidato_PASO_2023_Manuela_Castañeira',
    'Candidato_PASO_2023_Marcelo_Ramal',
    'Candidato_PASO_2023_Mempo_Giardinelli',
    'Candidato_PASO_2023_Nazareno_Etchepare',
    'Candidato_PASO_2023_Santiago_Cuneo',
    'Candidato_PASO_2023_Blanco',
    'Candidato_PASO_2023_Prefiero_No_Decirlo',
    'Candidato_PASO_2023_No_Aplica',

    # Categoría PASO 2023.
    'Categoria_PASO_2023',
    'Categoria_PASO_2023_Blank',
    'Categoria_PASO_2023_Centre',
    'Categoria_PASO_2023_Left_Wing',
    'Categoria_PASO_2023_Moderate_Right_A',
    'Categoria_PASO_2023_Moderate_Right_B',
    'Categoria_PASO_2023_Progressivism',
    'Categoria_PASO_2023_Right_Wing_Libertarian',
    'Categoria_PASO_2023_Other',
    'Categoria_PASO_2023_No_Response',
    'Categoria_PASO_2023_No_Apply',

    # Votará 2023.
    'Votara_2023',
    'Votara_2023_Si',
    'Votara_2023_No',
    'Votara_2023_No_Sabe',


    # ============================================================
    # POLÍTICOS
    # ============================================================

    # Afiliación política.
    'Afiliacion_Politica',
    'Afiliacion_Politica_Si',
    'Afiliacion_Politica_No',

    # Autopercepciones.
    'Autopercepcion_Izq_Der',
    'Autopercepcion_Izq_Der_Agrupada',
    'Autopercepcion_Izq_Der_Agrupada_A',
    'Autopercepcion_Izq_Der_Agrupada_B',
    'Autopercepcion_Izq_Der_Agrupada_C',
    'Autopercepcion_Con_Pro',
    'Autopercepcion_Con_Pro_Agrupada',
    'Autopercepcion_Con_Pro_Agrupada_A',
    'Autopercepcion_Con_Pro_Agrupada_B',
    'Autopercepcion_Con_Pro_Agrupada_C',
    'Autopercepcion_Per_Antiper',
    'Autopercepcion_Per_Antiper_Agrupada',
    'Autopercepcion_Per_Antiper_Agrupada_A',
    'Autopercepcion_Per_Antiper_Agrupada_B',
    'Autopercepcion_Per_Antiper_Agrupada_C',

    # Cercanía con candidatos.
    'Cercania_Massa',
    'Cercania_Bullrich',
    'Cercania_Bregman',
    'Cercania_Milei',
    'Cercania_Schiaretti',

    # Redes sociales.
    'Influencia_Redes',
    'Red_Social',
    'Red_Social_Twitter',
    'Red_Social_Facebook',
    'Red_Social_Instagram',
    'Red_Social_Threads',
    'Red_Social_Tiktok',
    'Red_Social_Youtube',
    'Red_Social_Whatsapp',
    'Red_Social_Telegram',

    # Medios de prensa.
    'Influencia_Prensa',
    'Medios_Informacion',
    'Medios_Prensa',
    'Medios_Prensa_Ambito_Financiero',
    'Medios_Prensa_Prensa_Obrera',
    'Medios_Prensa_Diario_Universal',
    'Medios_Prensa_Popular',
    'Medios_Prensa_Izquierda_Diario',
    'Medios_Prensa_Clarin',
    'Medios_Prensa_Perfil',
    'Medios_Prensa_Pagina_12',
    'Medios_Prensa_Infobae',
    'Medios_Prensa_El_Cronista',
    'Medios_Prensa_La_Nacion',
    'Medios_Prensa_Tiempo_Argentino',
    'Medios_Prensa_Ninguno',


    # ============================================================
    # CLIMA ELECTORAL
    # ============================================================

    # Escala de conocimiento económico (ECE).
    'ECE_Item_1',
    'ECE_Item_2',
    'ECE_Item_3',
    'ECE_Item_4',
    'ECE_Item_5',
    'ECE_Item_6',
    'ECE_Item_7',
    'ECE_Item_5_Negativo',


    # ============================================================
    # CARACTERIZACIÓN DE CANDIDATOS
    # ============================================================

    # Candidatos con descripción - CDC.
    'CDC_Massa_0',
    'CDC_Massa_1',
    'CDC_Massa_Tiempo',
    'CDC_Bullrich_0',
    'CDC_Bullrich_1',
    'CDC_Bullrich_Tiempo',
    'CDC_Schiaretti_0',
    'CDC_Schiaretti_1',
    'CDC_Schiaretti_Tiempo',
    'CDC_Milei_0',
    'CDC_Milei_1',
    'CDC_Milei_Tiempo',
    'CDC_Bregman_0',
    'CDC_Bregman_1',
    'CDC_Bregman_Tiempo',


    # ============================================================
    # ITEMS SIN Y CON ASOCIACION
    # ============================================================

    # Items de personalidad implícita.
    'IP_Item_3_Respuesta',
    'IP_Item_3_Tiempo',
    'IP_Item_3_Izq_Candidato',
    'IP_Item_3_Izq_Respuesta',
    'IP_Item_3_Izq_Tiempo',
    'IP_Item_3_Der_Candidato',
    'IP_Item_3_Der_Respuesta',
    'IP_Item_3_Der_Tiempo',

    'IP_Item_4_Respuesta',
    'IP_Item_4_Tiempo',
    'IP_Item_4_Izq_Candidato',
    'IP_Item_4_Izq_Respuesta',
    'IP_Item_4_Izq_Tiempo',
    'IP_Item_4_Der_Candidato',
    'IP_Item_4_Der_Respuesta',
    'IP_Item_4_Der_Tiempo',

    'IP_Item_5_Respuesta',
    'IP_Item_5_Tiempo',
    'IP_Item_5_Izq_Candidato',
    'IP_Item_5_Izq_Respuesta',
    'IP_Item_5_Izq_Tiempo',
    'IP_Item_5_Der_Candidato',
    'IP_Item_5_Der_Respuesta',
    'IP_Item_5_Der_Tiempo',

    'IP_Item_6_Respuesta',
    'IP_Item_6_Tiempo',
    'IP_Item_6_Izq_Candidato',
    'IP_Item_6_Izq_Respuesta',
    'IP_Item_6_Izq_Tiempo',
    'IP_Item_6_Der_Candidato',
    'IP_Item_6_Der_Respuesta',
    'IP_Item_6_Der_Tiempo',

    'IP_Item_7_Respuesta',
    'IP_Item_7_Tiempo',
    'IP_Item_7_Izq_Candidato',
    'IP_Item_7_Izq_Respuesta',
    'IP_Item_7_Izq_Tiempo',
    'IP_Item_7_Der_Candidato',
    'IP_Item_7_Der_Respuesta',
    'IP_Item_7_Der_Tiempo',

    'IP_Item_8_Respuesta',
    'IP_Item_8_Tiempo',
    'IP_Item_8_Izq_Candidato',
    'IP_Item_8_Izq_Respuesta',
    'IP_Item_8_Izq_Tiempo',
    'IP_Item_8_Der_Candidato',
    'IP_Item_8_Der_Respuesta',
    'IP_Item_8_Der_Tiempo',

    'IP_Item_9_Respuesta',
    'IP_Item_9_Tiempo',
    'IP_Item_9_Izq_Candidato',
    'IP_Item_9_Izq_Respuesta',
    'IP_Item_9_Izq_Tiempo',
    'IP_Item_9_Der_Candidato',
    'IP_Item_9_Der_Respuesta',
    'IP_Item_9_Der_Tiempo',

    'IP_Item_10_Respuesta',
    'IP_Item_10_Tiempo',
    'IP_Item_10_Izq_Candidato',
    'IP_Item_10_Izq_Respuesta',
    'IP_Item_10_Izq_Tiempo',
    'IP_Item_10_Der_Candidato',
    'IP_Item_10_Der_Respuesta',
    'IP_Item_10_Der_Tiempo',

    'IP_Item_11_Respuesta',
    'IP_Item_11_Tiempo',
    'IP_Item_11_Izq_Candidato',
    'IP_Item_11_Izq_Respuesta',
    'IP_Item_11_Izq_Tiempo',
    'IP_Item_11_Der_Candidato',
    'IP_Item_11_Der_Respuesta',
    'IP_Item_11_Der_Tiempo',

    'IP_Item_16_Respuesta',
    'IP_Item_16_Tiempo',
    'IP_Item_16_Izq_Candidato',
    'IP_Item_16_Izq_Respuesta',
    'IP_Item_16_Izq_Tiempo',
    'IP_Item_16_Der_Candidato',
    'IP_Item_16_Der_Respuesta',
    'IP_Item_16_Der_Tiempo',

    'IP_Item_19_Respuesta',
    'IP_Item_19_Tiempo',
    'IP_Item_19_Izq_Candidato',
    'IP_Item_19_Izq_Respuesta',
    'IP_Item_19_Izq_Tiempo',
    'IP_Item_19_Der_Candidato',
    'IP_Item_19_Der_Respuesta',
    'IP_Item_19_Der_Tiempo',

    'IP_Item_20_Respuesta',
    'IP_Item_20_Tiempo',
    'IP_Item_20_Izq_Candidato',
    'IP_Item_20_Izq_Respuesta',
    'IP_Item_20_Izq_Tiempo',
    'IP_Item_20_Der_Candidato',
    'IP_Item_20_Der_Respuesta',
    'IP_Item_20_Der_Tiempo',

    'IP_Item_22_Respuesta',
    'IP_Item_22_Tiempo',
    'IP_Item_22_Izq_Candidato',
    'IP_Item_22_Izq_Respuesta',
    'IP_Item_22_Izq_Tiempo',
    'IP_Item_22_Der_Candidato',
    'IP_Item_22_Der_Respuesta',
    'IP_Item_22_Der_Tiempo',

    'IP_Item_23_Respuesta',
    'IP_Item_23_Tiempo',
    'IP_Item_23_Izq_Candidato',
    'IP_Item_23_Izq_Respuesta',
    'IP_Item_23_Izq_Tiempo',
    'IP_Item_23_Der_Candidato',
    'IP_Item_23_Der_Respuesta',
    'IP_Item_23_Der_Tiempo',

    'IP_Item_24_Respuesta',
    'IP_Item_24_Tiempo',
    'IP_Item_24_Izq_Candidato',
    'IP_Item_24_Izq_Respuesta',
    'IP_Item_24_Izq_Tiempo',
    'IP_Item_24_Der_Candidato',
    'IP_Item_24_Der_Respuesta',
    'IP_Item_24_Der_Tiempo',

    'IP_Item_25_Respuesta',
    'IP_Item_25_Tiempo',
    'IP_Item_25_Izq_Candidato',
    'IP_Item_25_Izq_Respuesta',
    'IP_Item_25_Izq_Tiempo',
    'IP_Item_25_Der_Candidato',
    'IP_Item_25_Der_Respuesta',
    'IP_Item_25_Der_Tiempo',

    'IP_Item_27_Respuesta',
    'IP_Item_27_Tiempo',
    'IP_Item_27_Izq_Candidato',
    'IP_Item_27_Izq_Respuesta',
    'IP_Item_27_Izq_Tiempo',
    'IP_Item_27_Der_Candidato',
    'IP_Item_27_Der_Respuesta',
    'IP_Item_27_Der_Tiempo',

    'IP_Item_28_Respuesta',
    'IP_Item_28_Tiempo',
    'IP_Item_28_Izq_Candidato',
    'IP_Item_28_Izq_Respuesta',
    'IP_Item_28_Izq_Tiempo',
    'IP_Item_28_Der_Candidato',
    'IP_Item_28_Der_Respuesta',
    'IP_Item_28_Der_Tiempo',

    'IP_Item_29_Respuesta',
    'IP_Item_29_Tiempo',
    'IP_Item_29_Izq_Candidato',
    'IP_Item_29_Izq_Respuesta',
    'IP_Item_29_Izq_Tiempo',
    'IP_Item_29_Der_Candidato',
    'IP_Item_29_Der_Respuesta',
    'IP_Item_29_Der_Tiempo',

    'IP_Item_30_Respuesta',
    'IP_Item_30_Tiempo',
    'IP_Item_30_Izq_Candidato',
    'IP_Item_30_Izq_Respuesta',
    'IP_Item_30_Izq_Tiempo',
    'IP_Item_30_Der_Candidato',
    'IP_Item_30_Der_Respuesta',
    'IP_Item_30_Der_Tiempo',


    # ============================================================
    # ORDEN DE IP ITEMS
    # ============================================================

    'Orden_IP_Items',
    'Ultimo_IP_Item',
    'Orden_IP_Items_Asociados',
    'Primeros_IP_Items_Asociados',
    'Ultimo_IP_Item_Asociado',


    # ============================================================
    # VARIABLES CALCULADAS
    # ============================================================

    'Indice_Positividad',
    'Indice_Progresismo',
    'Indice_Progresismo_Tiempo',
    'Indice_Conservadurismo',
    'Indice_Conservadurismo_Tiempo',

    # Tiempos de respuesta promedio.
    'Tiempos_Respuesta_Promedio_Pro_Izq',
    'Tiempos_Respuesta_Promedio_Pro_Der',
    'Tiempos_Respuesta_Promedio_Con_Izq',
    'Tiempos_Respuesta_Promedio_Con_Der',
    'Tiempos_Respuesta_Promedio_Pro',
    'Tiempos_Respuesta_Promedio_Con',


    # ============================================================
    # CONTROL
    # ============================================================

    'Sentimiento_Fase_Final',
    'Evento_Estresante',
    'Sabia_Del_Experimento',

    # Uso de sustancias.
    'Usa_Sustancias',
    'Tabaco',
    'Alcohol',
    'Marihuana',
    'Drogas_Recreativas',
    'Cual_Droga_Recreativa',
    'Medicamentos',
    'Cual_Medicamento',
    'Otras_Sustancias',

    # Sueño.
    'Horas_Sueno_Promedio',
    'Sueno_Noche_Anterior',
]


# Mapeo de renombramientos de redes sociales.
MAPEO_REDES_SOCIALES = {
    'Twitter': 'Red_Social_Twitter',
    'Facebook': 'Red_Social_Facebook',
    'Instagram': 'Red_Social_Instagram',
    'Threads': 'Red_Social_Threads',
    'Tiktok': 'Red_Social_Tiktok',
    'Youtube': 'Red_Social_Youtube',
    'Whatsapp': 'Red_Social_Whatsapp',
    'Telegram': 'Red_Social_Telegram'
}


# Mapeo de renombramientos de medios de prensa.
MAPEO_MEDIOS_PRENSA = {
    'Ambito_Financiero': 'Medios_Prensa_Ambito_Financiero',
    'Prensa_Obrera': 'Medios_Prensa_Prensa_Obrera',
    'Diario_Universal': 'Medios_Prensa_Diario_Universal',
    'Popular': 'Medios_Prensa_Popular',
    'Izquierda_Diario': 'Medios_Prensa_Izquierda_Diario',
    'Clarin': 'Medios_Prensa_Clarin',
    'Perfil': 'Medios_Prensa_Perfil',
    'Pagina_12': 'Medios_Prensa_Pagina_12',
    'Infobae': 'Medios_Prensa_Infobae',
    'El_Cronista': 'Medios_Prensa_El_Cronista',
    'La_Nacion': 'Medios_Prensa_La_Nacion',
    'Tiempo_Argentino': 'Medios_Prensa_Tiempo_Argentino'
}


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def Aplicar_Renombramientos(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Aplica renombramientos de prefijos a columnas de redes
    sociales y medios de prensa.

    Parámetros:
    - Df: DataFrame con columnas a renombrar.

    Retorna:
    - DataFrame con columnas renombradas.

    """

    print("\n" + "="*60)
    print("APLICACIÓN DE RENOMBRAMIENTOS")
    print("="*60)

    Df_Resultado = Df.copy()

    # Renombrar redes sociales.
    print("\nRenombrando redes sociales...")
    Redes_Renombradas = 0
    for Antiguo, Nuevo in MAPEO_REDES_SOCIALES.items():
        if Antiguo in Df_Resultado.columns:
            Df_Resultado.rename(
                columns={Antiguo: Nuevo},
                inplace=True
            )
            Redes_Renombradas += 1

    print(f"  ✓ {Redes_Renombradas} redes renombradas")

    # Renombrar medios de prensa.
    print("\nRenombrando medios de prensa...")
    Medios_Renombrados = 0
    for Antiguo, Nuevo in MAPEO_MEDIOS_PRENSA.items():
        if Antiguo in Df_Resultado.columns:
            Df_Resultado.rename(
                columns={Antiguo: Nuevo},
                inplace=True
            )
            Medios_Renombrados += 1

    print(f"  ✓ {Medios_Renombrados} medios renombrados")

    print("\n" + "="*60)
    print("✓ RENOMBRAMIENTOS COMPLETADOS")
    print("="*60)

    return Df_Resultado


def Ordenar_Columnas(
    Df: pd.DataFrame,
    Orden: List[str] = None
) -> pd.DataFrame:

    """
    Ordena columnas del DataFrame según lista especificada.

    Solo incluye columnas que existen en el DataFrame. Las
    columnas no especificadas en el orden se agregan al final.

    Parámetros:
    - Df: DataFrame a ordenar.
    - Orden: Lista de nombres de columnas en orden deseado.
      Si es None, usa ORDEN_COLUMNAS_ESTANDAR.

    Retorna:
    - DataFrame con columnas ordenadas.

    """

    print("\n" + "="*60)
    print("ORDENAMIENTO DE COLUMNAS")
    print("="*60)

    Df_Resultado = Df.copy()

    # Usar orden estándar si no se proporciona.
    if Orden is None:
        Orden = ORDEN_COLUMNAS_ESTANDAR

    print(f"\nColumnas en DataFrame: {len(Df_Resultado.columns)}")
    print(f"Columnas en orden de referencia: {len(Orden)}")

    # Filtrar columnas existentes según orden.
    Columnas_Existentes_Ordenadas = [
        Col for Col in Orden
        if Col in Df_Resultado.columns
    ]

    # Identificar columnas no especificadas en orden.
    Columnas_No_Especificadas = [
        Col for Col in Df_Resultado.columns
        if Col not in Orden
    ]

    print(f"\nColumnas ordenadas: {len(Columnas_Existentes_Ordenadas)}")
    print(f"Columnas no especificadas (irán al final): "
          f"{len(Columnas_No_Especificadas)}")

    if Columnas_No_Especificadas:
        print("\nColumnas no especificadas en orden:")
        for Col in Columnas_No_Especificadas[:10]:
            print(f"  - {Col}")
        if len(Columnas_No_Especificadas) > 10:
            print(f"  ... y {len(Columnas_No_Especificadas) - 10} "
                  f"más")

    # Combinar: ordenadas + no especificadas.
    Orden_Final = (
        Columnas_Existentes_Ordenadas +
        Columnas_No_Especificadas
    )

    # Reordenar DataFrame.
    Df_Resultado = Df_Resultado[Orden_Final]

    print(f"\n✓ DataFrame reordenado con {len(Orden_Final)} columnas")

    print("\n" + "="*60)
    print("✓ ORDENAMIENTO COMPLETADO")
    print("="*60)

    return Df_Resultado


def Aplicar_Ordenamiento_Completo(
    Df: pd.DataFrame,
    Orden: List[str] = None
) -> pd.DataFrame:

    """
    Aplica renombramientos y ordenamiento completo de
    columnas.

    Proceso:
    1. Renombrar redes sociales y medios de prensa.
    2. Ordenar columnas según lista estándar.

    Parámetros:
    - Df: DataFrame a procesar.
    - Orden: Lista de orden de columnas (opcional).

    Retorna:
    - DataFrame con columnas renombradas y ordenadas.

    """

    print("\n" + "="*60)
    print("ORDENAMIENTO COMPLETO")
    print("="*60)

    # Paso 1: Renombramientos.
    Df_Resultado = Aplicar_Renombramientos(Df)

    # Paso 2: Ordenamiento.
    Df_Resultado = Ordenar_Columnas(Df_Resultado, Orden)

    print("\n" + "="*60)
    print("✓ ORDENAMIENTO COMPLETO FINALIZADO")
    print("="*60)

    return Df_Resultado


def Aplicar_Ordenamiento_Diccionario(
    Diccionario_Dfs: Dict[str, pd.DataFrame],
    Orden: List[str] = None
) -> Dict[str, pd.DataFrame]:

    """
    Aplica ordenamiento completo a un diccionario de
    DataFrames.

    Parámetros:
    - Diccionario_Dfs: Dict con DataFrames.
    - Orden: Lista de orden de columnas (opcional).

    Retorna:
    - Diccionario con DataFrames procesados.

    """

    Diccionario_Resultado = {}

    for Nombre, Df in Diccionario_Dfs.items():
        print(f"\n{'='*70}")
        print(f"PROCESANDO: {Nombre}")
        print(f"{'='*70}")

        Diccionario_Resultado[Nombre] = (
            Aplicar_Ordenamiento_Completo(Df, Orden)
        )

    return Diccionario_Resultado


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Este módulo debe ser importado, no ejecutado "
          "directamente.")
    print("Uso:")
    print("  from Ordenamiento_Columnas import "
          "Aplicar_Ordenamiento_Completo")
    print("  Df = Aplicar_Ordenamiento_Completo(Df)")
