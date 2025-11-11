# ============================================================
# AGRUPAMIENTO_VARIABLES.PY
# ============================================================
# Agrupamiento y normalización de variables categóricas y
# sociodemográficas. Aplica transformaciones configurables
# para consolidar categorías dispersas en grupos coherentes.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
import unidecode
from typing import Dict, List, Tuple, Union, Any


# ============================================================
# CONSTANTES - MAPEOS DE AGRUPAMIENTO
# ============================================================

# Mapeo de provincias a regiones geográficas.
MAPEO_PROVINCIAS = {
    'buenos aires': 'BsAs',
    'ciudad autonoma de buenos aires': 'CABA',
    'caba': 'CABA',
    'catamarca': 'Norte',
    'chaco': 'Norte',
    'chubut': 'Patagonia',
    'cordoba': 'Centro',
    'corrientes': 'Norte',
    'entre rios': 'Centro',
    'formosa': 'Norte',
    'jujuy': 'Norte',
    'la pampa': 'Centro',
    'la rioja': 'Cuyo',
    'mendoza': 'Cuyo',
    'misiones': 'Norte',
    'neuquen': 'Patagonia',
    'rio negro': 'Patagonia',
    'salta': 'Norte',
    'san juan': 'Cuyo',
    'san luis': 'Cuyo',
    'santa cruz': 'Patagonia',
    'santa fe': 'Centro',
    'santiago del estero': 'Norte',
    'tierra del fuego': 'Patagonia',
    'tucuman': 'Norte'
}

# Rangos de edad para agrupamiento.
RANGOS_EDAD = [0, 25, 35, 45, 55, 120]
ETIQUETAS_EDAD = [
    'Menos_25',
    'Entre_25_Y_34',
    'Entre_35_Y_44',
    'Entre_45_Y_54',
    'Mayor_55'
]

# Mapeo de género normalizado.
MAPEO_GENERO = {
    'femenino': 'Femenino',
    'masculino': 'Masculino',
    'otro': 'Otro',
    'hombre': 'Masculino',
    'mujer': 'Femenino',
    'varon': 'Masculino',
    'f': 'Femenino',
    'm': 'Masculino',
    'x': 'Otro',
    'no binario': 'Otro'
}

# Mapeo de tipo de inmueble de residencia.
MAPEO_INMUEBLE = {
    'casa': 'Casa',
    'departamento': 'Departamento',
    'casa de mi propiedad': 'Casa',
    'casa en alquiler': 'Casa',
    'departamento de mi propiedad': 'Departamento',
    'departamento en alquiler': 'Departamento',
    'casa familiar': 'Casa',
    'depto': 'Departamento',
    'vivienda social': 'Vivienda_Social',
    'casa compartida': 'Casa',
    'departamento compartido': 'Departamento',
    'pension': 'Pension',
    'hotel': 'Pension',
    'habitacion': 'Pension',
    'casa de familia': 'Casa',
    'casa propia': 'Casa',
    'casa alquilada': 'Casa',
    'departamento propio': 'Departamento',
    'departamento alquilado': 'Departamento',
    'otro': 'Otro'
}

# Mapeo de fuentes de ingreso principal.
MAPEO_FUENTE_INGRESO = {
    'trabajo en relacion de dependencia': 'Relacion_Dependencia',
    'trabajo independiente': 'Independiente',
    'jubilacion': 'Jubilacion',
    'pension': 'Jubilacion',
    'desempleo': 'Desempleado',
    'sin ingresos': 'Desempleado',
    'changas': 'Changas',
    'trabajo informal': 'Changas',
    'ayuda familiar': 'Ayuda_Familiar',
    'ayuda social': 'Ayuda_Social',
    'plan social': 'Ayuda_Social',
    'beca': 'Beca',
    'alquiler': 'Rentas',
    'rentas': 'Rentas',
    'inversion': 'Rentas',
    'inversiones': 'Rentas',
    'empleado': 'Relacion_Dependencia',
    'empleada': 'Relacion_Dependencia',
    'monotributista': 'Independiente',
    'autonomo': 'Independiente',
    'cuentapropista': 'Independiente',
    'jubilado': 'Jubilacion',
    'pensionado': 'Jubilacion',
    'desocupado': 'Desempleado',
    'ninguno': 'Desempleado',
    'no trabajo': 'Desempleado',
    'changa': 'Changas',
    'trabajos ocasionales': 'Changas',
    'familia': 'Ayuda_Familiar',
    'padres': 'Ayuda_Familiar',
    'pareja': 'Ayuda_Familiar',
    'auh': 'Ayuda_Social',
    'asignacion': 'Ayuda_Social',
    'subsidio': 'Ayuda_Social',
    'becado': 'Beca',
    'estudiante': 'Beca',
    'otro': 'Otro'
}

