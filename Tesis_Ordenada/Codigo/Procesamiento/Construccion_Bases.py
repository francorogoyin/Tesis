# ============================================================
# CONSTRUCCION_BASES.PY
# ============================================================
# Construcción de bases de datos desde archivos CSV crudos.
# Combina múltiples archivos de resultados en un solo
# DataFrame consolidado.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from pathlib import Path
import sys

# Agregar ruta de Utilidades al path.
sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import (
    RUTA_DATA_CRUDOS,
    RUTA_DATA_PROCESADOS
)
from Funciones_Comunes import Procesar_Columna_Results


# ============================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================

def Cargar_CSV_Crudo(Ruta_Archivo: Path) -> pd.DataFrame:

    """
    Carga un archivo CSV crudo individual.

    Parámetros:
    - Ruta_Archivo: Ruta completa al archivo CSV.

    Retorna:
    - DataFrame con los datos cargados.

    """

    try:
        Df = pd.read_csv(Ruta_Archivo, encoding='utf-8')
        print(f"✓ Cargado: {Ruta_Archivo.name}")
        return Df
    except Exception as Error:
        print(f"✗ Error cargando {Ruta_Archivo.name}: {Error}")
        return pd.DataFrame()


def Combinar_Archivos_Generales() -> pd.DataFrame:

    """
    Combina los 5 archivos de resultados de elecciones
    Generales en un solo DataFrame.

    Retorna:
    - DataFrame consolidado de elecciones Generales.

    """

    print("\n" + "="*60)
    print("COMBINANDO ARCHIVOS DE ELECCIONES GENERALES")
    print("="*60 + "\n")

    Lista_Dataframes = []

    for Numero in range(1, 6):
        Ruta = RUTA_DATA_CRUDOS / f"Generales {Numero}.csv"
        if Ruta.exists():
            Df = Cargar_CSV_Crudo(Ruta)
            if not Df.empty:
                Lista_Dataframes.append(Df)

    if Lista_Dataframes:
        Df_Combinado = pd.concat(
            Lista_Dataframes,
            ignore_index=True
        )
        print(
            f"\n✓ Total de filas combinadas: "
            f"{len(Df_Combinado)}"
        )
        return Df_Combinado
    else:
        print("✗ No se pudieron combinar archivos.")
        return pd.DataFrame()


def Combinar_Archivos_Ballotage() -> pd.DataFrame:

    """
    Combina los 2 archivos de resultados de Ballotage en un
    solo DataFrame.

    Retorna:
    - DataFrame consolidado de Ballotage.

    """

    print("\n" + "="*60)
    print("COMBINANDO ARCHIVOS DE BALLOTAGE")
    print("="*60 + "\n")

    Lista_Dataframes = []

    for Numero in range(1, 3):
        Ruta = RUTA_DATA_CRUDOS / f"Ballotage {Numero}.csv"
        if Ruta.exists():
            Df = Cargar_CSV_Crudo(Ruta)
            if not Df.empty:
                Lista_Dataframes.append(Df)

    if Lista_Dataframes:
        Df_Combinado = pd.concat(
            Lista_Dataframes,
            ignore_index=True
        )
        print(
            f"\n✓ Total de filas combinadas: "
            f"{len(Df_Combinado)}"
        )
        return Df_Combinado
    else:
        print("✗ No se pudieron combinar archivos.")
        return pd.DataFrame()


# ============================================================
# FUNCIONES DE PROCESAMIENTO
# ============================================================

def Procesar_Base_Completa(
    Df_Crudo: pd.DataFrame
) -> pd.DataFrame:

    """
    Procesa la base cruda extrayendo y aplanando la columna
    'results' en formato JSON.

    Parámetros:
    - Df_Crudo: DataFrame crudo con columna 'results'.

    Retorna:
    - DataFrame procesado con datos aplanados.

    """

    print("\nProcesando columna 'results'...")
    Df_Procesado = Procesar_Columna_Results(Df_Crudo)
    print(f"✓ Filas procesadas: {len(Df_Procesado)}")

    return Df_Procesado


# ============================================================
# FUNCIONES DE EXPORTACION
# ============================================================

def Guardar_Base_Procesada(
    Df: pd.DataFrame,
    Nombre_Archivo: str
) -> None:

    """
    Guarda el DataFrame procesado en formato Excel.

    Parámetros:
    - Df: DataFrame a guardar.
    - Nombre_Archivo: Nombre del archivo (sin extensión).

    """

    Ruta_Salida = (
        RUTA_DATA_PROCESADOS / f"{Nombre_Archivo}.xlsx"
    )

    try:
        Df.to_excel(Ruta_Salida, index=False)
        print(f"✓ Base guardada en: {Ruta_Salida}")
    except Exception as Error:
        print(f"✗ Error guardando base: {Error}")


# ============================================================
# EJECUCION PRINCIPAL
# ============================================================

def Ejecutar_Construccion_Bases():

    """
    Ejecuta el pipeline completo de construcción de bases.

    """

    print("\n" + "="*60)
    print("PIPELINE DE CONSTRUCCION DE BASES")
    print("="*60)

    # Combinar archivos Generales.
    Df_Generales_Crudo = Combinar_Archivos_Generales()
    if not Df_Generales_Crudo.empty:
        Df_Generales = Procesar_Base_Completa(
            Df_Generales_Crudo
        )
        Guardar_Base_Procesada(Df_Generales, "Base_Generales")

    # Combinar archivos Ballotage.
    Df_Ballotage_Crudo = Combinar_Archivos_Ballotage()
    if not Df_Ballotage_Crudo.empty:
        Df_Ballotage = Procesar_Base_Completa(
            Df_Ballotage_Crudo
        )
        Guardar_Base_Procesada(Df_Ballotage, "Base_Ballotage")

    print("\n" + "="*60)
    print("CONSTRUCCION DE BASES COMPLETADA")
    print("="*60 + "\n")


if __name__ == "__main__":
    Ejecutar_Construccion_Bases()
