# ============================================================
# RELLENO_MEDIANAS.PY
# ============================================================
# Relleno de valores NaN con mediana del grupo ideológico.
# Aplica imputación por categoría política para items IP
# base y asociados a candidatos.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path
import sys
from typing import Dict

# Agregar ruta de Utilidades al path.
sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import (
    ITEMS_PROGRESISTAS,
    ITEMS_CONSERVADORES
)


# ============================================================
# CONSTANTES
# ============================================================

# Items a procesar (todos los items IP).
ITEMS_TODOS = [3, 4, 5, 6, 7, 8, 9, 10, 11, 16,
               19, 20, 22, 23, 24, 25, 27, 28, 29, 30]

# Variable de agrupación.
VARIABLE_AGRUPACION = 'Categoria_PASO_2023'


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def Crear_Columnas_Originales(
    Df: pd.DataFrame,
    Tipo_Variables: str = 'no_asociadas'
) -> pd.DataFrame:

    """
    Crea copias de seguridad de columnas antes del relleno.

    Parámetros:
    - Df: DataFrame a procesar.
    - Tipo_Variables: 'no_asociadas' o 'asociadas'.

    Retorna:
    - DataFrame con columnas _Original agregadas.

    """

    Df_Resultado = Df.copy()

    if Tipo_Variables == 'no_asociadas':
        # Variables sin asociar (Respuesta y Tiempo base).
        Patron_Columnas = (
            lambda col: col.startswith('IP_Item_') and
            ('_Respuesta' in col or '_Tiempo' in col) and
            '_Izq' not in col and
            '_Der' not in col and
            not col.endswith('_Original')
        )
    else:
        # Variables asociadas (Izq/Der).
        Patron_Columnas = (
            lambda col: 'IP_Item_' in col and
            ('_Izq_' in col or '_Der_' in col) and
            ('Respuesta' in col or 'Tiempo' in col) and
            not col.endswith('_Original')
        )

    for Columna in Df_Resultado.columns:
        if Patron_Columnas(Columna):
            Columna_Original = f'{Columna}_Original'

            if Columna_Original not in Df_Resultado.columns:
                Df_Resultado[Columna_Original] = (
                    Df_Resultado[Columna]
                )

    return Df_Resultado


