# ============================================================
# CONFIGURACION.PY
# ============================================================
# Configuración centralizada para el proyecto de tesis.
# Contiene rutas, constantes, parámetros estadísticos y
# metadata del experimento.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

from pathlib import Path


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

# Ruta base del proyecto Tesis_Ordenada.
RUTA_BASE = Path(__file__).parent.parent.parent

# Rutas de datos.
RUTA_DATA = RUTA_BASE / "Data"
RUTA_DATA_CRUDOS = RUTA_DATA / "Datos_Crudos"
RUTA_DATA_PROCESADOS = RUTA_DATA / "Datos_Procesados"

# Rutas específicas de datos crudos por elección.
RUTA_DATOS_CRUDOS_GENERALES = RUTA_DATA_CRUDOS / "Generales"
RUTA_DATOS_CRUDOS_BALLOTAGE = RUTA_DATA_CRUDOS / "Ballotage"

# Rutas de salida de gráficos.
RUTA_GRAFICOS = RUTA_BASE / "Graficos"
RUTA_GRAFICOS_CLEVELAND = RUTA_GRAFICOS / "Cleveland"
RUTA_GRAFICOS_HEATMAPS = RUTA_GRAFICOS / "Heatmaps"
RUTA_GRAFICOS_VIOLIN = RUTA_GRAFICOS / "Violin"
RUTA_GRAFICOS_BARRAS = RUTA_GRAFICOS / "Barras"

# Rutas de salida de tablas.
RUTA_TABLAS = RUTA_BASE / "Tablas"
RUTA_TABLAS_TESTS = RUTA_TABLAS / "Resultados_Tests"
RUTA_TABLAS_SEM = RUTA_TABLAS / "Resultados_SEM"
RUTA_TABLAS_BASES = RUTA_TABLAS / "Bases_Procesadas"


# ============================================================
# CONSTANTES DEL EXPERIMENTO
# ============================================================

# Números de items IP utilizados en el experimento.
NUMEROS_ITEMS_IP = [
    3, 4, 5, 6, 7, 8, 9, 10, 11, 16,
    19, 20, 22, 23, 24, 25, 27, 28, 29, 30
]

# Items progresistas.
ITEMS_PROGRESISTAS = [3, 4, 5, 6, 7, 9, 10, 16, 22, 24]

# Items conservadores.
ITEMS_CONSERVADORES = [8, 11, 19, 20, 23, 25, 27, 28, 29, 30]


# ============================================================
# CATEGORIAS IDEOLOGICAS
# ============================================================

# Orden de categorías para visualizaciones.
ORDEN_CATEGORIAS = [
    'Left_Wing',
    'Progressivism',
    'Centre',
    'Moderate_Right_A',
    'Moderate_Right_B',
    'Right_Wing_Libertarian'
]

# Candidatos por categoría (PASO 2023).
CANDIDATOS_POR_CATEGORIA = {
    'Left_Wing': ['Myriam Bregman', 'Gabriel Solano'],
    'Progressivism': ['Sergio Massa', 'Juan Grabois'],
    'Centre': ['Juan Schiaretti'],
    'Moderate_Right_A': ['Horacio Rodríguez Larreta'],
    'Moderate_Right_B': ['Patricia Bullrich'],
    'Right_Wing_Libertarian': ['Javier Milei']
}

# Categorías de izquierda.
CATEGORIAS_IZQUIERDA = ['Left_Wing', 'Progressivism']

# Categorías de derecha.
CATEGORIAS_DERECHA = [
    'Moderate_Right_A',
    'Moderate_Right_B',
    'Right_Wing_Libertarian'
]

# Categorías a excluir de análisis.
CATEGORIAS_EXCLUIR = [
    'Other'
]


# ============================================================
# COLORES PARA VISUALIZACIONES
# ============================================================

COLORES_CATEGORIAS = {
    'Left_Wing': '#f65058',
    'Progressivism': '#0078bf',
    'Centre': '#009cdd',
    'Moderate_Right_A': '#f7d117',
    'Moderate_Right_B': '#f7d117',
    'Right_Wing_Libertarian': '#753bbd',
    'Blank': '#FFFFFF'
}


# ============================================================
# PARAMETROS ESTADISTICOS
# ============================================================

