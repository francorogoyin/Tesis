# ============================================================
# TESTS_ADICIONALES.PY
# ============================================================
# Tests estadísticos no paramétricos adicionales: Wilcoxon,
# Kruskal-Wallis y análisis post-hoc con Dunn.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
from scipy.stats import wilcoxon, kruskal
from pathlib import Path
import sys
from typing import List, Dict

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import ALPHA, ORDEN_CATEGORIAS

# Importación condicional de scikit-posthocs.
try:
    import scikit_posthocs as sp
    POSTHOCS_DISPONIBLE = True
except ImportError:
    POSTHOCS_DISPONIBLE = False
    print(
        "⚠️ scikit-posthocs no disponible. "
        "Tests post-hoc deshabilitados."
    )


# ============================================================
# TEST DE WILCOXON (MUESTRAS PAREADAS)
# ============================================================

def Ejecutar_Wilcoxon(
    Df: pd.DataFrame,
    Columna_Variable_1: str,
    Columna_Variable_2: str,
    Alternative: str = 'two-sided'
) -> dict:

    """
    Ejecuta test de Wilcoxon para muestras pareadas.

    Útil para comparar dos mediciones del mismo sujeto
    (ej: CO_Item_3_Izq vs CO_Item_3_Der).

    Parámetros:
    - Df: DataFrame con los datos.
    - Columna_Variable_1: Primera variable a comparar.
    - Columna_Variable_2: Segunda variable a comparar.
    - Alternative: 'two-sided', 'less' o 'greater'.

    Retorna:
    - Diccionario con estadístico, p-valor y significancia.

    """

    # Extraer datos y eliminar NaN en pares.
    Datos = Df[[Columna_Variable_1, Columna_Variable_2]].dropna()

    Variable_1 = Datos[Columna_Variable_1]
    Variable_2 = Datos[Columna_Variable_2]

    # Verificar que hay suficientes datos.
    if len(Variable_1) < 3:
        return {
            'Estadistico': None,
            'P_Valor': None,
            'Significativo': False,
            'N': len(Variable_1),
            'Error': 'Datos insuficientes (mínimo 3 pares)'
        }

    # Verificar que hay diferencias no nulas.
    Diferencias = Variable_1 - Variable_2
    N_Diferencias_No_Nulas = (Diferencias != 0).sum()

    if N_Diferencias_No_Nulas < 1:
        return {
            'Estadistico': None,
            'P_Valor': None,
            'Significativo': False,
            'N': len(Variable_1),
            'Error': 'Todas las diferencias son cero'
        }

    # Ejecutar test.
    try:
        Estadistico, P_Valor = wilcoxon(
            Variable_1,
            Variable_2,
            alternative=Alternative
        )

        return {
            'Estadistico': Estadistico,
            'P_Valor': P_Valor,
            'Significativo': P_Valor < ALPHA,
            'N': len(Variable_1),
            'Media_Variable_1': Variable_1.mean(),
            'Media_Variable_2': Variable_2.mean(),
            'Mediana_Variable_1': Variable_1.median(),
            'Mediana_Variable_2': Variable_2.median()
        }
    except Exception as Error:
        return {
            'Estadistico': None,
            'P_Valor': None,
            'Significativo': False,
            'N': len(Variable_1),
            'Error': str(Error)
        }


# ============================================================
# TEST DE KRUSKAL-WALLIS (MÚLTIPLES GRUPOS)
# ============================================================

