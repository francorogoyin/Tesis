# ============================================================
# ANALISIS_CORRELACION.PY
# ============================================================
# Análisis de correlaciones de Spearman entre variables
# ideológicas (predictores) y variables de cambio (outcomes).
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
from typing import List, Tuple, Dict

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import ALPHA, RUTA_GRAFICOS, RUTA_TABLAS


# ============================================================
# ANÁLISIS DE CORRELACIONES
# ============================================================

def Calcular_Matriz_Correlaciones_Spearman(
    Df: pd.DataFrame,
    Variables: List[str],
    Verbose: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    """
    Calcula matriz de correlaciones de Spearman entre
    variables especificadas.

    Parámetros:
    - Df: DataFrame con los datos.
    - Variables: Lista de nombres de variables a correlacionar.
    - Verbose: Si imprimir información durante el cálculo.

    Retorna:
    - Tupla con (Matriz_Correlaciones, Matriz_P_Valores).

    """

    # Verificar variables existentes.
    Variables_Existentes = [
        v for v in Variables if v in Df.columns
    ]
    Variables_Faltantes = [
        v for v in Variables if v not in Df.columns
    ]

    if Verbose and Variables_Faltantes:
        print(
            f"\n⚠️ Variables no encontradas "
            f"({len(Variables_Faltantes)}):"
        )
        for v in Variables_Faltantes[:5]:
            print(f"  - {v}")
        if len(Variables_Faltantes) > 5:
            print(f"  ... y {len(Variables_Faltantes) - 5} más")

    if Verbose:
        print(
            f"\n✓ Variables encontradas: "
            f"{len(Variables_Existentes)}"
        )

    # Seleccionar datos y eliminar NaN.
    Df_Subset = Df[Variables_Existentes].copy()
    Df_Clean = Df_Subset.dropna()

    if Verbose:
        print(
            f"✓ Registros válidos: {len(Df_Clean)} "
            f"de {len(Df)}"
        )

    # Calcular matriz de correlaciones.
    N_Vars = len(Variables_Existentes)
    Matriz_Corr = np.zeros((N_Vars, N_Vars))
    Matriz_P_Valor = np.zeros((N_Vars, N_Vars))

    if Verbose:
        print(f"\n🔄 Calculando correlaciones de Spearman...")

    for i in range(N_Vars):
        for j in range(N_Vars):
            if i == j:
                Matriz_Corr[i, j] = 1.0
                Matriz_P_Valor[i, j] = 0.0
            else:
                Datos_I = Df_Clean[Variables_Existentes[i]]
                Datos_J = Df_Clean[Variables_Existentes[j]]

                Corr, P_Val = spearmanr(Datos_I, Datos_J)

                Matriz_Corr[i, j] = Corr
                Matriz_P_Valor[i, j] = P_Val

    # Convertir a DataFrames.
    Df_Corr = pd.DataFrame(
        Matriz_Corr,
        index=Variables_Existentes,
        columns=Variables_Existentes
    )

    Df_P_Valor = pd.DataFrame(
        Matriz_P_Valor,
        index=Variables_Existentes,
        columns=Variables_Existentes
    )

    if Verbose:
        print(f"✅ Correlaciones calculadas exitosamente\n")

    return Df_Corr, Df_P_Valor


def Resumir_Correlaciones_Significativas(
    Df_Corr: pd.DataFrame,
    Df_P_Valor: pd.DataFrame,
    Variables_Predictoras: List[str],
    Variables_Outcome: List[str],
    Umbral: float = ALPHA,
    Top_N: int = 10
) -> Dict[str, List[Dict]]:

    """
    Resume las correlaciones significativas entre predictores
    y outcomes.

    Parámetros:
    - Df_Corr: Matriz de correlaciones.
    - Df_P_Valor: Matriz de p-valores.
    - Variables_Predictoras: Lista de variables predictoras.
    - Variables_Outcome: Lista de variables outcome.
    - Umbral: Umbral de significancia (por defecto ALPHA).
    - Top_N: Número de correlaciones principales a reportar.

    Retorna:
    - Diccionario con correlaciones significativas por
      predictor.

    """

    Resumen = {}

    for Predictor in Variables_Predictoras:
        if Predictor not in Df_Corr.index:
            continue

        Correlaciones_Sig = []

        for Outcome in Variables_Outcome:
            if Outcome not in Df_Corr.columns:
                continue

            Corr = Df_Corr.loc[Predictor, Outcome]
            P_Val = Df_P_Valor.loc[Predictor, Outcome]

            if P_Val < Umbral:
                Sig = (
                    '***' if P_Val < 0.001 else
                    '**' if P_Val < 0.01 else
                    '*'
                )

                Correlaciones_Sig.append({
                    'Variable': Outcome,
                    'r': Corr,
                    'p': P_Val,
                    'sig': Sig
                })

        # Ordenar por valor absoluto de correlación.
        Correlaciones_Sig.sort(
            key=lambda x: abs(x['r']),
            reverse=True
        )

        Resumen[Predictor] = Correlaciones_Sig[:Top_N]

    return Resumen


def Imprimir_Resumen_Correlaciones(
    Resumen: Dict[str, List[Dict]]
) -> None:

    """
    Imprime resumen de correlaciones significativas.

    Parámetros:
    - Resumen: Diccionario con correlaciones por predictor.

    """

    print("\n" + "="*70)
    print("RESUMEN: CORRELACIONES SIGNIFICATIVAS")
    print("="*70)

    for Predictor, Correlaciones in Resumen.items():
        print(f"\n{Predictor}:")

        if Correlaciones:
            for Item in Correlaciones:
                print(
                    f"  {Item['Variable']:<35} "
                    f"r={Item['r']:>6.3f} "
                    f"(p={Item['p']:.4f}) {Item['sig']}"
                )
        else:
            print("  ❌ No hay correlaciones significativas")

    print("\n" + "="*70)


# ============================================================
# VISUALIZACIÓN
# ============================================================

def Crear_Heatmap_Correlaciones(
    Matriz_Corr: pd.DataFrame,
    Titulo: str,
    Ruta_Salida: Path,
    Tamano_Figura: Tuple[int, int] = (16, 14)
) -> None:

    """
    Crea y guarda heatmap de matriz de correlaciones.

    Parámetros:
    - Matriz_Corr: Matriz de correlaciones.
    - Titulo: Título del gráfico.
    - Ruta_Salida: Path completo del archivo de salida.
    - Tamano_Figura: Tupla con (ancho, alto) en pulgadas.

    """

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=Tamano_Figura)

    # Crear heatmap.
    sns.heatmap(
        Matriz_Corr,
        annot=True,
        fmt='.2f',
        cmap='RdBu_r',
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={'label': 'Correlación de Spearman'},
        ax=Ax
    )

    # Configurar.
    Ax.set_title(Titulo, fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()

    # Crear directorio si no existe.
    Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)

    # Guardar.
    plt.savefig(Ruta_Salida, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Heatmap guardado: {Ruta_Salida.name}")


def Crear_Heatmap_Predictores_Vs_Outcomes(
    Df_Corr: pd.DataFrame,
    Variables_Predictoras: List[str],
    Variables_Outcome: List[str],
    Titulo: str,
    Ruta_Salida: Path
) -> None:

    """
    Crea heatmap enfocado solo en predictores vs outcomes.

    Parámetros:
    - Df_Corr: Matriz de correlaciones completa.
    - Variables_Predictoras: Lista de variables predictoras.
    - Variables_Outcome: Lista de variables outcome.
    - Titulo: Título del gráfico.
    - Ruta_Salida: Path completo del archivo de salida.

    """

    # Filtrar variables disponibles.
    Predictores_Disp = [
        p for p in Variables_Predictoras
        if p in Df_Corr.index
    ]
    Outcomes_Disp = [
        o for o in Variables_Outcome
        if o in Df_Corr.columns
    ]

    if not Predictores_Disp or not Outcomes_Disp:
        print(
            "⚠️ No hay suficientes variables para crear "
            "heatmap de predictores vs outcomes"
        )
        return

    # Extraer submatriz.
    Df_Subset = Df_Corr.loc[Predictores_Disp, Outcomes_Disp]

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=(18, 4))

    # Crear heatmap.
    sns.heatmap(
        Df_Subset,
        annot=True,
        fmt='.3f',
        cmap='RdBu_r',
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        cbar_kws={'label': 'Correlación de Spearman'},
        ax=Ax
    )

    # Configurar.
    Ax.set_title(
        Titulo,
        fontsize=14,
        fontweight='bold',
        pad=15
    )
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()

    # Crear directorio si no existe.
    Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)

    # Guardar.
    plt.savefig(Ruta_Salida, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  ✓ Heatmap guardado: {Ruta_Salida.name}")


# ============================================================
# EXPORTACIÓN
# ============================================================

def Exportar_Correlaciones_Excel(
    Df_Corr: pd.DataFrame,
    Df_P_Valor: pd.DataFrame,
    Ruta_Salida: Path
) -> None:

    """
    Exporta matrices de correlación a Excel con formato.

    Crea tres hojas:
    1. Correlaciones (valores numéricos).
    2. P-valores.
    3. Correlaciones con significancia marcada.

    Parámetros:
    - Df_Corr: Matriz de correlaciones.
    - Df_P_Valor: Matriz de p-valores.
    - Ruta_Salida: Path completo del archivo Excel.

    """

    # Crear directorio si no existe.
    Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)

    # Crear DataFrame con significancia marcada.
    Df_Texto = pd.DataFrame(
        index=Df_Corr.index,
        columns=Df_Corr.columns
    )

    for i in Df_Corr.index:
        for j in Df_Corr.columns:
            Corr = Df_Corr.loc[i, j]
            P_Val = Df_P_Valor.loc[i, j]

            if i == j:
                Df_Texto.loc[i, j] = '1.00'
            else:
                Sig = (
                    '***' if P_Val < 0.001 else
                    '**' if P_Val < 0.01 else
                    '*' if P_Val < 0.05 else
                    ''
                )
                Df_Texto.loc[i, j] = f"{Corr:.3f}{Sig}"

    # Guardar en Excel.
    with pd.ExcelWriter(
        Ruta_Salida,
        engine='openpyxl'
    ) as Writer:
        Df_Corr.to_excel(
            Writer,
            sheet_name='Correlaciones',
            index=True
        )
        Df_P_Valor.to_excel(
            Writer,
            sheet_name='P_Valores',
            index=True
        )
        Df_Texto.to_excel(
            Writer,
            sheet_name='Correlaciones_Sig',
            index=True
        )

    print(f"  ✓ Excel guardado: {Ruta_Salida.name}")