# Nivel de significancia estadística.
ALPHA = 0.05

# Número de desviaciones estándar para detección outliers.
NUM_DESVIACIONES_OUTLIERS = 3

# Método de test estadístico no paramétrico.
METODO_TEST = 'mannwhitneyu'

# Método de correlación.
METODO_CORRELACION = 'spearman'

# Número de primeros items a eliminar (warm-up).
NUM_PRIMEROS_ITEMS_ELIMINAR = 3


# ============================================================
# NOMBRES DE COLUMNAS ESTANDARIZADOS
# ============================================================

# Columnas de identificación.
COL_ID = 'ID'
COL_CATEGORIA = 'Categoria_PASO_2023'

# Columnas de índices calculados.
COL_INDICE_PROGRESISMO = 'Indice_Progresismo'
COL_INDICE_CONSERVADURISMO = 'Indice_Conservadurismo'
COL_INDICE_POSITIVIDAD = 'Indice_Positividad'

# Prefijos de columnas.
PREFIJO_IP_ITEM = 'IP_Item_'
PREFIJO_CO = 'CO_Item_'
PREFIJO_CT = 'CT_Item_'

# Sufijos de columnas.
SUFIJO_RESPUESTA = '_Respuesta'
SUFIJO_TIEMPO = '_Tiempo'
SUFIJO_CANDIDATO = '_Candidato'
SUFIJO_IZQ = '_Izq'
SUFIJO_DER = '_Der'


# ============================================================
# METADATA DE ITEMS IP
# ============================================================

DICCIONARIO_ITEMS_IP = {
    3: {
        'Numero_Item': 3,
        'Titulo': 'Aborto legal y seguro',
        'Tipo': 'Progresista',
        'Texto': (
            'El aborto legal, seguro y gratuito es un '
            'derecho fundamental de las mujeres.'
        )
    },
    4: {
        'Numero_Item': 4,
        'Titulo': 'Matrimonio igualitario',
        'Tipo': 'Progresista',
        'Texto': (
            'El matrimonio entre personas del mismo '
            'sexo debe ser reconocido legalmente.'
        )
    },
    5: {
        'Numero_Item': 5,
        'Titulo': 'Educación sexual integral',
        'Tipo': 'Progresista',
        'Texto': (
            'La educación sexual integral debe '
            'implementarse en todas las escuelas.'
        )
    },
    6: {
        'Numero_Item': 6,
        'Titulo': 'Impuesto a las grandes fortunas',
        'Tipo': 'Progresista',
        'Texto': (
            'Debe existir un impuesto especial a '
            'las grandes fortunas y patrimonios.'
        )
    },
    7: {
        'Numero_Item': 7,
        'Titulo': 'Intervención estatal en economía',
        'Tipo': 'Progresista',
        'Texto': (
            'El Estado debe intervenir activamente '
            'en la economía para garantizar justicia '
            'social.'
        )
    },
    8: {
        'Numero_Item': 8,
        'Titulo': 'Mano dura contra delincuencia',
        'Tipo': 'Conservador',
        'Texto': (
            'La seguridad requiere mano dura '
            'contra la delincuencia.'
        )
    },
    9: {
        'Numero_Item': 9,
        'Titulo': 'Protección de minorías',
        'Tipo': 'Progresista',
        'Texto': (
            'Es necesario implementar políticas '
            'de protección de minorías.'
        )
    },
    10: {
        'Numero_Item': 10,
        'Titulo': 'Cambio climático urgente',
        'Tipo': 'Progresista',
        'Texto': (
            'El cambio climático requiere '
            'acción inmediata del gobierno.'
        )
    },
    11: {
        'Numero_Item': 11,
        'Titulo': 'Valores tradicionales familiares',
        'Tipo': 'Conservador',
        'Texto': (
            'Los valores tradicionales de la '
            'familia deben ser preservados.'
        )
    },
    16: {
        'Numero_Item': 16,
        'Titulo': 'Legalización de drogas blandas',
        'Tipo': 'Progresista',
        'Texto': (
            'Debería legalizarse el consumo '
            'de marihuana.'
        )
    },
    19: {
        'Numero_Item': 19,
        'Titulo': 'Libre mercado sin regulación',
        'Tipo': 'Conservador',
        'Texto': (
            'El libre mercado debe funcionar '
            'sin regulación estatal.'
        )
    },
    20: {
        'Numero_Item': 20,
        'Titulo': 'Reducción del gasto público',
        'Tipo': 'Conservador',
        'Texto': (
            'Es necesario reducir drásticamente '
            'el gasto público.'
        )
    },
    22: {
        'Numero_Item': 22,
        'Titulo': 'Redistribución de la riqueza',
        'Tipo': 'Progresista',
        'Texto': (
            'La redistribución de la riqueza '
            'es esencial para la justicia.'
        )
    },
    23: {
        'Numero_Item': 23,
        'Titulo': 'Autoridad y orden',
        'Tipo': 'Conservador',
        'Texto': (
            'La autoridad y el orden deben '
            'prevalecer sobre las libertades '
            'individuales.'
        )
    },
    24: {
        'Numero_Item': 24,
        'Titulo': 'Derechos LGBTQ+',
        'Tipo': 'Progresista',
        'Texto': (
            'Los derechos de las personas LGBTQ+ '
            'deben ser ampliamente protegidos.'
        )
    },
    25: {
        'Numero_Item': 25,
        'Titulo': 'Privatización de empresas',
        'Tipo': 'Conservador',
        'Texto': (
            'Las empresas estatales deberían '
            'privatizarse.'
        )
    },
    27: {
        'Numero_Item': 27,
        'Titulo': 'Religión en educación',
        'Tipo': 'Conservador',
        'Texto': (
            'La religión debe tener un lugar '
            'en la educación pública.'
        )
    },
    28: {
        'Numero_Item': 28,
        'Titulo': 'Límites a inmigración',
        'Tipo': 'Conservador',
        'Texto': (
            'Debe limitarse la inmigración '
            'para proteger los empleos nacionales.'
        )
    },
    29: {
        'Numero_Item': 29,
        'Titulo': 'Portación de armas',
        'Tipo': 'Conservador',
        'Texto': (
            'Los ciudadanos deberían tener '
            'derecho a portar armas.'
        )
    },
    30: {
        'Numero_Item': 30,
        'Titulo': 'Pena de muerte',
        'Tipo': 'Conservador',
        'Texto': (
            'La pena de muerte debería aplicarse '
            'en casos extremos.'
        )
    }
}


