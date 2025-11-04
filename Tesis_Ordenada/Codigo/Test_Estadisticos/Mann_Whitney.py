# ============================================================
# MANN_WHITNEY.PY
# ============================================================
# Tests de Mann-Whitney U para comparaciones no paramétricas
# entre grupos ideológicos.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from scipy.stats import mannwhitneyu
from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import ALPHA, CATEGORIAS_EXCLUIR


# ============================================================
# FUNCIONES DE TEST
# ============================================================

def Ejecutar_Mann_Whitney(
    Df: pd.DataFrame,
    Columna_Variable: str,
    Categoria_Grupo_1: list,
    Categoria_Grupo_2: list
) -> dict:

    """
    Ejecuta test Mann-Whitney U entre dos grupos.

    Parámetros:
    - Df: DataFrame con los datos.
    - Columna_Variable: Variable a comparar (ej: 'CO_Item_3_Izq').
    - Categoria_Grupo_1: Lista de categorías del grupo 1.
    - Categoria_Grupo_2: Lista de categorías del grupo 2.

    Retorna:
    - Diccionario con estadístico, p-valor y significancia.

    """

    # Filtrar datos excluyendo categorías no válidas.
    Df_Limpio = Df[
        ~Df['Categoria_PASO_2023'].isin(CATEGORIAS_EXCLUIR)
    ]

    # Extraer datos de cada grupo.
    Datos_Grupo_1 = Df_Limpio[
        Df_Limpio['Categoria_PASO_2023'].isin(
            Categoria_Grupo_1
        )
    ][Columna_Variable].dropna()

    Datos_Grupo_2 = Df_Limpio[
        Df_Limpio['Categoria_PASO_2023'].isin(
            Categoria_Grupo_2
        )
    ][Columna_Variable].dropna()

    # Verificar que hay suficientes datos.
    if len(Datos_Grupo_1) < 3 or len(Datos_Grupo_2) < 3:
        return {
            'Estadistico': None,
            'P_Valor': None,
            'Significativo': False,
            'N_Grupo_1': len(Datos_Grupo_1),
            'N_Grupo_2': len(Datos_Grupo_2)
        }

    # Ejecutar test.
    Estadistico, P_Valor = mannwhitneyu(
        Datos_Grupo_1,
        Datos_Grupo_2,
        alternative='two-sided'
    )

    return {
        'Estadistico': Estadistico,
        'P_Valor': P_Valor,
        'Significativo': P_Valor < ALPHA,
        'N_Grupo_1': len(Datos_Grupo_1),
        'N_Grupo_2': len(Datos_Grupo_2),
        'Media_Grupo_1': Datos_Grupo_1.mean(),
        'Media_Grupo_2': Datos_Grupo_2.mean()
    }


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    print("Módulo de tests Mann-Whitney cargado.")