def Ejecutar_Kruskal_Wallis(
    Df: pd.DataFrame,
    Columna_Variable: str,
    Columna_Grupos: str = 'Categoria_PASO_2023',
    Categorias_Incluir: List[str] = None
) -> dict:

    """
    Ejecuta test de Kruskal-Wallis para comparar múltiples
    grupos independientes.

    Es la versión no paramétrica de ANOVA.

    Parámetros:
    - Df: DataFrame con los datos.
    - Columna_Variable: Variable a comparar entre grupos.
    - Columna_Grupos: Columna con etiquetas de grupos.
    - Categorias_Incluir: Lista de categorías a incluir.
      Si es None, usa ORDEN_CATEGORIAS.

    Retorna:
    - Diccionario con estadístico, p-valor y significancia.

    """

    if Categorias_Incluir is None:
        Categorias_Incluir = ORDEN_CATEGORIAS

    # Filtrar datos.
    Df_Filtrado = Df[
        Df[Columna_Grupos].isin(Categorias_Incluir)
    ][[Columna_Grupos, Columna_Variable]].dropna()

    # Crear grupos.
    Grupos = [
        Df_Filtrado[
            Df_Filtrado[Columna_Grupos] == Categoria
        ][Columna_Variable].values
        for Categoria in Categorias_Incluir
    ]

    # Filtrar grupos vacíos.
    Grupos = [G for G in Grupos if len(G) > 0]

    # Verificar que hay al menos 2 grupos con datos.
    if len(Grupos) < 2:
        return {
            'Estadistico': None,
            'P_Valor': None,
            'Significativo': False,
            'N_Grupos': len(Grupos),
            'Error': 'Se necesitan al menos 2 grupos con datos'
        }

    # Ejecutar test.
    try:
        Estadistico, P_Valor = kruskal(*Grupos)

        # Contar observaciones por grupo.
        N_Por_Grupo = {
            Categoria: len(
                Df_Filtrado[
                    Df_Filtrado[Columna_Grupos] == Categoria
                ][Columna_Variable]
            )
            for Categoria in Categorias_Incluir
        }

        return {
            'Estadistico': Estadistico,
            'P_Valor': P_Valor,
            'Significativo': P_Valor < ALPHA,
            'N_Grupos': len(Grupos),
            'N_Total': sum(len(G) for G in Grupos),
            'N_Por_Grupo': N_Por_Grupo
        }
    except Exception as Error:
        return {
            'Estadistico': None,
            'P_Valor': None,
            'Significativo': False,
            'N_Grupos': len(Grupos),
            'Error': str(Error)
        }


# ============================================================
# ANÁLISIS POST-HOC CON TEST DE DUNN
# ============================================================

def Ejecutar_Post_Hoc_Dunn(
    Df: pd.DataFrame,
    Columna_Variable: str,
    Columna_Grupos: str = 'Categoria_PASO_2023',
    Metodo_Ajuste: str = 'holm'
) -> pd.DataFrame:

    """
    Ejecuta análisis post-hoc con test de Dunn para
    comparaciones múltiples después de Kruskal-Wallis.

    Parámetros:
    - Df: DataFrame con los datos.
    - Columna_Variable: Variable a comparar.
    - Columna_Grupos: Columna con etiquetas de grupos.
    - Metodo_Ajuste: Método de ajuste de p-valores
      ('bonferroni', 'holm', 'fdr_bh', etc.).

    Retorna:
    - DataFrame con matriz de p-valores ajustados.

    """

    if not POSTHOCS_DISPONIBLE:
        print(
            "⚠️ scikit-posthocs no disponible. "
            "Instalar con: pip install scikit-posthocs"
        )
        return pd.DataFrame()

    # Eliminar filas con NaN.
    Datos_Limpios = Df[
        [Columna_Grupos, Columna_Variable]
    ].dropna()

    # Verificar que hay suficientes datos.
    if len(Datos_Limpios) < 3:
        print(
            f"⚠️ Datos insuficientes para {Columna_Variable}"
        )
        return pd.DataFrame()

    try:
        Matriz_Dunn = sp.posthoc_dunn(
            Datos_Limpios,
            val_col=Columna_Variable,
            group_col=Columna_Grupos,
            p_adjust=Metodo_Ajuste
        )

        return Matriz_Dunn

    except Exception as Error:
        print(f"⚠️ Error en test de Dunn: {Error}")
        return pd.DataFrame()


