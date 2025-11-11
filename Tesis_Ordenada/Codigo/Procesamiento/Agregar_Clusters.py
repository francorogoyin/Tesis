# ============================================================
# AGREGAR_CLUSTERS.PY
# ============================================================
# Agregado de variables de clustering ideológico desde
# archivo externo. Incorpora vectores y asignaciones de
# cluster basadas en análisis K-means de índices de
# Progresismo y Conservadurismo.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from pathlib import Path
from typing import Dict, List
import sys

# Agregar ruta de Data al path.
Ruta_Actual = Path(__file__).parent
Ruta_Data = Ruta_Actual.parent.parent / "Data"


# ============================================================
# CONSTANTES
# ============================================================

# Ruta al archivo de clusters.
RUTA_ARCHIVO_CLUSTERS = Ruta_Data / "Clusters.xlsx"

# Columnas de cluster a transferir.
COLUMNAS_CLUSTER = [
    'Conservative_Vector',
    'Progressive_Vector',
    'Conservative_Cluster',
    'Progressive_Cluster'
]


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def Cargar_Datos_Clusters(
    Ruta_Archivo: Path = RUTA_ARCHIVO_CLUSTERS
) -> pd.DataFrame:

    """
    Carga archivo de datos de clustering.

    El archivo contiene:
    - ID: Identificador único de participante
    - Election: Tipo de elección (Generales/Ballotage)
    - Conservative_Vector: Vector bidimensional conservador
    - Progressive_Vector: Vector bidimensional progresista
    - Conservative_Cluster: Asignación de cluster conservador
    - Progressive_Cluster: Asignación de cluster progresista

    Parámetros:
    - Ruta_Archivo: Path al archivo Clusters.xlsx.

    Retorna:
    - DataFrame con datos de clustering.

    """

    print("\n" + "="*60)
    print("CARGA DE DATOS DE CLUSTERING")
    print("="*60)

    if not Ruta_Archivo.exists():
        print(f"✗ Error: Archivo no encontrado en {Ruta_Archivo}")
        return pd.DataFrame()

    print(f"\nCargando desde: {Ruta_Archivo}")

    Df_Clusters = pd.read_excel(Ruta_Archivo)

    print(f"✓ Archivo cargado: {len(Df_Clusters)} filas, "
          f"{len(Df_Clusters.columns)} columnas")

    # Verificar columnas requeridas.
    Columnas_Requeridas = ['ID', 'Election'] + COLUMNAS_CLUSTER
    Columnas_Faltantes = [
        Col for Col in Columnas_Requeridas
        if Col not in Df_Clusters.columns
    ]

    if Columnas_Faltantes:
        print(f"⚠ Columnas faltantes: {Columnas_Faltantes}")

    # Reporte de distribución por elección.
    if 'Election' in Df_Clusters.columns:
        print("\nDistribución por elección:")
        Distribucion = Df_Clusters['Election'].value_counts()
        for Eleccion, Cantidad in Distribucion.items():
            print(f"  {Eleccion}: {Cantidad} casos")

    print("\n" + "="*60)
    print("✓ CARGA COMPLETADA")
    print("="*60)

    return Df_Clusters


