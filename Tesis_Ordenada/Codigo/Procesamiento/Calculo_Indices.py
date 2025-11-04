# ============================================================
# CALCULO_INDICES.PY
# ============================================================
# Cálculo de índices de Progresismo, Conservadurismo y
# Positividad a partir de las respuestas a los items IP.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import (
    ITEMS_PROGRESISTAS,
    ITEMS_CONSERVADORES,
    NUMEROS_ITEMS_IP
)


# ============================================================
# FUNCIONES DE CALCULO DE INDICES
# ============================================================

def Calcular_Indice_Progresismo(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Calcula el índice de progresismo como promedio de
    respuestas a items progresistas.

    Parámetros:
    - Df: DataFrame con columnas IP_Item_X_Respuesta.

    Retorna:
    - DataFrame con columna 'Indice_Progresismo'.

    """

    Columnas_Progresistas = [
        f'IP_Item_{Num}_Respuesta' for Num in ITEMS_PROGRESISTAS
        if f'IP_Item_{Num}_Respuesta' in Df.columns
    ]

    if Columnas_Progresistas:
        Df['Indice_Progresismo'] = Df[
            Columnas_Progresistas
        ].mean(axis=1)
        print(
            f"✓ Índice de Progresismo calculado "
            f"({len(Columnas_Progresistas)} items)"
        )
    else:
        print("✗ No se encontraron columnas progresistas")

    return Df


def Calcular_Indice_Conservadurismo(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Calcula el índice de conservadurismo como promedio de
    respuestas a items conservadores.

    Parámetros:
    - Df: DataFrame con columnas IP_Item_X_Respuesta.

    Retorna:
    - DataFrame con columna 'Indice_Conservadurismo'.

    """

    Columnas_Conservadoras = [
        f'IP_Item_{Num}_Respuesta'
        for Num in ITEMS_CONSERVADORES
        if f'IP_Item_{Num}_Respuesta' in Df.columns
    ]

    if Columnas_Conservadoras:
        Df['Indice_Conservadurismo'] = Df[
            Columnas_Conservadoras
        ].mean(axis=1)
        print(
            f"✓ Índice de Conservadurismo calculado "
            f"({len(Columnas_Conservadoras)} items)"
        )
    else:
        print("✗ No se encontraron columnas conservadoras")

    return Df


def Calcular_Indice_Positividad(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Calcula el índice de positividad como promedio de todas
    las respuestas a items IP.

    Parámetros:
    - Df: DataFrame con columnas IP_Item_X_Respuesta.

    Retorna:
    - DataFrame con columna 'Indice_Positividad'.

    """

    Columnas_Todos_Items = [
        f'IP_Item_{Num}_Respuesta' for Num in NUMEROS_ITEMS_IP
        if f'IP_Item_{Num}_Respuesta' in Df.columns
    ]

    if Columnas_Todos_Items:
        Df['Indice_Positividad'] = Df[
            Columnas_Todos_Items
        ].mean(axis=1)
        print(
            f"✓ Índice de Positividad calculado "
            f"({len(Columnas_Todos_Items)} items)"
        )
    else:
        print("✗ No se encontraron columnas de items IP")

    return Df


def Calcular_Todos_Indices(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Calcula todos los índices ideológicos.

    Parámetros:
    - Df: DataFrame con columnas IP_Item_X_Respuesta.

    Retorna:
    - DataFrame con todos los índices calculados.

    """

    print("\nCalculando índices ideológicos...")

    Df = Calcular_Indice_Progresismo(Df)
    Df = Calcular_Indice_Conservadurismo(Df)
    Df = Calcular_Indice_Positividad(Df)

    print("✓ Todos los índices calculados.\n")

    return Df


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    print("Módulo de cálculo de índices cargado.")
