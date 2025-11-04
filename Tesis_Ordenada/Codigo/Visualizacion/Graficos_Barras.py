# ============================================================
# GRAFICOS_BARRAS.PY
# ============================================================
# Módulo especializado en gráficos de barras con medias y
# errores estándar por categoría.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from typing import List, Tuple, Optional

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import (
    ORDEN_CATEGORIAS,
    RUTA_GRAFICOS,
    COLORES_CATEGORIAS
)


# ============================================================
# GRÁFICO DE BARRAS BÁSICO
# ============================================================

def Grafico_Barras_Medias(
    Df: pd.DataFrame,
    Variable: str,
    Columna_Categoria: str = 'Categoria_PASO_2023',
    Titulo: str = None,
    Orden_Categorias: List[str] = None,
    Colores: List[str] = None,
    Mostrar_N: bool = True,
    Mostrar_Valores: bool = True,
    Escala_Y: Tuple[float, float] = None,
    Tamano_Figura: Tuple[int, int] = (10, 6),
    Ruta_Salida: Path = None
) -> pd.DataFrame:

    """
    Crea gráfico de barras mostrando media por categoría con
    barras de error estándar.

    Parámetros:
    - Df: DataFrame con los datos.
    - Variable: Nombre de la variable a graficar.
    - Columna_Categoria: Columna con categorías.
    - Titulo: Título del gráfico (None para automático).
    - Orden_Categorias: Orden de categorías (None usa
      ORDEN_CATEGORIAS).
    - Colores: Lista de colores para barras (None usa
      COLORES_CATEGORIAS).
    - Mostrar_N: Si mostrar tamaño de muestra en barras.
    - Mostrar_Valores: Si mostrar valores numéricos en barras.
    - Escala_Y: Tupla (min, max) para eje Y.
    - Tamano_Figura: Tupla (ancho, alto) en pulgadas.
    - Ruta_Salida: Path para guardar gráfico (None no guarda).

    Retorna:
    - DataFrame con estadísticas por categoría.

    """

    # Filtrar datos válidos.
    Datos_Limpios = Df[[Columna_Categoria, Variable]].dropna()

    if len(Datos_Limpios) == 0:
        print(f"⚠️ No hay datos válidos para {Variable}")
        return pd.DataFrame()

    # Calcular estadísticas por grupo.
    Estadisticas = Datos_Limpios.groupby(
        Columna_Categoria
    )[Variable].agg([
        'mean',
        'sem',
        'count'
    ]).reset_index()

    Estadisticas.columns = [
        Columna_Categoria,
        'Media',
        'Error_Estandar',
        'N'
    ]

    # Ordenar según parámetro.
    if Orden_Categorias is None:
        Orden_Categorias = ORDEN_CATEGORIAS

    # Filtrar y ordenar.
    Estadisticas_Filtradas = Estadisticas[
        Estadisticas[Columna_Categoria].isin(Orden_Categorias)
    ].copy()

    Orden_Mapeo = {
        cat: i for i, cat in enumerate(Orden_Categorias)
    }
    Estadisticas_Filtradas['Orden'] = (
        Estadisticas_Filtradas[Columna_Categoria].map(
            Orden_Mapeo
        )
    )
    Estadisticas_Ordenadas = Estadisticas_Filtradas.sort_values(
        'Orden'
    ).drop('Orden', axis=1)

    # Verificar datos.
    if len(Estadisticas_Ordenadas) == 0:
        print(
            f"⚠️ No hay datos para las categorías "
            f"especificadas"
        )
        return pd.DataFrame()

    # Configurar colores.
    if Colores is None:
        Colores = [
            COLORES_CATEGORIAS.get(cat, 'steelblue')
            for cat in Estadisticas_Ordenadas[
                Columna_Categoria
            ]
        ]

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=Tamano_Figura)

    # Crear barras.
    Barras = Ax.bar(
        Estadisticas_Ordenadas[Columna_Categoria],
        Estadisticas_Ordenadas['Media'],
        yerr=Estadisticas_Ordenadas['Error_Estandar'],
        capsize=5,
        alpha=0.7,
        color=Colores,
        edgecolor='black',
        linewidth=0.5
    )

    # Configurar ejes.
    Ax.set_xlabel(Columna_Categoria, fontsize=12)
    Ax.set_ylabel(f'Media de {Variable}', fontsize=12)

    if Titulo is None:
        Titulo = f'Media de {Variable} por Categoría'

    Ax.set_title(Titulo, fontsize=14, fontweight='bold')

    if Escala_Y is not None:
        Ax.set_ylim(Escala_Y)

    # Añadir valores en barras.
    if Mostrar_Valores:
        for i, Barra in enumerate(Barras):
            Altura = Barra.get_height()
            N_Grupo = Estadisticas_Ordenadas.iloc[i]['N']

            if Mostrar_N:
                Texto = f'{Altura:.2f}\n(n={N_Grupo})'
            else:
                Texto = f'{Altura:.2f}'

            Ax.text(
                Barra.get_x() + Barra.get_width()/2.,
                Altura,
                Texto,
                ha='center',
                va='bottom',
                fontsize=9
            )

    # Mejorar diseño.
    plt.xticks(rotation=45, ha='right')
    Ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    # Guardar si se especifica ruta.
    if Ruta_Salida is not None:
        Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            Ruta_Salida,
            dpi=300,
            bbox_inches='tight'
        )
        print(f"  ✓ Gráfico guardado: {Ruta_Salida.name}")
    else:
        plt.show()

    plt.close()

    return Estadisticas_Ordenadas


