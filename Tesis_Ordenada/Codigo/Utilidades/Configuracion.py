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

# Items progresistas (clasificación del notebook original).
ITEMS_PROGRESISTAS = [5, 6, 9, 11, 16, 20, 24, 25, 27, 28]

# Items conservadores (clasificación del notebook original).
ITEMS_CONSERVADORES = [3, 4, 7, 8, 10, 19, 22, 23, 29, 30]


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
        'Titulo': 'Aborto como crimen',
        'Tipo': 'Conservador',
        'Texto': (
            'El aborto es un crimen y debe ser perseguido y '
            'penado por la justicia en todas las circunstancias.'
        )
    },
    4: {
        'Numero_Item': 4,
        'Titulo': 'Homosexuales en educación',
        'Tipo': 'Conservador',
        'Texto': (
            'La ley no debería permitir a personas homosexuales '
            'dar clases en las escuelas.'
        )
    },
    5: {
        'Numero_Item': 5,
        'Titulo': 'Consultas populares vinculantes',
        'Tipo': 'Progresista',
        'Texto': (
            'El Estado debería hacer consultas populares vinculantes '
            'antes de tomar grandes decisiones para el destino del país.'
        )
    },
    6: {
        'Numero_Item': 6,
        'Titulo': 'Sistema público de jubilaciones',
        'Tipo': 'Progresista',
        'Texto': (
            'El Estado debería preservar el sistema de fondos de '
            'pensiones (jubilaciones) como un sistema eminentemente público.'
        )
    },
    7: {
        'Numero_Item': 7,
        'Titulo': 'Gobierno militar vs democrático',
        'Tipo': 'Conservador',
        'Texto': (
            'A veces un gobierno militar puede ser preferible '
            'a uno democrático.'
        )
    },
    8: {
        'Numero_Item': 8,
        'Titulo': 'Educación sexual sólo por padres',
        'Tipo': 'Conservador',
        'Texto': (
            'Sólo los padres tienen derecho a enseñar a sus hijos temas '
            'relacionados con la sexualidad; el colegio no debería intervenir '
            'en estas cuestiones.'
        )
    },
    9: {
        'Numero_Item': 9,
        'Titulo': 'Servicios públicos esenciales estatales',
        'Tipo': 'Progresista',
        'Texto': (
            'Los servicios públicos esenciales (agua, luz, gas) deberían '
            'ser propiedad del Estado.'
        )
    },
    10: {
        'Numero_Item': 10,
        'Titulo': 'Más policías vs otras áreas',
        'Tipo': 'Conservador',
        'Texto': (
            'El Estado debería asegurar más policías en la calle para el '
            'control del crimen y la delincuencia, aún si para ello fuera '
            'necesario recortar el presupuesto de otras áreas importantes '
            'como trabajo, salud y educación.'
        )
    },
    11: {
        'Numero_Item': 11,
        'Titulo': 'Campañas consumo responsable marihuana',
        'Tipo': 'Progresista',
        'Texto': (
            'El Estado debería promover campañas de concientización '
            'sobre el consumo responsable de sustancias como la marihuana.'
        )
    },
    16: {
        'Numero_Item': 16,
        'Titulo': 'Tierras a comunidades indígenas',
        'Tipo': 'Progresista',
        'Texto': (
            'El Estado debería otorgarle tierras a las comunidades indígenas '
            'que habitan en el país para que puedan autogobernarse.'
        )
    },
    19: {
        'Numero_Item': 19,
        'Titulo': 'Educación sexual es peligrosa',
        'Tipo': 'Conservador',
        'Texto': (
            'La educación sexual en jóvenes es peligrosa porque los motiva '
            'a una iniciación sexual temprana.'
        )
    },
    20: {
        'Numero_Item': 20,
        'Titulo': 'Ingreso mínimo para niños',
        'Tipo': 'Progresista',
        'Texto': (
            'El Estado debería garantizar un ingreso mínimo a todos los niños '
            'sin importar la situación laboral de sus padres.'
        )
    },
    22: {
        'Numero_Item': 22,
        'Titulo': 'Estado sostiene a Iglesia Católica',
        'Tipo': 'Conservador',
        'Texto': (
            'Está bien que el Estado sostenga económicamente '
            'a la Iglesia Católica.'
        )
    },
    23: {
        'Numero_Item': 23,
        'Titulo': 'Límites a inmigración por crisis',
        'Tipo': 'Conservador',
        'Texto': (
            'Ante la crisis económica, nuestro país debería ser menos permisivo '
            'con el ingreso de inmigrantes que compiten con los ciudadanos '
            'locales en la búsqueda de trabajo y mejores condiciones de vida.'
        )
    },
    24: {
        'Numero_Item': 24,
        'Titulo': 'Piquetes y cortes de ruta',
        'Tipo': 'Progresista',
        'Texto': (
            'Está bien que desocupados y vecinos realicen piquetes y cortes '
            'de calles o rutas, ya que es la única manera que tienen para '
            'presionar y lograr que sus reclamos sean atendidos por los gobiernos.'
        )
    },
    25: {
        'Numero_Item': 25,
        'Titulo': 'Evitar concentración de medios',
        'Tipo': 'Progresista',
        'Texto': (
            'El Estado debería hacer lo posible por evitar la concentración '
            'de medios de comunicación en pocas manos, y asegurar así la '
            'pluralidad de expresión.'
        )
    },
    27: {
        'Numero_Item': 27,
        'Titulo': 'Gasto en asistencia social',
        'Tipo': 'Progresista',
        'Texto': (
            'Cuando hay crisis económica, el Estado debería aumentar el gasto '
            'en programas de asistencia social y subsidios (como el programa '
            'nacional "jefas y jefes de hogar").'
        )
    },
    28: {
        'Numero_Item': 28,
        'Titulo': 'Propiedad de quien trabaja tierra',
        'Tipo': 'Progresista',
        'Texto': (
            'La propiedad de la tierra debe ser de quien la trabaje.'
        )
    },
    29: {
        'Numero_Item': 29,
        'Titulo': 'Privatización de empresas públicas',
        'Tipo': 'Conservador',
        'Texto': (
            'El Estado debería privatizar todas las empresas '
            'públicas ineficientes.'
        )
    },
    30: {
        'Numero_Item': 30,
        'Titulo': 'Medios estatales sin propaganda',
        'Tipo': 'Conservador',
        'Texto': (
            'No deberían utilizarse los medios de comunicación estatal '
            'para publicidad oficial o propaganda gubernamental.'
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