def Agregar_Clusters_A_DataFrame(
    Df: pd.DataFrame,
    Df_Clusters: pd.DataFrame,
    Nombre_Eleccion: str
) -> pd.DataFrame:

    """
    Agrega variables de cluster a un DataFrame mediante merge
    con ID.

    Parámetros:
    - Df: DataFrame destino.
    - Df_Clusters: DataFrame con datos de clustering.
    - Nombre_Eleccion: Nombre de la elección ('Generales' o
      'Ballotage').

    Retorna:
    - DataFrame con columnas de cluster agregadas.

    """

    print("\n" + "="*60)
    print(f"AGREGANDO CLUSTERS - {Nombre_Eleccion}")
    print("="*60)

    Df_Resultado = Df.copy()

    # Verificar que existe columna ID.
    if 'ID' not in Df_Resultado.columns:
        print("✗ Error: Columna 'ID' no encontrada en DataFrame")
        return Df_Resultado

    # Filtrar datos de la elección correspondiente.
    Datos_Filtrados = Df_Clusters[
        Df_Clusters['Election'] == Nombre_Eleccion
    ].copy()

    print(f"\nCasos en archivo de clusters: "
          f"{len(Datos_Filtrados)}")
    print(f"Casos en DataFrame destino: {len(Df_Resultado)}")

    # Seleccionar solo ID y columnas de cluster.
    Columnas_A_Mergear = ['ID'] + COLUMNAS_CLUSTER
    Columnas_Disponibles = [
        Col for Col in Columnas_A_Mergear
        if Col in Datos_Filtrados.columns
    ]

    Datos_A_Mergear = Datos_Filtrados[Columnas_Disponibles]

    # Realizar merge.
    Columnas_Antes = len(Df_Resultado.columns)

    Df_Resultado = Df_Resultado.merge(
        Datos_A_Mergear,
        on='ID',
        how='left'
    )

    Columnas_Despues = len(Df_Resultado.columns)
    Columnas_Agregadas = Columnas_Despues - Columnas_Antes

    print(f"\n✓ {Columnas_Agregadas} columnas agregadas")

    # Reporte de columnas agregadas.
    Columnas_Nuevas = [
        Col for Col in COLUMNAS_CLUSTER
        if Col in Df_Resultado.columns
    ]

    if Columnas_Nuevas:
        print("\nColumnas agregadas:")
        for Col in Columnas_Nuevas:
            Valores_Nulos = Df_Resultado[Col].isna().sum()
            Porcentaje_Nulos = (
                (Valores_Nulos / len(Df_Resultado)) * 100
            )
            print(f"  - {Col}: {Valores_Nulos} NaN "
                  f"({Porcentaje_Nulos:.1f}%)")

    print("\n" + "="*60)
    print("✓ AGREGADO DE CLUSTERS COMPLETADO")
    print("="*60)

    return Df_Resultado


def Agregar_Clusters_Completo(
    Df: pd.DataFrame,
    Nombre_Eleccion: str,
    Ruta_Archivo: Path = RUTA_ARCHIVO_CLUSTERS
) -> pd.DataFrame:

    """
    Carga archivo de clusters y los agrega al DataFrame.

    Proceso completo:
    1. Cargar archivo Clusters.xlsx
    2. Filtrar por tipo de elección
    3. Hacer merge por ID
    4. Agregar 4 columnas de clustering

    Parámetros:
    - Df: DataFrame a procesar.
    - Nombre_Eleccion: 'Generales' o 'Ballotage'.
    - Ruta_Archivo: Path al archivo de clusters (opcional).

    Retorna:
    - DataFrame con variables de cluster agregadas.

    """

    print("\n" + "="*70)
    print("PROCESO COMPLETO - AGREGADO DE CLUSTERS")
    print("="*70)

    # Paso 1: Cargar datos de clusters.
    Df_Clusters = Cargar_Datos_Clusters(Ruta_Archivo)

    if Df_Clusters.empty:
        print("\n✗ No se pudieron cargar datos de clustering")
        return Df

    # Paso 2: Agregar clusters al DataFrame.
    Df_Resultado = Agregar_Clusters_A_DataFrame(
        Df,
        Df_Clusters,
        Nombre_Eleccion
    )

    print("\n" + "="*70)
    print("✓ PROCESO COMPLETO FINALIZADO")
    print("="*70)

    return Df_Resultado


def Agregar_Clusters_Diccionario(
    Diccionario_Dfs: Dict[str, pd.DataFrame],
    Ruta_Archivo: Path = RUTA_ARCHIVO_CLUSTERS
) -> Dict[str, pd.DataFrame]:

    """
    Aplica agregado de clusters a un diccionario de
    DataFrames.

    La clave del diccionario debe coincidir con el valor de
    'Election' en el archivo de clusters ('Generales' o
    'Ballotage').

    Parámetros:
    - Diccionario_Dfs: Dict con DataFrames.
    - Ruta_Archivo: Path al archivo de clusters (opcional).

    Retorna:
    - Diccionario con DataFrames procesados.

    """

    # Cargar datos de clusters una sola vez.
    Df_Clusters = Cargar_Datos_Clusters(Ruta_Archivo)

    if Df_Clusters.empty:
        print("\n✗ No se pudieron cargar datos de clustering")
        return Diccionario_Dfs

    Diccionario_Resultado = {}

    for Nombre, Df in Diccionario_Dfs.items():
        print(f"\n{'='*70}")
        print(f"PROCESANDO: {Nombre}")
        print(f"{'='*70}")

        Diccionario_Resultado[Nombre] = (
            Agregar_Clusters_A_DataFrame(
                Df,
                Df_Clusters,
                Nombre
            )
        )

    return Diccionario_Resultado


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Este módulo debe ser importado, no ejecutado "
          "directamente.")
    print("Uso:")
    print("  from Agregar_Clusters import "
          "Agregar_Clusters_Completo")
    print("  Df = Agregar_Clusters_Completo(Df, "
          "'Generales')")
