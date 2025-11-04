# ============================================================
# LIMPIEZA_DATOS.PY
# ============================================================
# Módulo para limpieza y filtrado de datos.
# Incluye eliminación de outliers por categoría y por tiempos
# de respuesta según criterios estadísticos.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from pathlib import Path
import sys
from typing import List

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import (
    CATEGORIAS_EXCLUIR,
    COL_CATEGORIA,
    NUM_DESVIACIONES_OUTLIERS
)
from Funciones_Comunes import (
    Eliminar_Filas_Por_Desviacion_Estandar
)


# ============================================================
# FUNCIONES DE FILTRADO POR CATEGORIA
# ============================================================

def Filtrar_Categorias_Invalidas(
    Df: pd.DataFrame,
    Nombre_Columna_Categoria: str = COL_CATEGORIA,
    Categorias_A_Excluir: List[str] = None
) -> pd.DataFrame:

    """
    Filtra participantes con categorías ideológicas inválidas
    o problemáticas.

    Las categorías excluidas típicamente incluyen:
    - 'Other': Participantes sin categoría ideológica clara.
    - 'No apply': Sin información ideológica.
    - 'No response': Sin respuesta a clasificación.
    - 'Blank': Respuestas en blanco.

    Parámetros:
    - Df: DataFrame a filtrar.
    - Nombre_Columna_Categoria: Nombre de la columna con
      categoría ideológica.
    - Categorias_A_Excluir: Lista de categorías a eliminar.
      Si es None, usa CATEGORIAS_EXCLUIR de Configuracion.

    Retorna:
    - DataFrame filtrado sin categorías inválidas.

    """

    if Nombre_Columna_Categoria not in Df.columns:
        print(
            f"⚠️ Columna '{Nombre_Columna_Categoria}' "
            f"no encontrada."
        )
        print("   Retornando DataFrame sin cambios.")
        return Df

    if Categorias_A_Excluir is None:
        Categorias_A_Excluir = CATEGORIAS_EXCLUIR

    N_Inicial = len(Df)

    # Contar por categoría antes del filtro.
    print(f"\nDistribución ANTES del filtro:")
    Conteo_Antes = Df[Nombre_Columna_Categoria].value_counts()
    for Cat, Cuenta in Conteo_Antes.items():
        if Cat in Categorias_A_Excluir:
            print(f"  ❌ {Cat}: {Cuenta} (será eliminado)")
        else:
            print(f"  ✅ {Cat}: {Cuenta}")

    # Aplicar filtro.
    Df_Filtrado = Df[
        ~Df[Nombre_Columna_Categoria].isin(Categorias_A_Excluir)
    ].copy()

    N_Final = len(Df_Filtrado)
    N_Eliminadas = N_Inicial - N_Final

    print(f"\nResultado del filtro por categoría:")
    print(f"  Filas iniciales: {N_Inicial}")
    print(f"  Filas eliminadas: {N_Eliminadas}")
    print(f"  Filas finales: {N_Final}")
    print(
        f"  Porcentaje eliminado: "
        f"{(N_Eliminadas/N_Inicial)*100:.2f}%"
    )

    return Df_Filtrado


# ============================================================
# FUNCIONES DE ELIMINACION WARM-UP
# ============================================================

def Eliminar_Primeros_Items_Warm_Up(
    Df: pd.DataFrame,
    Columna_Orden: str = 'Orden_IP_Items_Asociados',
    Num_Items_Unicos: int = 3
) -> pd.DataFrame:

    """
    Elimina datos de los primeros N items únicos de cada
    participante para controlar efecto de aprendizaje (warm-up).

    El algoritmo:
    1. Lee la columna de orden de presentación de items.
    2. Recorre secuencialmente hasta encontrar N números de
       item únicos (por defecto 3).
    3. Elimina (setea NaN) TODOS los datos de esos N items,
       tanto _Izq como _Der, en _Respuesta, _Tiempo y _Candidato.

    Ejemplo: Si orden es ['25_Izq', '3_Izq', '27_Izq', ...],
    elimina items 25, 3 y 27 (ambas direcciones).

    Parámetros:
    - Df: DataFrame con datos de items.
    - Columna_Orden: Nombre de columna con orden de
      presentación.
    - Num_Items_Unicos: Cantidad de items únicos a eliminar
      (por defecto 3).

    Retorna:
    - DataFrame con primeros items eliminados (NaN).

    """

    if Columna_Orden not in Df.columns:
        print(
            f"⚠️ Columna '{Columna_Orden}' no encontrada."
        )
        print("   Retornando DataFrame sin cambios.")
        return Df

    N_Inicial = len(Df)
    Df_Modificado = Df.copy()

    # Sufijos de columnas a eliminar.
    Sufijos = ['_Respuesta', '_Candidato', '_Tiempo']

    Total_Datos_Eliminados = 0
    Participantes_Procesados = 0

    print(
        f"\nEliminando primeros {Num_Items_Unicos} items "
        f"únicos (warm-up)..."
    )

    # Iterar por cada participante.
    for Index, Fila in Df_Modificado.iterrows():
        Orden_IP_Items = Fila[Columna_Orden]

        # Verificar que la lista sea válida.
        if not isinstance(Orden_IP_Items, list) or len(
            Orden_IP_Items
        ) == 0:
            continue

        Participantes_Procesados += 1

        # Estrategia: Tomar items hasta obtener N números únicos.
        Numeros_IP_Unicos = set()
        Items_Procesados = []

        # Recorrer orden hasta obtener N números únicos.
        for Item in Orden_IP_Items:
            if isinstance(Item, str) and '_' in Item:
                Numero = Item.split('_')[0]  # Extraer número.

                Items_Procesados.append(Item)
                Numeros_IP_Unicos.add(Numero)

                # Parar cuando tengamos N números únicos.
                if len(Numeros_IP_Unicos) >= Num_Items_Unicos:
                    break

        # Eliminar datos para los N números únicos encontrados.
        for Numero in Numeros_IP_Unicos:
            for Direccion in ['_Izq', '_Der']:
                for Sufijo in Sufijos:
                    # Construir nombre de columna.
                    Columna = (
                        f'IP_Item_{Numero}{Direccion}{Sufijo}'
                    )

                    # Si la columna existe, eliminar dato.
                    if Columna in Df_Modificado.columns:
                        if pd.notna(Df_Modificado.at[Index, Columna]):
                            Df_Modificado.at[Index, Columna] = pd.NA
                            Total_Datos_Eliminados += 1

    print(
        f"✓ Participantes procesados: {Participantes_Procesados}"
    )
    print(
        f"✓ Datos eliminados (warm-up): {Total_Datos_Eliminados}"
    )
    print(
        f"✓ Promedio por participante: "
        f"{Total_Datos_Eliminados/Participantes_Procesados:.1f}"
    )

    return Df_Modificado


