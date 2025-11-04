# ============================================================
# GRAFICOS_VIOLIN.PY
# ============================================================
# Módulo especializado en violin plots para visualización de
# distribuciones con densidad de probabilidad.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
# VIOLIN PLOT BÁSICO
# ============================================================

def Violin_Plot_Por_Categoria(
    Df: pd.DataFrame,
    Variable: str,
    Columna_Categoria: str = 'Categoria_PASO_2023',
    Titulo: str = None,
    Orden_Categorias: List[str] = None,
    Colores: dict = None,
    Escala_Y: Tuple[float, float] = None,
    Mostrar_Quartiles: bool = True,
    Tamano_Figura: Tuple[int, int] = (12, 6),
    Ruta_Salida: Path = None
) -> None:

    """
    Crea violin plot de una variable por categoría.

    Los violin plots combinan boxplot con kernel density
    estimation, mostrando la distribución completa de datos.

    Parámetros:
    - Df: DataFrame con los datos.
    - Variable: Nombre de la variable a graficar.
    - Columna_Categoria: Columna con categorías.
    - Titulo: Título del gráfico (None para automático).
    - Orden_Categorias: Orden de categorías (None usa
      ORDEN_CATEGORIAS).
    - Colores: Diccionario de colores por categoría.
    - Escala_Y: Tupla (min, max) para eje Y.
    - Mostrar_Quartiles: Si mostrar líneas de quartiles.
    - Tamano_Figura: Tupla (ancho, alto) en pulgadas.
    - Ruta_Salida: Path para guardar gráfico (None muestra).

    """

    # Filtrar datos válidos.
    Datos_Limpios = Df[[Columna_Categoria, Variable]].dropna()

    if len(Datos_Limpios) == 0:
        print(f"⚠️ No hay datos válidos para {Variable}")
        return

    # Configurar orden.
    if Orden_Categorias is None:
        Orden_Categorias = ORDEN_CATEGORIAS

    # Filtrar categorías válidas.
    Datos_Filtrados = Datos_Limpios[
        Datos_Limpios[Columna_Categoria].isin(
            Orden_Categorias
        )
    ]

    if len(Datos_Filtrados) == 0:
        print(
            f"⚠️ No hay datos para las categorías "
            f"especificadas"
        )
        return

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=Tamano_Figura)

    # Configurar paleta de colores.
    if Colores is None:
        Paleta = {
            cat: COLORES_CATEGORIAS.get(cat, 'steelblue')
            for cat in Orden_Categorias
        }
    else:
        Paleta = Colores

    # Determinar parámetro inner.
    if Mostrar_Quartiles:
        Inner = 'quartile'
    else:
        Inner = None

    # Crear violin plot.
    sns.violinplot(
        data=Datos_Filtrados,
        x=Columna_Categoria,
        y=Variable,
        order=Orden_Categorias,
        palette=Paleta,
        inner=Inner,
        ax=Ax
    )

    # Configurar.
    Ax.set_xlabel(Columna_Categoria, fontsize=12)
    Ax.set_ylabel(Variable, fontsize=12)

    if Titulo is None:
        Titulo = (
            f'Distribución de {Variable} por Categoría '
            f'(Violin Plot)'
        )

    Ax.set_title(Titulo, fontsize=14, fontweight='bold')

    if Escala_Y is not None:
        Ax.set_ylim(Escala_Y)

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
        print(f"  ✓ Violin plot guardado: {Ruta_Salida.name}")
    else:
        plt.show()

    plt.close()


# ============================================================
# VIOLIN PLOT DIVIDIDO (SPLIT)
# ============================================================