def Resumir_Comparaciones_Significativas(
    Matriz_P_Valores: pd.DataFrame,
    Umbral: float = ALPHA
) -> List[str]:

    """
    Resume las comparaciones significativas de una matriz
    de p-valores.

    Parámetros:
    - Matriz_P_Valores: Matriz de p-valores (de Dunn u otro).
    - Umbral: Umbral de significancia (por defecto ALPHA).

    Retorna:
    - Lista de strings describiendo comparaciones
      significativas.

    """

    Comparaciones = []

    for Categoria_1 in Matriz_P_Valores.index:
        for Categoria_2 in Matriz_P_Valores.columns:
            # Evitar duplicados (solo triángulo superior).
            if Categoria_1 < Categoria_2:
                P_Valor = Matriz_P_Valores.loc[
                    Categoria_1,
                    Categoria_2
                ]
                if P_Valor < Umbral:
                    Comparaciones.append(
                        f"{Categoria_1} vs {Categoria_2} "
                        f"(p = {P_Valor:.4f})"
                    )

    return Comparaciones


# ============================================================
# FUNCIÓN INTEGRADA DE ANÁLISIS KRUSKAL + POST-HOC
# ============================================================

def Analizar_Kruskal_Con_Post_Hoc(
    Df: pd.DataFrame,
    Columnas_Variables: List[str],
    Columna_Grupos: str = 'Categoria_PASO_2023',
    Metodo_Ajuste: str = 'holm',
    Verbose: bool = True
) -> Dict[str, dict]:

    """
    Ejecuta análisis completo de Kruskal-Wallis seguido de
    post-hoc con Dunn para múltiples variables.

    Parámetros:
    - Df: DataFrame con los datos.
    - Columnas_Variables: Lista de variables a analizar.
    - Columna_Grupos: Columna con etiquetas de grupos.
    - Metodo_Ajuste: Método de ajuste para post-hoc.
    - Verbose: Si imprimir resultados durante ejecución.

    Retorna:
    - Diccionario con resultados por variable.

    """

    Resultados = {}

    for Variable in Columnas_Variables:
        if Verbose:
            print(f"\n{'='*70}")
            print(f"Analizando: {Variable}")
            print('='*70)

        # Kruskal-Wallis.
        Resultado_Kruskal = Ejecutar_Kruskal_Wallis(
            Df,
            Variable,
            Columna_Grupos
        )

        if Verbose:
            print(f"\nKruskal-Wallis:")
            print(
                f"  H = {Resultado_Kruskal.get('Estadistico', 'N/A')}"
            )
            print(
                f"  p = {Resultado_Kruskal.get('P_Valor', 'N/A')}"
            )
            print(
                f"  Significativo: "
                f"{Resultado_Kruskal.get('Significativo', False)}"
            )

        # Post-hoc solo si es significativo.
        Matriz_Post_Hoc = None
        Comparaciones_Significativas = []

        if Resultado_Kruskal.get('Significativo', False):
            Matriz_Post_Hoc = Ejecutar_Post_Hoc_Dunn(
                Df,
                Variable,
                Columna_Grupos,
                Metodo_Ajuste
            )

            if not Matriz_Post_Hoc.empty:
                Comparaciones_Significativas = (
                    Resumir_Comparaciones_Significativas(
                        Matriz_Post_Hoc
                    )
                )

                if Verbose:
                    print(f"\nPost-hoc (Dunn):")
                    if Comparaciones_Significativas:
                        for Comp in Comparaciones_Significativas:
                            print(f"  • {Comp}")
                    else:
                        print(
                            "  No hay diferencias "
                            "significativas entre pares"
                        )

        Resultados[Variable] = {
            'Kruskal_Wallis': Resultado_Kruskal,
            'Matriz_Post_Hoc': Matriz_Post_Hoc,
            'Comparaciones_Significativas':
                Comparaciones_Significativas
        }

    return Resultados


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    print("Módulo de tests adicionales cargado.")