# ============================================================
# FUNCIONES DE FILTRADO POR TIEMPOS
# ============================================================

def Obtener_Columnas_Tiempo(Df: pd.DataFrame) -> List[str]:

    """
    Identifica todas las columnas de tiempo de respuesta
    en el DataFrame.

    Busca columnas que contengan:
    - 'IP_Item' Y '_Tiempo'
    - Incluye base, izquierda y derecha.

    Parámetros:
    - Df: DataFrame a analizar.

    Retorna:
    - Lista de nombres de columnas de tiempo.

    """

    Todas_Columnas = list(Df.columns)

    # Filtrar columnas de tiempo.
    Columnas_Tiempo = [
        Col for Col in Todas_Columnas
        if 'IP_Item' in Col and '_Tiempo' in Col
    ]

    print(f"\nColumnas de tiempo identificadas: {len(Columnas_Tiempo)}")
    print(f"  - Base (sin asociar): {len([c for c in Columnas_Tiempo if '_Izq' not in c and '_Der' not in c])}")
    print(f"  - Asociadas izquierda: {len([c for c in Columnas_Tiempo if '_Izq' in c])}")
    print(f"  - Asociadas derecha: {len([c for c in Columnas_Tiempo if '_Der' in c])}")

    return Columnas_Tiempo


def Filtrar_Outliers_Por_Tiempo(
    Df: pd.DataFrame,
    Numero_Desviaciones: int = NUM_DESVIACIONES_OUTLIERS,
    Columnas_Tiempo: List[str] = None
) -> pd.DataFrame:

    """
    Elimina filas donde algún tiempo de respuesta exceda
    N desviaciones estándar desde la media global.

    Criterio: Media + (N × Desviación_Estándar) calculado
    sobre TODOS los tiempos de TODOS los participantes.

    Parámetros:
    - Df: DataFrame a filtrar.
    - Numero_Desviaciones: Umbral en desviaciones estándar
      (por defecto 3).
    - Columnas_Tiempo: Lista de columnas a analizar.
      Si es None, se detectan automáticamente.

    Retorna:
    - DataFrame filtrado sin outliers de tiempo.

    """

    if Columnas_Tiempo is None:
        Columnas_Tiempo = Obtener_Columnas_Tiempo(Df)

    if not Columnas_Tiempo:
        print("⚠️ No se encontraron columnas de tiempo.")
        print("   Retornando DataFrame sin cambios.")
        return Df

    N_Inicial = len(Df)

    print(
        f"\nAplicando filtro de outliers por tiempo "
        f"({Numero_Desviaciones} desv. est.)..."
    )

    # Usar función existente de Funciones_Comunes.
    Df_Filtrado = Eliminar_Filas_Por_Desviacion_Estandar(
        Df,
        Columnas_Tiempo,
        Numero_Desviaciones
    )

    N_Final = len(Df_Filtrado)
    N_Eliminadas = N_Inicial - N_Final

    print(f"\nResultado del filtro por tiempos:")
    print(f"  Filas iniciales: {N_Inicial}")
    print(f"  Filas eliminadas: {N_Eliminadas}")
    print(f"  Filas finales: {N_Final}")
    print(
        f"  Porcentaje eliminado: "
        f"{(N_Eliminadas/N_Inicial)*100:.2f}%"
    )

    return Df_Filtrado


