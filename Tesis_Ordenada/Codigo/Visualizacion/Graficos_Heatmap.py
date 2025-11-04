# ============================================================
# GRAFICOS_HEATMAP.PY
# ============================================================
# Módulo especializado en heatmaps para visualización de
# matrices de correlación y datos tabulares.
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
# HEATMAP BÁSICO DE CORRELACIÓN
# ============================================================

def Heatmap_Correlacion(
    Matriz_Correlacion: pd.DataFrame,
    Titulo: str = None,
    Mostrar_Valores: bool = True,
    Formato_Valores: str = '.2f',
    Mapa_Colores: str = 'RdBu_r',
    Escala_Valores: Tuple[float, float] = (-1, 1),
    Tamano_Figura: Tuple[int, int] = (12, 10),
    Ruta_Salida: Path = None
) -> None:

    """
    Crea heatmap de matriz de correlación.

    Parámetros:
    - Matriz_Correlacion: DataFrame con correlaciones.
    - Titulo: Título del gráfico (None para automático).
    - Mostrar_Valores: Si mostrar valores numéricos en celdas.
    - Formato_Valores: Formato de números (ej: '.2f', '.3f').
    - Mapa_Colores: Nombre del colormap ('RdBu_r', 'coolwarm',
      'viridis', etc.).
    - Escala_Valores: Tupla (min, max) para escala de colores.
    - Tamano_Figura: Tupla (ancho, alto) en pulgadas.
    - Ruta_Salida: Path para guardar gráfico (None muestra).

    """

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=Tamano_Figura)

    # Crear heatmap.
    sns.heatmap(
        Matriz_Correlacion,
        annot=Mostrar_Valores,
        fmt=Formato_Valores,
        cmap=Mapa_Colores,
        center=0,
        vmin=Escala_Valores[0],
        vmax=Escala_Valores[1],
        square=True,
        linewidths=0.5,
        cbar_kws={'label': 'Correlación'},
        ax=Ax
    )

    # Configurar.
    if Titulo is None:
        Titulo = 'Matriz de Correlación'

    Ax.set_title(Titulo, fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()

    # Guardar si se especifica ruta.
    if Ruta_Salida is not None:
        Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            Ruta_Salida,
            dpi=300,
            bbox_inches='tight'
        )
        print(f"  ✓ Heatmap guardado: {Ruta_Salida.name}")
    else:
        plt.show()

    plt.close()


# ============================================================
# HEATMAP DE SUBMATRIZ (PREDICTORES VS OUTCOMES)
# ============================================================

def Heatmap_Predictores_Vs_Outcomes(
    Matriz_Correlacion: pd.DataFrame,
    Variables_Filas: List[str],
    Variables_Columnas: List[str],
    Titulo: str = None,
    Mostrar_Valores: bool = True,
    Tamano_Figura: Tuple[int, int] = (16, 6),
    Ruta_Salida: Path = None
) -> None:

    """
    Crea heatmap de submatriz (filas vs columnas específicas).

    Útil para visualizar predictores vs outcomes.

    Parámetros:
    - Matriz_Correlacion: DataFrame con correlaciones completas.
    - Variables_Filas: Lista de variables para filas.
    - Variables_Columnas: Lista de variables para columnas.
    - Titulo: Título del gráfico.
    - Mostrar_Valores: Si mostrar valores en celdas.
    - Tamano_Figura: Tupla (ancho, alto) en pulgadas.
    - Ruta_Salida: Path para guardar gráfico.

    """

    # Filtrar variables disponibles.
    Filas_Disponibles = [
        v for v in Variables_Filas
        if v in Matriz_Correlacion.index
    ]
    Columnas_Disponibles = [
        v for v in Variables_Columnas
        if v in Matriz_Correlacion.columns
    ]

    if not Filas_Disponibles or not Columnas_Disponibles:
        print(
            "⚠️ No hay suficientes variables para crear "
            "submatriz"
        )
        return

    # Extraer submatriz.
    Submatriz = Matriz_Correlacion.loc[
        Filas_Disponibles,
        Columnas_Disponibles
    ]

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=Tamano_Figura)

    # Crear heatmap.
    sns.heatmap(
        Submatriz,
        annot=Mostrar_Valores,
        fmt='.3f',
        cmap='RdBu_r',
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        cbar_kws={'label': 'Correlación'},
        ax=Ax
    )

    # Configurar.
    if Titulo is None:
        Titulo = 'Predictores vs Outcomes'

    Ax.set_title(
        Titulo,
        fontsize=14,
        fontweight='bold',
        pad=15
    )
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()

    # Guardar si se especifica ruta.
    if Ruta_Salida is not None:
        Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            Ruta_Salida,
            dpi=300,
            bbox_inches='tight'
        )
        print(f"  ✓ Heatmap guardado: {Ruta_Salida.name}")
    else:
        plt.show()

    plt.close()


# ============================================================
# HEATMAP TRIANGULAR (EVITA REDUNDANCIA)
# ============================================================