def Convertir_A_Numerico(
    Df: pd.DataFrame,
    Columnas: list
) -> pd.DataFrame:

    """
    Convierte columnas a tipo numérico.

    Parámetros:
    - Df: DataFrame a procesar.
    - Columnas: Lista de nombres de columnas.

    Retorna:
    - DataFrame con columnas convertidas.

    """

    Df_Resultado = Df.copy()

    for Columna in Columnas:
        if Columna in Df_Resultado.columns:
            Df_Resultado[Columna] = pd.to_numeric(
                Df_Resultado[Columna],
                errors='coerce'
            )

    return Df_Resultado


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def Rellenar_Medianas_IP_No_Asociados(
    Df: pd.DataFrame,
    Variable_Agrupacion: str = VARIABLE_AGRUPACION,
    Crear_Backup: bool = True
) -> pd.DataFrame:

    """
    Rellena valores NaN en variables IP no asociadas con
    la mediana del grupo ideológico.

    Proceso:
    1. Crear columnas _Original (backup).
    2. Convertir columnas a numérico.
    3. Generar listas de columnas a procesar.
    4. Rellenar con groupby().transform(fillna(median())).

    Parámetros:
    - Df: DataFrame con datos procesados.
    - Variable_Agrupacion: Columna para agrupar
      (default: Categoria_PASO_2023).
    - Crear_Backup: Si crear columnas _Original.

    Retorna:
    - DataFrame con NaN rellenados.

    """

    print("\n" + "="*60)
    print("RELLENO DE MEDIANAS - ITEMS NO ASOCIADOS")
    print("="*60)

    Df_Resultado = Df.copy()

    # Verificar que existe la columna de agrupación.
    if Variable_Agrupacion not in Df_Resultado.columns:
        print(f"✗ Error: Columna '{Variable_Agrupacion}' "
              f"no encontrada.")
        return Df_Resultado

    # Paso 1: Crear columnas originales (backup).
    if Crear_Backup:
        print("Paso 1: Creando backup de columnas...")
        Df_Resultado = Crear_Columnas_Originales(
            Df_Resultado,
            'no_asociadas'
        )
        print("✓ Backup creado")

    # Paso 2: Generar listas de columnas.
    Items_Progresistas_Respuesta = [
        f'IP_Item_{Item}_Respuesta'
        for Item in ITEMS_PROGRESISTAS
    ]
    Items_Progresistas_Tiempo = [
        f'IP_Item_{Item}_Tiempo'
        for Item in ITEMS_PROGRESISTAS
    ]
    Items_Conservadores_Respuesta = [
        f'IP_Item_{Item}_Respuesta'
        for Item in ITEMS_CONSERVADORES
    ]
    Items_Conservadores_Tiempo = [
        f'IP_Item_{Item}_Tiempo'
        for Item in ITEMS_CONSERVADORES
    ]

    Items_Sin_Asociacion = (
        Items_Progresistas_Respuesta +
        Items_Progresistas_Tiempo +
        Items_Conservadores_Respuesta +
        Items_Conservadores_Tiempo
    )

    # Paso 3: Convertir a numérico.
    print("Paso 2: Convirtiendo columnas a numérico...")
    Df_Resultado = Convertir_A_Numerico(
        Df_Resultado,
        Items_Sin_Asociacion
    )
    print("✓ Conversión completada")

    # Paso 4: Reporte ANTES del relleno.
    print("\nPaso 3: Reporte ANTES del relleno:")
    Total_Faltantes_Antes = 0

    for Columna in Items_Sin_Asociacion:
        if Columna in Df_Resultado.columns:
            Faltantes = Df_Resultado[Columna].isna().sum()
            Total_Faltantes_Antes += Faltantes

    print(f"  Total NaN: {Total_Faltantes_Antes}")

    # Paso 5: Rellenar con mediana por grupo.
    print("\nPaso 4: Rellenando con mediana por grupo...")
    Columnas_Procesadas = 0

    for Columna in Items_Sin_Asociacion:
        if Columna in Df_Resultado.columns:
            Df_Resultado[Columna] = (
                Df_Resultado
                .groupby(Variable_Agrupacion)[Columna]
                .transform(
                    lambda Grupo: Grupo.fillna(Grupo.median())
                )
            )
            Columnas_Procesadas += 1

    print(f"✓ {Columnas_Procesadas} columnas procesadas")

    # Paso 6: Reporte DESPUÉS del relleno.
    print("\nPaso 5: Reporte DESPUÉS del relleno:")
    Total_Faltantes_Despues = 0

    for Columna in Items_Sin_Asociacion:
        if Columna in Df_Resultado.columns:
            Faltantes = Df_Resultado[Columna].isna().sum()
            Total_Faltantes_Despues += Faltantes

    print(f"  Total NaN restantes: {Total_Faltantes_Despues}")
    print(f"  NaN rellenados: "
          f"{Total_Faltantes_Antes - Total_Faltantes_Despues}")

    print("\n" + "="*60)
    print("✓ RELLENO DE ITEMS NO ASOCIADOS COMPLETADO")
    print("="*60)

    return Df_Resultado