def Violin_Plot_Dividido(
    Df: pd.DataFrame,
    Variable: str,
    Columna_Categoria: str,
    Columna_Hue: str,
    Titulo: str = None,
    Orden_Categorias: List[str] = None,
    Ruta_Salida: Path = None
) -> None:

    """
    Crea violin plot dividido comparando dos grupos
    (ej: Generales vs Ballotage).

    Parámetros:
    - Df: DataFrame con los datos combinados.
    - Variable: Variable a graficar.
    - Columna_Categoria: Columna con categorías principales.
    - Columna_Hue: Columna con segunda agrupación
      (ej: 'Eleccion').
    - Titulo: Título del gráfico.
    - Orden_Categorias: Orden de categorías.
    - Ruta_Salida: Path para guardar gráfico.

    """

    # Filtrar datos válidos.
    Datos_Limpios = Df[
        [Columna_Categoria, Variable, Columna_Hue]
    ].dropna()

    if len(Datos_Limpios) == 0:
        print(f"⚠️ No hay datos válidos")
        return

    if Orden_Categorias is None:
        Orden_Categorias = ORDEN_CATEGORIAS

    Datos_Filtrados = Datos_Limpios[
        Datos_Limpios[Columna_Categoria].isin(
            Orden_Categorias
        )
    ]

    if len(Datos_Filtrados) == 0:
        print(f"⚠️ No hay datos para categorías")
        return

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=(12, 6))

    # Crear violin plot dividido.
    sns.violinplot(
        data=Datos_Filtrados,
        x=Columna_Categoria,
        y=Variable,
        hue=Columna_Hue,
        order=Orden_Categorias,
        split=True,
        inner='quartile',
        ax=Ax
    )

    # Configurar.
    Ax.set_xlabel(Columna_Categoria, fontsize=12)
    Ax.set_ylabel(Variable, fontsize=12)

    if Titulo is None:
        Titulo = (
            f'Comparación de {Variable} por '
            f'{Columna_Hue} (Violin Plot Dividido)'
        )

    Ax.set_title(Titulo, fontsize=14, fontweight='bold')

    plt.xticks(rotation=45, ha='right')
    Ax.grid(axis='y', alpha=0.3)
    Ax.legend(title=Columna_Hue)
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
            f"  ✓ Violin plot dividido guardado: "
            f"{Ruta_Salida.name}"
        )
    else:
        plt.show()

    plt.close()


# ============================================================
# VIOLIN PLOTS MÚLTIPLES
# ============================================================

def Violin_Plots_Multiples(
    Df: pd.DataFrame,
    Variables: List[str],
    Columna_Categoria: str = 'Categoria_PASO_2023',
    Titulos: List[str] = None,
    Orden_Categorias: List[str] = None,
    Filas: int = 2,
    Columnas: int = 2,
    Ruta_Salida: Path = None
) -> None:

    """
    Crea múltiples violin plots en una cuadrícula.

    Parámetros:
    - Df: DataFrame con los datos.
    - Variables: Lista de variables a graficar.
    - Columna_Categoria: Columna con categorías.
    - Titulos: Títulos personalizados para cada subplot.
    - Orden_Categorias: Orden de categorías.
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

    # Aplanar array de axes.
    if Filas * Columnas > 1:
        Axes = Axes.flatten()
    else:
        Axes = [Axes]

    # Paleta de colores.
    Paleta = {
        cat: COLORES_CATEGORIAS.get(cat, 'steelblue')
        for cat in Orden_Categorias
    }

    for Idx, Variable in enumerate(Variables):
        if Idx >= len(Axes):
            break

        if Variable not in Df.columns:
            continue

        Ax = Axes[Idx]

        # Filtrar datos.
        Datos = Df[
            [Columna_Categoria, Variable]
        ].dropna()

        Datos_Filt = Datos[
            Datos[Columna_Categoria].isin(Orden_Categorias)
        ]

        if len(Datos_Filt) == 0:
            Ax.text(
                0.5,
                0.5,
                f'Sin datos para\n{Variable}',
                ha='center',
                va='center',
                transform=Ax.transAxes
            )
            continue

        # Crear violin plot.
        sns.violinplot(
            data=Datos_Filt,
            x=Columna_Categoria,
            y=Variable,
            order=Orden_Categorias,
            palette=Paleta,
            inner='quartile',
            ax=Ax
        )

        # Configurar.
        if Titulos and Idx < len(Titulos):
            Titulo = Titulos[Idx]
        else:
            Titulo = Variable

        Ax.set_title(Titulo, fontsize=11, fontweight='bold')
        Ax.set_xlabel('')
        Ax.set_ylabel('')
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
        print(
            f"  ✓ Violin plots múltiples guardados: "
            f"{Ruta_Salida.name}"
        )
    else:
        plt.show()

    plt.close()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Módulo de violin plots cargado.")