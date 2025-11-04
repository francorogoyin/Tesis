# ============================================================
# GRAFICOS_CLEVELAND.PY
# ============================================================
# Generación de gráficos de Cleveland (dot plots) para
# visualizar diferencias entre grupos.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import (
    RUTA_GRAFICOS_CLEVELAND,
    DPI_GRAFICOS,
    COLORES_CATEGORIAS
)


# ============================================================
# FUNCIONES DE VISUALIZACION
# ============================================================

def Crear_Cleveland_Comparativo(
    Df_Resultados: pd.DataFrame,
    Titulo: str,
    Nombre_Archivo: str
) -> None:

    """
    Crea un gráfico de Cleveland comparando diferencias entre
    grupos.

    Parámetros:
    - Df_Resultados: DataFrame con columnas 'Item',
      'Diferencia', 'Grupo'.
    - Titulo: Título del gráfico.
    - Nombre_Archivo: Nombre del archivo de salida (sin ext).

    """

    # Crear figura.
    Fig, Ax = plt.subplots(figsize=(12, 8))

    # Ordenar por diferencia.
    Df_Ordenado = Df_Resultados.sort_values('Diferencia')

    # Crear gráfico de puntos.
    sns.scatterplot(
        data=Df_Ordenado,
        x='Diferencia',
        y='Item',
        hue='Grupo',
        s=200,
        ax=Ax,
        palette='Set2'
    )

    # Añadir línea vertical en 0.
    Ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)

    # Configurar etiquetas.
    Ax.set_xlabel('Diferencia', fontsize=12)
    Ax.set_ylabel('Item', fontsize=12)
    Ax.set_title(Titulo, fontsize=14, pad=20)

    # Ajustar layout.
    plt.tight_layout()

    # Guardar en múltiples formatos.
    for Formato in ['png', 'svg']:
        Ruta_Salida = (
            RUTA_GRAFICOS_CLEVELAND /
            f"{Nombre_Archivo}.{Formato}"
        )
        Fig.savefig(
            Ruta_Salida,
            format=Formato,
            dpi=DPI_GRAFICOS,
            bbox_inches='tight'
        )

    print(f"✓ Gráfico Cleveland guardado: {Nombre_Archivo}")
    plt.close()


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    print("Módulo de gráficos de Cleveland cargado.")