def Rellenar_Medianas_IP_Asociados(
    Df: pd.DataFrame,
    Variable_Agrupacion: str = VARIABLE_AGRUPACION,
    Crear_Backup: bool = True
) -> pd.DataFrame:

    """
    Rellena valores NaN en variables IP asociadas (Izq/Der)
    con la mediana del grupo ideológico.

    Proceso:
    1. Identificar pares Izq/Der de cada item.
    2. Si Izq tiene valor y Der no → rellenar Der con mediana.
    3. Si Der tiene valor e Izq no → rellenar Izq con mediana.

    Parámetros:
    - Df: DataFrame con datos procesados.
    - Variable_Agrupacion: Columna para agrupar.
    - Crear_Backup: Si crear columnas _Original.

    Retorna:
    - DataFrame con NaN rellenados.

    """

    print("\n" + "="*60)
    print("RELLENO DE MEDIANAS - ITEMS ASOCIADOS")
    print("="*60)

    Df_Resultado = Df.copy()

    # Verificar columna de agrupación.
    if Variable_Agrupacion not in Df_Resultado.columns:
        print(f"✗ Error: Columna '{Variable_Agrupacion}' "
              f"no encontrada.")
        return Df_Resultado

    # Paso 1: Crear backup.
    if Crear_Backup:
        print("Paso 1: Creando backup...")
        Df_Resultado = Crear_Columnas_Originales(
            Df_Resultado,
            'asociadas'
        )
        print("✓ Backup creado")

    # Paso 2: Obtener todas las columnas IP asociadas.
    print("\nPaso 2: Identificando columnas asociadas...")
    Columnas_IP_Asociados = []

    for Columna in Df_Resultado.columns:
        if ('IP_Item_' in Columna and
            ('_Izq_' in Columna or '_Der_' in Columna) and
            ('Respuesta' in Columna or 'Tiempo' in Columna)):
            Columnas_IP_Asociados.append(Columna)

    print(f"✓ {len(Columnas_IP_Asociados)} columnas encontradas")

    # Paso 3: Convertir a numérico.
    print("\nPaso 3: Convirtiendo a numérico...")
    Df_Resultado = Convertir_A_Numerico(
        Df_Resultado,
        Columnas_IP_Asociados
    )
    print("✓ Conversión completada")

    # Paso 4: Identificar pares únicos de items.
    print("\nPaso 4: Identificando pares Izq/Der...")
    Items_Unicos = set()

    for Columna in Columnas_IP_Asociados:
        Partes = Columna.split('_')
        if len(Partes) >= 5:
            Numero_Item = Partes[2]
            Tipo_Variable = Partes[4]  # Respuesta o Tiempo.
            Items_Unicos.add((Numero_Item, Tipo_Variable))

    print(f"✓ {len(Items_Unicos)} pares identificados")

    # Paso 5: Rellenar por pares.
    print("\nPaso 5: Rellenando valores faltantes...")
    Casos_Rellenados = 0

    for Numero_Item, Tipo_Variable in Items_Unicos:
        Col_Izq = f'IP_Item_{Numero_Item}_Izq_{Tipo_Variable}'
        Col_Der = f'IP_Item_{Numero_Item}_Der_{Tipo_Variable}'

        if (Col_Izq in Df_Resultado.columns and
            Col_Der in Df_Resultado.columns):

            # Rellenar Der donde Izq tiene valor y Der no.
            Mask_Rellenar_Der = (
                Df_Resultado[Col_Izq].notna() &
                Df_Resultado[Col_Der].isna()
            )

            if Mask_Rellenar_Der.any():
                Df_Resultado.loc[Mask_Rellenar_Der, Col_Der] = (
                    Df_Resultado
                    .loc[Mask_Rellenar_Der]
                    .groupby(Variable_Agrupacion)[Col_Der]
                    .transform(
                        lambda x: x.fillna(
                            Df_Resultado[Col_Der].median()
                        )
                    )
                )

                # Rellenar con mediana del grupo.
                for Categoria in (
                    Df_Resultado[Variable_Agrupacion]
                    .unique()
                ):
                    Mask_Categoria = (
                        Mask_Rellenar_Der &
                        (Df_Resultado[Variable_Agrupacion] ==
                         Categoria)
                    )

                    if Mask_Categoria.any():
                        Mediana_Grupo = (
                            Df_Resultado
                            .loc[
                                Df_Resultado[Variable_Agrupacion]
                                == Categoria,
                                Col_Der
                            ]
                            .median()
                        )

                        Df_Resultado.loc[
                            Mask_Categoria,
                            Col_Der
                        ] = Mediana_Grupo

                Casos_Rellenados += Mask_Rellenar_Der.sum()

            # Rellenar Izq donde Der tiene valor e Izq no.
            Mask_Rellenar_Izq = (
                Df_Resultado[Col_Der].notna() &
                Df_Resultado[Col_Izq].isna()
            )

            if Mask_Rellenar_Izq.any():
                for Categoria in (
                    Df_Resultado[Variable_Agrupacion]
                    .unique()
                ):
                    Mask_Categoria = (
                        Mask_Rellenar_Izq &
                        (Df_Resultado[Variable_Agrupacion] ==
                         Categoria)
                    )

                    if Mask_Categoria.any():
                        Mediana_Grupo = (
                            Df_Resultado
                            .loc[
                                Df_Resultado[Variable_Agrupacion]
                                == Categoria,
                                Col_Izq
                            ]
                            .median()
                        )

                        Df_Resultado.loc[
                            Mask_Categoria,
                            Col_Izq
                        ] = Mediana_Grupo

                Casos_Rellenados += Mask_Rellenar_Izq.sum()

    print(f"✓ {Casos_Rellenados} valores rellenados")

    print("\n" + "="*60)
    print("✓ RELLENO DE ITEMS ASOCIADOS COMPLETADO")
    print("="*60)

    return Df_Resultado