# Mapeo de nivel educativo.
MAPEO_NIVEL_EDUCATIVO = {
    'primario incompleto': 'Primario',
    'primario completo': 'Primario',
    'secundario incompleto': 'Secundario',
    'secundario completo': 'Secundario',
    'terciario incompleto': 'Terciario',
    'terciario completo': 'Terciario',
    'universitario incompleto': 'Universitario',
    'universitario completo': 'Universitario',
    'posgrado': 'Posgrado',
    'sin estudios': 'Sin_Estudios',
    'primaria incompleta': 'Primario',
    'primaria completa': 'Primario',
    'secundaria incompleta': 'Secundario',
    'secundaria completa': 'Secundario',
    'terciaria incompleta': 'Terciario',
    'terciaria completa': 'Terciario',
    'universidad incompleta': 'Universitario',
    'universidad completa': 'Universitario',
    'master': 'Posgrado',
    'doctorado': 'Posgrado',
    'ninguno': 'Sin_Estudios'
}

# Mapeo de situación laboral.
MAPEO_SITUACION_LABORAL = {
    'empleado tiempo completo': 'Empleado_Completo',
    'empleado tiempo parcial': 'Empleado_Parcial',
    'desempleado': 'Desempleado',
    'jubilado': 'Jubilado',
    'estudiante': 'Estudiante',
    'autonomo': 'Autonomo',
    'ama de casa': 'Hogar',
    'empleada tiempo completo': 'Empleado_Completo',
    'empleada tiempo parcial': 'Empleado_Parcial',
    'desempleada': 'Desempleado',
    'jubilada': 'Jubilado',
    'autonoma': 'Autonomo',
    'cuentapropista': 'Autonomo',
    'monotributista': 'Autonomo',
    'freelance': 'Autonomo',
    'no trabajo': 'Desempleado',
    'sin empleo': 'Desempleado',
    'pensionado': 'Jubilado',
    'pensionada': 'Jubilado',
    'otro': 'Otro'
}