# ============================================================
# FUNCIÓN INTEGRADA
# ============================================================

def Analizar_Correlaciones_Completo(
    Diccionario_Dfs: Dict[str, pd.DataFrame],
    Variables_Predictoras: List[str],
    Variables_Outcome: List[str],
    Prefijo_Archivos: str = "Correlaciones"
) -> Dict[str, Dict]:

    """
    Ejecuta análisis completo de correlaciones para múltiples
    DataFrames.

    Parámetros:
    - Diccionario_Dfs: Diccionario con DataFrames a analizar.
    - Variables_Predictoras: Lista de predictores.
    - Variables_Outcome: Lista de outcomes.
    - Prefijo_Archivos: Prefijo para archivos de salida.

    Retorna:
    - Diccionario con resultados por DataFrame.

    """

    print("\n" + "="*70)
    print("ANÁLISIS COMPLETO DE CORRELACIONES")
    print("="*70)

    Resultados = {}

    for Nombre_Df, Df in Diccionario_Dfs.items():
        print(f"\n{'#'*70}")
        print(f"PROCESANDO: {Nombre_Df}")
        print(f"{'#'*70}")

        # Todas las variables.
        Todas_Variables = (
            Variables_Predictoras +
            Variables_Outcome
        )

        # Calcular correlaciones.
        Df_Corr, Df_P_Valor = (
            Calcular_Matriz_Correlaciones_Spearman(
                Df,
                Todas_Variables,
                Verbose=True
            )
        )

        # Resumir significancias.
        Resumen = Resumir_Correlaciones_Significativas(
            Df_Corr,
            Df_P_Valor,
            Variables_Predictoras,
            Variables_Outcome
        )

        Imprimir_Resumen_Correlaciones(Resumen)

        # Guardar resultados.
        print(f"\n📁 Guardando resultados de {Nombre_Df}...")

        # Excel.
        Ruta_Excel = (
            RUTA_TABLAS /
            f"{Prefijo_Archivos}_{Nombre_Df}.xlsx"
        )
        Exportar_Correlaciones_Excel(
            Df_Corr,
            Df_P_Valor,
            Ruta_Excel
        )

        # Heatmap completo.
        Ruta_Heatmap = (
            RUTA_GRAFICOS /
            f"Heatmap_{Prefijo_Archivos}_{Nombre_Df}.png"
        )
        Crear_Heatmap_Correlaciones(
            Df_Corr,
            f"Correlaciones de Spearman - {Nombre_Df}",
            Ruta_Heatmap
        )

        # Heatmap predictores vs outcomes.
        Ruta_Heatmap_PvO = (
            RUTA_GRAFICOS /
            f"Heatmap_Predictores_vs_Outcomes_{Nombre_Df}.png"
        )
        Crear_Heatmap_Predictores_Vs_Outcomes(
            Df_Corr,
            Variables_Predictoras,
            Variables_Outcome,
            f"Predictores vs Outcomes - {Nombre_Df}",
            Ruta_Heatmap_PvO
        )

        Resultados[Nombre_Df] = {
            'Matriz_Correlaciones': Df_Corr,
            'Matriz_P_Valores': Df_P_Valor,
            'Resumen_Significativas': Resumen
        }

    print("\n" + "="*70)
    print("✅ ANÁLISIS DE CORRELACIONES COMPLETADO")
    print("="*70 + "\n")

    return Resultados


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Módulo de análisis de correlación cargado.")