def Rellenar_Medianas_Completo(
    Df: pd.DataFrame,
    Variable_Agrupacion: str = VARIABLE_AGRUPACION,
    Crear_Backup: bool = True
) -> pd.DataFrame:

    """
    Aplica relleno de medianas completo: items no asociados
    y asociados.

    Parámetros:
    - Df: DataFrame con datos procesados.
    - Variable_Agrupacion: Columna para agrupar.
    - Crear_Backup: Si crear columnas _Original.

    Retorna:
    - DataFrame con todos los NaN rellenados.

    """

    print("\n" + "="*70)
    print("RELLENO DE MEDIANAS COMPLETO")
    print("="*70)

    # Paso 1: Items no asociados.
    Df_Resultado = Rellenar_Medianas_IP_No_Asociados(
        Df,
        Variable_Agrupacion,
        Crear_Backup
    )

    # Paso 2: Items asociados.
    Df_Resultado = Rellenar_Medianas_IP_Asociados(
        Df_Resultado,
        Variable_Agrupacion,
        False  # Ya se creó backup en paso anterior.
    )

    print("\n" + "="*70)
    print("✓ RELLENO DE MEDIANAS COMPLETO FINALIZADO")
    print("="*70)

    return Df_Resultado


def Rellenar_Medianas_Diccionario(
    Diccionario_Dfs: Dict[str, pd.DataFrame],
    Variable_Agrupacion: str = VARIABLE_AGRUPACION
) -> Dict[str, pd.DataFrame]:

    """
    Aplica relleno de medianas a un diccionario de DataFrames.

    Parámetros:
    - Diccionario_Dfs: Dict con DataFrames
      (ej: {'Generales': df1, 'Ballotage': df2}).
    - Variable_Agrupacion: Columna para agrupar.

    Retorna:
    - Diccionario con DataFrames procesados.

    """

    Diccionario_Resultado = {}

    for Nombre, Df in Diccionario_Dfs.items():
        print(f"\n{'='*70}")
        print(f"PROCESANDO: {Nombre}")
        print(f"{'='*70}")

        Diccionario_Resultado[Nombre] = (
            Rellenar_Medianas_Completo(
                Df,
                Variable_Agrupacion
            )
        )

    return Diccionario_Resultado


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Este módulo debe ser importado, no ejecutado "
          "directamente.")
    print("Uso:")
    print("  from Relleno_Medianas import "
          "Rellenar_Medianas_Completo")
    print("  Df = Rellenar_Medianas_Completo(Df)")
