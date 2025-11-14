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
        # Convertir columnas a numérico antes de calcular media.
        for Columna in Columnas_Progresistas:
            Df[Columna] = pd.to_numeric(Df[Columna], errors='coerce')

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
        # Convertir columnas a numérico antes de calcular media.
        for Columna in Columnas_Conservadoras:
            Df[Columna] = pd.to_numeric(Df[Columna], errors='coerce')

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
    Calcula el índice de positividad como SUMA de items ECE
    (escala electoral), invirtiendo ECE_Item_5.

    IMPORTANTE: Usa columnas ECE (NO IP) y calcula suma
    (NO promedio), siguiendo el Notebook 3 original.

    Parámetros:
    - Df: DataFrame con columnas ECE_Item_1 a ECE_Item_7.

    Retorna:
    - DataFrame con columna 'Indice_Positividad'.

    """

    # Columnas ECE (escala electoral).
    Columnas_Positividad = [
        'ECE_Item_1',
        'ECE_Item_2',
        'ECE_Item_3',
        'ECE_Item_4',
        'ECE_Item_5',
        'ECE_Item_6',
        'ECE_Item_7'
    ]

    # Verificar que existan todas las columnas.
    Columnas_Presentes = [
        Col for Col in Columnas_Positividad
        if Col in Df.columns
    ]

    if len(Columnas_Presentes) == 7:
        # Convertir columnas a numérico.
        for Columna in Columnas_Positividad:
            Df[Columna] = pd.to_numeric(Df[Columna], errors='coerce')

        # Invertir ECE_Item_5 (mapeo: 5→1, 4→2, 3→3, 2→4, 1→5).
        Df['ECE_Item_5_Negativo'] = Df['ECE_Item_5'].map({
            5: 1,
            4: 2,
            3: 3,
            2: 4,
            1: 5
        })

        # Calcular índice como SUMA (no promedio).
        Df['Indice_Positividad'] = (
            Df['ECE_Item_1'] +
            Df['ECE_Item_2'] +
            Df['ECE_Item_3'] +
            Df['ECE_Item_4'] +
            Df['ECE_Item_5_Negativo'] +
            Df['ECE_Item_6'] +
            Df['ECE_Item_7']
        )

        print(
            f"✓ Índice de Positividad calculado "
            f"(7 items ECE, item 5 invertido, suma)"
        )
    else:
        print(
            f"✗ No se encontraron todas las columnas ECE "
            f"({len(Columnas_Presentes)}/7 presentes)"
        )

    return Df


def Calcular_Promedios_Tiempos(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Calcula promedios de tiempos de respuesta agrupados
    por tipo ideológico y candidato asociado.

    Crea 6 columnas:
    - Tiempos_Respuesta_Promedio_Pro_Izq
    - Tiempos_Respuesta_Promedio_Pro_Der
    - Tiempos_Respuesta_Promedio_Con_Izq
    - Tiempos_Respuesta_Promedio_Con_Der
    - Tiempos_Respuesta_Promedio_Pro
    - Tiempos_Respuesta_Promedio_Con

    Parámetros:
    - Df: DataFrame con columnas de tiempo individuales.

    Retorna:
    - DataFrame con 6 columnas adicionales de promedios.

    """

    # Generar listas de columnas de tiempo.
    Items_Progresistas_Izq_Tiempo = [
        f'IP_Item_{Item}_Izq_Tiempo'
        for Item in ITEMS_PROGRESISTAS
        if f'IP_Item_{Item}_Izq_Tiempo' in Df.columns
    ]

    Items_Progresistas_Der_Tiempo = [
        f'IP_Item_{Item}_Der_Tiempo'
        for Item in ITEMS_PROGRESISTAS
        if f'IP_Item_{Item}_Der_Tiempo' in Df.columns
    ]

    Items_Conservadores_Izq_Tiempo = [
        f'IP_Item_{Item}_Izq_Tiempo'
        for Item in ITEMS_CONSERVADORES
        if f'IP_Item_{Item}_Izq_Tiempo' in Df.columns
    ]

    Items_Conservadores_Der_Tiempo = [
        f'IP_Item_{Item}_Der_Tiempo'
        for Item in ITEMS_CONSERVADORES
        if f'IP_Item_{Item}_Der_Tiempo' in Df.columns
    ]

    # Calcular promedios por tipo y dirección.
    if Items_Progresistas_Izq_Tiempo:
        Df['Tiempos_Respuesta_Promedio_Pro_Izq'] = (
            Df[Items_Progresistas_Izq_Tiempo].mean(axis=1)
        )

    if Items_Progresistas_Der_Tiempo:
        Df['Tiempos_Respuesta_Promedio_Pro_Der'] = (
            Df[Items_Progresistas_Der_Tiempo].mean(axis=1)
        )

    if Items_Conservadores_Izq_Tiempo:
        Df['Tiempos_Respuesta_Promedio_Con_Izq'] = (
            Df[Items_Conservadores_Izq_Tiempo].mean(axis=1)
        )

    if Items_Conservadores_Der_Tiempo:
        Df['Tiempos_Respuesta_Promedio_Con_Der'] = (
            Df[Items_Conservadores_Der_Tiempo].mean(axis=1)
        )

    # Calcular promedios generales (sin distinción Izq/Der).
    if ('Tiempos_Respuesta_Promedio_Pro_Izq' in Df.columns and
        'Tiempos_Respuesta_Promedio_Pro_Der' in Df.columns):
        Df['Tiempos_Respuesta_Promedio_Pro'] = (
            Df[[
                'Tiempos_Respuesta_Promedio_Pro_Izq',
                'Tiempos_Respuesta_Promedio_Pro_Der'
            ]].mean(axis=1)
        )

    if ('Tiempos_Respuesta_Promedio_Con_Izq' in Df.columns and
        'Tiempos_Respuesta_Promedio_Con_Der' in Df.columns):
        Df['Tiempos_Respuesta_Promedio_Con'] = (
            Df[[
                'Tiempos_Respuesta_Promedio_Con_Izq',
                'Tiempos_Respuesta_Promedio_Con_Der'
            ]].mean(axis=1)
        )

    return Df


def Calcular_Todos_Indices(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Calcula todos los índices ideológicos y promedios
    de tiempos.

    Parámetros:
    - Df: DataFrame con columnas IP_Item_X_Respuesta.

    Retorna:
    - DataFrame con todos los índices y promedios calculados.

    """

    print("\nCalculando índices ideológicos...")

    Df = Calcular_Indice_Progresismo(Df)
    Df = Calcular_Indice_Conservadurismo(Df)
    Df = Calcular_Indice_Positividad(Df)
    Df = Calcular_Promedios_Tiempos(Df)

    print("✓ Todos los índices calculados.\n")

    return Df


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    print("Módulo de cálculo de índices cargado.")