# Mapeo de estado civil.
MAPEO_ESTADO_CIVIL = {
    'soltero': 'Soltero',
    'casado': 'Casado',
    'divorciado': 'Divorciado',
    'viudo': 'Viudo',
    'en pareja': 'En_Pareja',
    'soltera': 'Soltero',
    'casada': 'Casado',
    'divorciada': 'Divorciado',
    'viuda': 'Viudo',
    'union de hecho': 'En_Pareja',
    'conviviente': 'En_Pareja',
    'separado': 'Divorciado',
    'separada': 'Divorciado',
    'concubinato': 'En_Pareja',
    'otro': 'Otro'
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def Normalizar_Texto(
    Valor: Any
) -> str:

    """
    Normaliza texto para comparación: minúsculas y sin
    acentos.

    Parámetros:
    - Valor: Valor a normalizar (puede ser str, int, float,
      etc.).

    Retorna:
    - Texto normalizado en minúsculas sin acentos.

    """

    if pd.isna(Valor):
        return ''

    Texto = str(Valor).strip()
    Texto_Normalizado = unidecode.unidecode(Texto).lower()

    return Texto_Normalizado


def Aplicar_Mapeo_Diccionario(
    Df: pd.DataFrame,
    Columna_Origen: str,
    Columna_Destino: str,
    Diccionario_Mapeo: Dict[str, str],
    Normalizar: bool = True,
    Valor_Default: str = 'Otro'
) -> pd.DataFrame:

    """
    Aplica mapeo de diccionario a una columna. Opcionalmente
    normaliza texto antes del mapeo.

    Parámetros:
    - Df: DataFrame a procesar.
    - Columna_Origen: Nombre de columna origen.
    - Columna_Destino: Nombre de columna destino.
    - Diccionario_Mapeo: Diccionario con mapeo de valores.
    - Normalizar: Si aplicar normalización de texto.
    - Valor_Default: Valor para casos no encontrados.

    Retorna:
    - DataFrame con columna destino agregada.

    """

    Df_Resultado = Df.copy()

    if Columna_Origen not in Df_Resultado.columns:
        print(f"  ✗ Columna '{Columna_Origen}' no encontrada")
        return Df_Resultado

    if Normalizar:
        Valores_Normalizados = (
            Df_Resultado[Columna_Origen]
            .apply(Normalizar_Texto)
        )
        Df_Resultado[Columna_Destino] = (
            Valores_Normalizados
            .map(Diccionario_Mapeo)
            .fillna(Valor_Default)
        )
    else:
        Df_Resultado[Columna_Destino] = (
            Df_Resultado[Columna_Origen]
            .map(Diccionario_Mapeo)
            .fillna(Valor_Default)
        )

    return Df_Resultado


def Aplicar_Agrupamiento_Rangos(
    Df: pd.DataFrame,
    Columna_Origen: str,
    Columna_Destino: str,
    Bins: List[Union[int, float]],
    Etiquetas: List[str]
) -> pd.DataFrame:

    """
    Agrupa valores numéricos en rangos categóricos usando
    pd.cut.

    Parámetros:
    - Df: DataFrame a procesar.
    - Columna_Origen: Nombre de columna numérica origen.
    - Columna_Destino: Nombre de columna destino.
    - Bins: Lista de límites de rangos.
    - Etiquetas: Lista de etiquetas para cada rango.

    Retorna:
    - DataFrame con columna destino agregada.

    """

    Df_Resultado = Df.copy()

    if Columna_Origen not in Df_Resultado.columns:
        print(f"  ✗ Columna '{Columna_Origen}' no encontrada")
        return Df_Resultado

    # Convertir a numérico.
    Df_Resultado[Columna_Origen] = pd.to_numeric(
        Df_Resultado[Columna_Origen],
        errors='coerce'
    )

    # Aplicar pd.cut.
    Df_Resultado[Columna_Destino] = pd.cut(
        Df_Resultado[Columna_Origen],
        bins=Bins,
        labels=Etiquetas,
        include_lowest=True
    )

    return Df_Resultado


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def Aplicar_Agrupamiento_General(
    Df: pd.DataFrame,
    Configuracion_Agrupamiento: Dict[str, Dict[str, Any]]
) -> pd.DataFrame:

    """
    Aplica múltiples agrupamientos de forma genérica según
    configuración proporcionada.

    La configuración debe ser un diccionario donde cada clave
    es el nombre de la transformación y el valor es otro
    diccionario con:
    - 'tipo': 'mapeo' o 'rangos'
    - 'columna_origen': nombre de columna origen
    - 'columna_destino': nombre de columna destino
    - Para tipo 'mapeo':
      - 'diccionario': diccionario de mapeo
      - 'normalizar': bool (opcional, default True)
      - 'valor_default': str (opcional, default 'Otro')
    - Para tipo 'rangos':
      - 'bins': lista de límites
      - 'etiquetas': lista de etiquetas

    Parámetros:
    - Df: DataFrame a procesar.
    - Configuracion_Agrupamiento: Diccionario de
      configuración.

    Retorna:
    - DataFrame con todas las transformaciones aplicadas.

    """

    print("\n" + "="*60)
    print("APLICACIÓN DE AGRUPAMIENTOS")
    print("="*60)

    Df_Resultado = Df.copy()
    Transformaciones_Aplicadas = 0

    for Nombre, Config in Configuracion_Agrupamiento.items():
        print(f"\n  Aplicando: {Nombre}")

        Tipo = Config.get('tipo')
        Columna_Origen = Config.get('columna_origen')
        Columna_Destino = Config.get('columna_destino')

        if Tipo == 'mapeo':
            Diccionario = Config.get('diccionario', {})
            Normalizar = Config.get('normalizar', True)
            Valor_Default = Config.get('valor_default', 'Otro')

            Df_Resultado = Aplicar_Mapeo_Diccionario(
                Df_Resultado,
                Columna_Origen,
                Columna_Destino,
                Diccionario,
                Normalizar,
                Valor_Default
            )

            Transformaciones_Aplicadas += 1

        elif Tipo == 'rangos':
            Bins = Config.get('bins', [])
            Etiquetas = Config.get('etiquetas', [])

            Df_Resultado = Aplicar_Agrupamiento_Rangos(
                Df_Resultado,
                Columna_Origen,
                Columna_Destino,
                Bins,
                Etiquetas
            )

            Transformaciones_Aplicadas += 1

        else:
            print(f"  ✗ Tipo '{Tipo}' no reconocido")

    print(f"\n✓ {Transformaciones_Aplicadas} "
          f"transformaciones aplicadas")

    print("\n" + "="*60)
    print("✓ AGRUPAMIENTOS COMPLETADOS")
    print("="*60)

    return Df_Resultado


def Aplicar_Agrupamientos_Sociodemograficos(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Aplica todos los agrupamientos sociodemográficos estándar
    del estudio.

    Transformaciones incluidas:
    - Provincia → Region
    - Edad → Edad_Agrupada
    - Género normalizado
    - Inmueble_Residencia normalizado
    - Fuente_Ingreso normalizada
    - Nivel_Educativo normalizado
    - Situacion_Laboral normalizada
    - Estado_Civil normalizado

    Parámetros:
    - Df: DataFrame con variables sociodemográficas.

    Retorna:
    - DataFrame con variables agrupadas.

    """

    print("\n" + "="*60)
    print("AGRUPAMIENTOS SOCIODEMOGRÁFICOS")
    print("="*60)

    # Configuración completa de agrupamientos.
    Configuracion = {
        'Provincia_a_Region': {
            'tipo': 'mapeo',
            'columna_origen': 'Provincia',
            'columna_destino': 'Region',
            'diccionario': MAPEO_PROVINCIAS,
            'normalizar': True,
            'valor_default': 'Otro'
        },
        'Edad_a_Rangos': {
            'tipo': 'rangos',
            'columna_origen': 'Edad',
            'columna_destino': 'Edad_Agrupada',
            'bins': RANGOS_EDAD,
            'etiquetas': ETIQUETAS_EDAD
        },
        'Genero_Normalizado': {
            'tipo': 'mapeo',
            'columna_origen': 'Genero',
            'columna_destino': 'Genero_Agrupado',
            'diccionario': MAPEO_GENERO,
            'normalizar': True,
            'valor_default': 'Otro'
        },
        'Inmueble_Normalizado': {
            'tipo': 'mapeo',
            'columna_origen': 'Inmueble_Residencia',
            'columna_destino': 'Inmueble_Agrupado',
            'diccionario': MAPEO_INMUEBLE,
            'normalizar': True,
            'valor_default': 'Otro'
        },
        'Fuente_Ingreso_Normalizada': {
            'tipo': 'mapeo',
            'columna_origen': 'Fuente_Ingreso',
            'columna_destino': 'Fuente_Ingreso_Agrupada',
            'diccionario': MAPEO_FUENTE_INGRESO,
            'normalizar': True,
            'valor_default': 'Otro'
        },
        'Nivel_Educativo_Normalizado': {
            'tipo': 'mapeo',
            'columna_origen': 'Nivel_Educativo',
            'columna_destino': 'Nivel_Educativo_Agrupado',
            'diccionario': MAPEO_NIVEL_EDUCATIVO,
            'normalizar': True,
            'valor_default': 'Otro'
        },
        'Situacion_Laboral_Normalizada': {
            'tipo': 'mapeo',
            'columna_origen': 'Situacion_Laboral',
            'columna_destino': 'Situacion_Laboral_Agrupada',
            'diccionario': MAPEO_SITUACION_LABORAL,
            'normalizar': True,
            'valor_default': 'Otro'
        },
        'Estado_Civil_Normalizado': {
            'tipo': 'mapeo',
            'columna_origen': 'Estado_Civil',
            'columna_destino': 'Estado_Civil_Agrupado',
            'diccionario': MAPEO_ESTADO_CIVIL,
            'normalizar': True,
            'valor_default': 'Otro'
        }
    }

    Df_Resultado = Aplicar_Agrupamiento_General(
        Df,
        Configuracion
    )

    print("\n" + "="*60)
    print("✓ AGRUPAMIENTOS SOCIODEMOGRÁFICOS COMPLETADOS")
    print("="*60)

    return Df_Resultado


def Agrupar_Autopercepciones(
    Df: pd.DataFrame,
    Columnas_Autopercepcion: List[str] = [
        'Autopercepcion_Izq_Der',
        'Autopercepcion_Prog_Cons',
        'Autopercepcion_Lib_Aut'
    ]
) -> pd.DataFrame:

    """
    Agrupa escalas de autopercepción (1-10) en categorías
    A/B/C.

    Categorías:
    - A: 1-3
    - B: 4-7
    - C: 8-10

    Parámetros:
    - Df: DataFrame con columnas de autopercepción.
    - Columnas_Autopercepcion: Lista de nombres de columnas.

    Retorna:
    - DataFrame con columnas _Agrupada agregadas.

    """

    print("\n" + "="*60)
    print("AGRUPAMIENTO DE AUTOPERCEPCIONES")
    print("="*60)

    Df_Resultado = Df.copy()

    # Definir bins y etiquetas.
    Bins_Autopercepcion = [0, 3, 7, 10]
    Etiquetas_Autopercepcion = ['A', 'B', 'C']

    Columnas_Procesadas = 0

    for Columna in Columnas_Autopercepcion:
        if Columna in Df_Resultado.columns:
            Columna_Destino = f'{Columna}_Agrupada'

            Df_Resultado = Aplicar_Agrupamiento_Rangos(
                Df_Resultado,
                Columna,
                Columna_Destino,
                Bins_Autopercepcion,
                Etiquetas_Autopercepcion
            )

            Columnas_Procesadas += 1
            print(f"  ✓ {Columna} → {Columna_Destino}")

    print(f"\n✓ {Columnas_Procesadas} columnas procesadas")

    print("\n" + "="*60)
    print("✓ AGRUPAMIENTO DE AUTOPERCEPCIONES COMPLETADO")
    print("="*60)

    return Df_Resultado


def Aplicar_Agrupamientos_Completos(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Aplica todos los agrupamientos: sociodemográficos y
    autopercepciones.

    Parámetros:
    - Df: DataFrame con datos procesados.

    Retorna:
    - DataFrame con todas las variables agrupadas.

    """

    print("\n" + "="*70)
    print("AGRUPAMIENTO COMPLETO DE VARIABLES")
    print("="*70)

    # Paso 1: Agrupamientos sociodemográficos.
    Df_Resultado = Aplicar_Agrupamientos_Sociodemograficos(Df)

    # Paso 2: Agrupamientos de autopercepciones.
    Df_Resultado = Agrupar_Autopercepciones(Df_Resultado)

    print("\n" + "="*70)
    print("✓ AGRUPAMIENTO COMPLETO FINALIZADO")
    print("="*70)

    return Df_Resultado


def Aplicar_Agrupamientos_Diccionario(
    Diccionario_Dfs: Dict[str, pd.DataFrame]
) -> Dict[str, pd.DataFrame]:

    """
    Aplica agrupamientos completos a un diccionario de
    DataFrames.

    Parámetros:
    - Diccionario_Dfs: Dict con DataFrames.

    Retorna:
    - Diccionario con DataFrames procesados.

    """

    Diccionario_Resultado = {}

    for Nombre, Df in Diccionario_Dfs.items():
        print(f"\n{'='*70}")
        print(f"PROCESANDO: {Nombre}")
        print(f"{'='*70}")

        Diccionario_Resultado[Nombre] = (
            Aplicar_Agrupamientos_Completos(Df)
        )

    return Diccionario_Resultado


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Este módulo debe ser importado, no ejecutado "
          "directamente.")
    print("Uso:")
    print("  from Agrupamiento_Variables import "
          "Aplicar_Agrupamientos_Completos")
    print("  Df = Aplicar_Agrupamientos_Completos(Df)")