def Heatmap_Triangular(
    Matriz_Correlacion: pd.DataFrame,
    Titulo: str = None,
    Mitad: str = 'inferior',
    Tamano_Figura: Tuple[int, int] = (12, 10),
    Ruta_Salida: Path = None
) -> None:

    """
    Crea heatmap mostrando solo mitad triangular de la matriz.

    Parámetros:
    - Matriz_Correlacion: DataFrame con correlaciones.
    - Titulo: Título del gráfico.
    - Mitad: 'inferior' o 'superior' para elegir triángulo.
    - Tamano_Figura: Tupla (ancho, alto) en pulgadas.
    - Ruta_Salida: Path para guardar gráfico.

    """

    # Crear máscara.
    Mascara = np.zeros_like(
        Matriz_Correlacion,
        dtype=bool
    )

    if Mitad == 'superior':
        Mascara[np.tril_indices_from(Mascara)] = True
    else:  # inferior
        Mascara[np.triu_indices_from(Mascara)] = True

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=Tamano_Figura)

    # Crear heatmap.
    sns.heatmap(
        Matriz_Correlacion,
        mask=Mascara,
        annot=True,
        fmt='.2f',
        cmap='RdBu_r',
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={'label': 'Correlación'},
        ax=Ax
    )

    # Configurar.
    if Titulo is None:
        Titulo = f'Matriz de Correlación (Triángulo {Mitad})'

    Ax.set_title(Titulo, fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()

    # Guardar si se especifica ruta.
    if Ruta_Salida is not None:
        Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            Ruta_Salida,
            dpi=300,
            bbox_inches='tight'
        )
        print(f"  ✓ Heatmap guardado: {Ruta_Salida.name}")
    else:
        plt.show()

    plt.close()


# ============================================================
# HEATMAP DE DATOS AGRUPADOS
# ============================================================

def Heatmap_Datos_Agrupados(
    Df: pd.DataFrame,
    Variable_Filas: str,
    Variable_Columnas: str,
    Variable_Valores: str,
    Funcion_Agregacion: str = 'mean',
    Titulo: str = None,
    Tamano_Figura: Tuple[int, int] = (10, 8),
    Ruta_Salida: Path = None
) -> None:

    """
    Crea heatmap de datos agrupados (ej: medias por categoría).

    Parámetros:
    - Df: DataFrame con los datos.
    - Variable_Filas: Variable para filas del heatmap.
    - Variable_Columnas: Variable para columnas del heatmap.
    - Variable_Valores: Variable numérica a agregar.
    - Funcion_Agregacion: Función de agregación ('mean', 'median',
      'sum', 'count').
    - Titulo: Título del gráfico.
    - Tamano_Figura: Tupla (ancho, alto) en pulgadas.
    - Ruta_Salida: Path para guardar gráfico.

    """

    # Crear tabla pivote.
    Tabla_Pivote = pd.pivot_table(
        Df,
        values=Variable_Valores,
        index=Variable_Filas,
        columns=Variable_Columnas,
        aggfunc=Funcion_Agregacion
    )

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=Tamano_Figura)

    # Crear heatmap.
    sns.heatmap(
        Tabla_Pivote,
        annot=True,
        fmt='.2f',
        cmap='YlOrRd',
        linewidths=0.5,
        cbar_kws={'label': Variable_Valores},
        ax=Ax
    )

    # Configurar.
    if Titulo is None:
        Titulo = (
            f'{Funcion_Agregacion.capitalize()} de '
            f'{Variable_Valores}'
        )

    Ax.set_title(Titulo, fontsize=14, fontweight='bold', pad=20)
    Ax.set_xlabel(Variable_Columnas, fontsize=12)
    Ax.set_ylabel(Variable_Filas, fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()

    # Guardar si se especifica ruta.
    if Ruta_Salida is not None:
        Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            Ruta_Salida,
            dpi=300,
            bbox_inches='tight'
        )
        print(f"  ✓ Heatmap guardado: {Ruta_Salida.name}")
    else:
        plt.show()

    plt.close()


# ============================================================
# HEATMAP CON CLUSTERMAP (AGRUPACIÓN JERÁRQUICA)
# ============================================================

def Heatmap_Con_Clustering(
    Matriz_Datos: pd.DataFrame,
    Titulo: str = None,
    Metodo_Clustering: str = 'average',
    Metrica_Distancia: str = 'euclidean',
    Tamano_Figura: Tuple[int, int] = (12, 12),
    Ruta_Salida: Path = None
) -> None:

    """
    Crea heatmap con agrupación jerárquica (clustermap).

    Parámetros:
    - Matriz_Datos: DataFrame con datos a visualizar.
    - Titulo: Título del gráfico.
    - Metodo_Clustering: Método de agrupación ('average',
      'complete', 'single', 'ward').
    - Metrica_Distancia: Métrica de distancia ('euclidean',
      'correlation', 'cosine').
    - Tamano_Figura: Tupla (ancho, alto) en pulgadas.
    - Ruta_Salida: Path para guardar gráfico.

    """

    # Crear clustermap.
    Cluster = sns.clustermap(
        Matriz_Datos,
        method=Metodo_Clustering,
        metric=Metrica_Distancia,
        cmap='RdBu_r',
        center=0,
        annot=True,
        fmt='.2f',
        figsize=Tamano_Figura,
        linewidths=0.5,
        cbar_kws={'label': 'Valor'}
    )

    # Rotar etiquetas.
    plt.setp(
        Cluster.ax_heatmap.xaxis.get_majorticklabels(),
        rotation=45,
        ha='right',
        fontsize=8
    )
    plt.setp(
        Cluster.ax_heatmap.yaxis.get_majorticklabels(),
        rotation=0,
        fontsize=8
    )

    # Título.
    if Titulo is not None:
        Cluster.fig.suptitle(
            Titulo,
            fontsize=14,
            fontweight='bold',
            y=0.98
        )

    # Guardar si se especifica ruta.
    if Ruta_Salida is not None:
        Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            Ruta_Salida,
            dpi=300,
            bbox_inches='tight'
        )
        print(f"  ✓ Clustermap guardado: {Ruta_Salida.name}")
    else:
        plt.show()

    plt.close()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Módulo de heatmaps cargado.")