# ============================================================
# GRÁFICO DE BARRAS COMPARATIVO
# ============================================================

def Grafico_Barras_Comparativo(
    Df_1: pd.DataFrame,
    Df_2: pd.DataFrame,
    Variable: str,
    Nombre_1: str = 'Grupo 1',
    Nombre_2: str = 'Grupo 2',
    Columna_Categoria: str = 'Categoria_PASO_2023',
    Titulo: str = None,
    Orden_Categorias: List[str] = None,
    Color_1: str = '#0078bf',
    Color_2: str = '#f65058',
    Ruta_Salida: Path = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    """
    Crea gráfico de barras comparando dos DataFrames
    (ej: Generales vs Ballotage).

    Parámetros:
    - Df_1: Primer DataFrame.
    - Df_2: Segundo DataFrame.
    - Variable: Variable a comparar.
    - Nombre_1: Nombre del primer grupo.
    - Nombre_2: Nombre del segundo grupo.
    - Columna_Categoria: Columna con categorías.
    - Titulo: Título del gráfico.
    - Orden_Categorias: Orden de categorías.
    - Color_1: Color para primer grupo.
    - Color_2: Color para segundo grupo.
    - Ruta_Salida: Path para guardar gráfico.

    Retorna:
    - Tupla con (Estadísticas_Df_1, Estadísticas_Df_2).

    """

    if Orden_Categorias is None:
        Orden_Categorias = ORDEN_CATEGORIAS

    # Calcular estadísticas para ambos DataFrames.
    Stats_1 = Df_1[
        [Columna_Categoria, Variable]
    ].dropna().groupby(Columna_Categoria)[Variable].agg([
        'mean',
        'sem',
        'count'
    ]).reset_index()

    Stats_2 = Df_2[
        [Columna_Categoria, Variable]
    ].dropna().groupby(Columna_Categoria)[Variable].agg([
        'mean',
        'sem',
        'count'
    ]).reset_index()

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=(12, 6))

    X = np.arange(len(Orden_Categorias))
    Ancho = 0.35

    # Filtrar y ordenar.
    Stats_1_Ord = Stats_1[
        Stats_1[Columna_Categoria].isin(Orden_Categorias)
    ]
    Stats_2_Ord = Stats_2[
        Stats_2[Columna_Categoria].isin(Orden_Categorias)
    ]

    Orden_Map = {
        cat: i for i, cat in enumerate(Orden_Categorias)
    }

    Stats_1_Ord = Stats_1_Ord.copy()
    Stats_2_Ord = Stats_2_Ord.copy()

    Stats_1_Ord['Orden'] = Stats_1_Ord[
        Columna_Categoria
    ].map(Orden_Map)
    Stats_2_Ord['Orden'] = Stats_2_Ord[
        Columna_Categoria
    ].map(Orden_Map)

    Stats_1_Final = Stats_1_Ord.sort_values('Orden')
    Stats_2_Final = Stats_2_Ord.sort_values('Orden')

    # Crear barras.
    Ax.bar(
        X - Ancho/2,
        Stats_1_Final['mean'],
        Ancho,
        yerr=Stats_1_Final['sem'],
        label=Nombre_1,
        capsize=5,
        alpha=0.7,
        color=Color_1
    )

    Ax.bar(
        X + Ancho/2,
        Stats_2_Final['mean'],
        Ancho,
        yerr=Stats_2_Final['sem'],
        label=Nombre_2,
        capsize=5,
        alpha=0.7,
        color=Color_2
    )

    # Configurar.
    Ax.set_xlabel(Columna_Categoria, fontsize=12)
    Ax.set_ylabel(f'Media de {Variable}', fontsize=12)

    if Titulo is None:
        Titulo = (
            f'Comparación {Variable}: '
            f'{Nombre_1} vs {Nombre_2}'
        )

    Ax.set_title(Titulo, fontsize=14, fontweight='bold')
    Ax.set_xticks(X)
    Ax.set_xticklabels(
        Orden_Categorias,
        rotation=45,
        ha='right'
    )
    Ax.legend()
    Ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    # Guardar si se especifica ruta.
    if Ruta_Salida is not None:
        Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            Ruta_Salida,
            dpi=300,
            bbox_inches='tight'
        )
        print(
            f"  ✓ Gráfico comparativo guardado: "
            f"{Ruta_Salida.name}"
        )
    else:
        plt.show()

    plt.close()

    return Stats_1_Final, Stats_2_Final