# ============================================================
# CONFIGURACION DE FORMATOS DE SALIDA
# ============================================================

# Formatos de gráficos a generar.
FORMATOS_GRAFICOS = ['png', 'svg']

# DPI para exportación de gráficos.
DPI_GRAFICOS = 300

# Formato de exportación de tablas.
FORMATO_TABLAS = 'xlsx'


# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def Crear_Carpetas_Salida():

    """
    Crea todas las carpetas de salida necesarias si no existen.

    """

    Carpetas = [
        RUTA_GRAFICOS_CLEVELAND,
        RUTA_GRAFICOS_HEATMAPS,
        RUTA_GRAFICOS_VIOLIN,
        RUTA_GRAFICOS_BARRAS,
        RUTA_TABLAS_TESTS,
        RUTA_TABLAS_SEM,
        RUTA_TABLAS_BASES,
        RUTA_DATA_PROCESADOS
    ]

    for Carpeta in Carpetas:
        Carpeta.mkdir(parents=True, exist_ok=True)


def Obtener_Tipo_Item(Numero_Item: int) -> str:

    """
    Obtiene el tipo de item dado su número.

    Parámetros:
    - Numero_Item: Número del item IP.

    Retorna:
    - Tipo del item ('Progresista' o 'Conservador').

    """

    if Numero_Item in ITEMS_PROGRESISTAS:
        return 'Progresista'
    elif Numero_Item in ITEMS_CONSERVADORES:
        return 'Conservador'
    else:
        return 'Desconocido'


def Obtener_Color_Categoria(Categoria: str) -> str:

    """
    Obtiene el color asignado a una categoría ideológica.

    Parámetros:
    - Categoria: Nombre de la categoría.

    Retorna:
    - Código de color hexadecimal.

    """

    return COLORES_CATEGORIAS.get(Categoria, '#999999')