# ============================================================
# FUNCION INTEGRADA DE LIMPIEZA COMPLETA
# ============================================================

def Limpiar_Datos_Completo(
    Df: pd.DataFrame,
    Eliminar_Warm_Up: bool = True,
    Filtrar_Categorias: bool = True,
    Filtrar_Tiempos: bool = True,
    Num_Items_Warm_Up: int = 3,
    Numero_Desviaciones: int = NUM_DESVIACIONES_OUTLIERS,
    Nombre_Columna_Categoria: str = COL_CATEGORIA,
    Categorias_A_Excluir: List[str] = None,
    Columnas_Tiempo: List[str] = None
) -> pd.DataFrame:

    """
    Aplica todos los filtros de limpieza de datos en
    secuencia ordenada.

    Orden de limpieza:
    0. Eliminación de primeros items (warm-up).
    1. Filtro por categorías inválidas.
    2. Filtro por outliers de tiempo.

    Parámetros:
    - Df: DataFrame a limpiar.
    - Eliminar_Warm_Up: Si eliminar primeros items (warm-up).
    - Filtrar_Categorias: Si aplicar filtro de categorías.
    - Filtrar_Tiempos: Si aplicar filtro de tiempos.
    - Num_Items_Warm_Up: Cantidad de items únicos a eliminar
      en warm-up.
    - Numero_Desviaciones: Umbral para outliers de tiempo.
    - Nombre_Columna_Categoria: Columna de categoría.
    - Categorias_A_Excluir: Categorías a eliminar.
    - Columnas_Tiempo: Columnas de tiempo específicas.

    Retorna:
    - DataFrame completamente limpio.

    """

    print("\n" + "="*70)
    print("LIMPIEZA COMPLETA DE DATOS")
    print("="*70)

    N_Inicial = len(Df)
    print(f"\nFilas iniciales: {N_Inicial}")

    Df_Limpio = Df.copy()

    # Paso 0: Eliminar warm-up.
    if Eliminar_Warm_Up:
        print("\n" + "-"*70)
        print("PASO 0: ELIMINACIÓN WARM-UP (PRIMEROS ITEMS)")
        print("-"*70)

        Df_Limpio = Eliminar_Primeros_Items_Warm_Up(
            Df_Limpio,
            Num_Items_Unicos=Num_Items_Warm_Up
        )

    # Paso 1: Filtrar categorías.
    if Filtrar_Categorias:
        print("\n" + "-"*70)
        print("PASO 1: FILTRADO POR CATEGORÍA")
        print("-"*70)

        Df_Limpio = Filtrar_Categorias_Invalidas(
            Df_Limpio,
            Nombre_Columna_Categoria,
            Categorias_A_Excluir
        )

    # Paso 2: Filtrar outliers de tiempo.
    if Filtrar_Tiempos:
        print("\n" + "-"*70)
        print("PASO 2: FILTRADO POR OUTLIERS DE TIEMPO")
        print("-"*70)

        Df_Limpio = Filtrar_Outliers_Por_Tiempo(
            Df_Limpio,
            Numero_Desviaciones,
            Columnas_Tiempo
        )

    # Resumen final.
    N_Final = len(Df_Limpio)
    N_Total_Eliminadas = N_Inicial - N_Final

    print("\n" + "="*70)
    print("RESUMEN DE LIMPIEZA COMPLETA")
    print("="*70)
    print(f"Filas iniciales: {N_Inicial}")
    print(f"Filas finales: {N_Final}")
    print(f"Total eliminadas: {N_Total_Eliminadas}")
    print(
        f"Porcentaje retenido: "
        f"{(N_Final/N_Inicial)*100:.2f}%"
    )
    print("="*70 + "\n")

    return Df_Limpio


# ============================================================
# FUNCION WRAPPER PARA DICCIONARIOS
# ============================================================

def Limpiar_Diccionario_Dataframes(
    Diccionario_Dfs: dict,
    **kwargs
) -> dict:

    """
    Aplica limpieza completa a todos los DataFrames en un
    diccionario.

    Parámetros:
    - Diccionario_Dfs: Dict con DataFrames a limpiar.
    - **kwargs: Parámetros para Limpiar_Datos_Completo().

    Retorna:
    - Diccionario con DataFrames limpios.

    """

    print("\n" + "="*70)
    print("LIMPIEZA DE MÚLTIPLES DATAFRAMES")
    print("="*70)

    Diccionario_Limpio = {}

    for Nombre_Df, Df in Diccionario_Dfs.items():
        print(f"\n{'#'*70}")
        print(f"PROCESANDO: {Nombre_Df}")
        print(f"{'#'*70}")

        Diccionario_Limpio[Nombre_Df] = Limpiar_Datos_Completo(
            Df,
            **kwargs
        )

    print("\n" + "="*70)
    print("LIMPIEZA DE TODOS LOS DATAFRAMES COMPLETADA")
    print("="*70 + "\n")

    return Diccionario_Limpio


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    print("Módulo de limpieza de datos cargado.")