# ============================================================
# GRÁFICO DE BARRAS AGRUPADAS MÚLTIPLES
# ============================================================

def Grafico_Barras_Multiples(
    Df: pd.DataFrame,
    Variables: List[str],
    Columna_Categoria: str = 'Categoria_PASO_2023',
    Titulos_Variables: List[str] = None,
    Orden_Categorias: List[str] = None,
    Colores: List[str] = None,
    Filas: int = 2,
    Columnas: int = 2,
    Ruta_Salida: Path = None
) -> None:

    """
    Crea múltiples gráficos de barras en una cuadrícula.

    Parámetros:
    - Df: DataFrame con los datos.
    - Variables: Lista de variables a graficar.
    - Columna_Categoria: Columna con categorías.
    - Titulos_Variables: Títulos personalizados (None para
      automático).
    - Orden_Categorias: Orden de categorías.
    - Colores: Lista de colores.
    - Filas: Número de filas en la cuadrícula.
    - Columnas: Número de columnas en la cuadrícula.
    - Ruta_Salida: Path para guardar gráfico.

    """

    if Orden_Categorias is None:
        Orden_Categorias = ORDEN_CATEGORIAS

    # Crear figura con subplots.
    Fig, Axes = plt.subplots(
        Filas,
        Columnas,
        figsize=(Columnas * 6, Filas * 5)
    )

    # Aplanar array de axes si es necesario.
    if Filas * Columnas > 1:
        Axes = Axes.flatten()
    else:
        Axes = [Axes]

    for Idx, Variable in enumerate(Variables):
        if Idx >= len(Axes):
            break

        if Variable not in Df.columns:
            continue

        Ax = Axes[Idx]

        # Calcular estadísticas.
        Datos_Limpios = Df[
            [Columna_Categoria, Variable]
        ].dropna()

        if len(Datos_Limpios) == 0:
            Ax.text(
                0.5,
                0.5,
                f'Sin datos para\n{Variable}',
                ha='center',
                va='center',
                transform=Ax.transAxes
            )
            continue

        Stats = Datos_Limpios.groupby(
            Columna_Categoria
        )[Variable].agg(['mean', 'sem']).reset_index()

        # Filtrar y ordenar.
        Stats_Filt = Stats[
            Stats[Columna_Categoria].isin(Orden_Categorias)
        ]

        Orden_Map = {
            cat: i for i, cat in enumerate(Orden_Categorias)
        }
        Stats_Filt = Stats_Filt.copy()
        Stats_Filt['Orden'] = Stats_Filt[
            Columna_Categoria
        ].map(Orden_Map)
        Stats_Ord = Stats_Filt.sort_values('Orden')

        # Configurar colores.
        if Colores is None:
            Cols = [
                COLORES_CATEGORIAS.get(cat, 'steelblue')
                for cat in Stats_Ord[Columna_Categoria]
            ]
        else:
            Cols = Colores

        # Crear barras.
        Ax.bar(
            Stats_Ord[Columna_Categoria],
            Stats_Ord['mean'],
            yerr=Stats_Ord['sem'],
            capsize=3,
            alpha=0.7,
            color=Cols,
            edgecolor='black',
            linewidth=0.5
        )

        # Configurar.
        if Titulos_Variables and Idx < len(Titulos_Variables):
            Titulo = Titulos_Variables[Idx]
        else:
            Titulo = Variable

        Ax.set_title(Titulo, fontsize=11, fontweight='bold')
        Ax.set_xlabel('')
        Ax.set_ylabel('Media', fontsize=9)
        Ax.tick_params(axis='x', rotation=45, labelsize=8)
        Ax.grid(axis='y', alpha=0.3)

    # Ocultar subplots vacíos.
    for Idx in range(len(Variables), len(Axes)):
        Axes[Idx].axis('off')

    plt.tight_layout()

    # Guardar si se especifica ruta.
    if Ruta_Salida is not None:
        Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            Ruta_Salida,
            dpi=300,
            bbox_inches='tight'
        )
        print(f"  ✓ Gráfico múltiple guardado: {Ruta_Salida.name}")
    else:
        plt.show()

    plt.close()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Módulo de gráficos de barras cargado.")
