# ============================================================
# EJECUTAR_PIPELINE_COMPLETO.PY
# ============================================================
# Script principal para ejecutar el pipeline completo de
# procesamiento y análisis de datos.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import sys
from pathlib import Path

# Agregar rutas de módulos.
Ruta_Base = Path(__file__).parent.parent
sys.path.append(str(Ruta_Base / "Codigo" / "Utilidades"))
sys.path.append(str(Ruta_Base / "Codigo" / "Procesamiento"))
sys.path.append(str(Ruta_Base / "Codigo" / "Test_Estadisticos"))
sys.path.append(str(Ruta_Base / "Codigo" / "Modelado_Estadistico"))

import pandas as pd
from Configuracion import *


# ============================================================
# PIPELINE COMPLETO
# ============================================================

def Ejecutar_Pipeline_Completo():

    """
    Ejecuta el pipeline completo de procesamiento.

    Orden de ejecución:
    1. Construcción de bases de datos.
    2. Eliminación de warm-up.
    3. Cálculo de índices ideológicos.
    4. Creación de variables de cambio (CO y CT).
    5. Limpieza final (categorías y outliers).

    """

    print("\n" + "="*70)
    print("PIPELINE COMPLETO DE PROCESAMIENTO")
    print("="*70)

    # ========================================================
    # PASO 1: CONSTRUCCIÓN DE BASES DE DATOS
    # ========================================================

    print("\n" + "#"*70)
    print("PASO 1: CONSTRUCCIÓN DE BASES DE DATOS")
    print("#"*70)

    from Construccion_Bases import (
        Combinar_Archivos_Generales,
        Combinar_Archivos_Ballotage,
        Procesar_Base_Completa
    )

    # Cargar y procesar Generales.
    print("\nProcesando datos de Generales...")
    Df_Generales_Crudo = Combinar_Archivos_Generales()
    Df_Generales = Procesar_Base_Completa(Df_Generales_Crudo)
    print(f"✓ Generales: {len(Df_Generales)} participantes")

    # Cargar y procesar Ballotage.
    print("\nProcesando datos de Ballotage...")
    Df_Ballotage_Crudo = Combinar_Archivos_Ballotage()
    Df_Ballotage = Procesar_Base_Completa(Df_Ballotage_Crudo)
    print(f"✓ Ballotage: {len(Df_Ballotage)} participantes")

    # Crear diccionario.
    Diccionario_Dfs = {
        'Generales': Df_Generales,
        'Ballotage': Df_Ballotage
    }

    # ========================================================
    # PASO 2: ELIMINACIÓN DE WARM-UP
    # ========================================================

    print("\n" + "#"*70)
    print("PASO 2: ELIMINACIÓN DE WARM-UP")
    print("#"*70)
    print(
        "\nEliminando primeros 3 items únicos asociados "
        "de cada participante..."
    )

    from Limpieza_Datos import Eliminar_Primeros_Items_Warm_Up

    for Nombre_Df, Df in Diccionario_Dfs.items():
        print(f"\nProcesando {Nombre_Df}:")
        Diccionario_Dfs[Nombre_Df] = (
            Eliminar_Primeros_Items_Warm_Up(Df)
        )

    # ========================================================
    # PASO 3: CÁLCULO DE ÍNDICES IDEOLÓGICOS
    # ========================================================

    print("\n" + "#"*70)
    print("PASO 3: CÁLCULO DE ÍNDICES IDEOLÓGICOS")
    print("#"*70)

    from Calculo_Indices import Calcular_Todos_Indices

    for Nombre_Df, Df in Diccionario_Dfs.items():
        print(f"\nCalculando índices para {Nombre_Df}...")
        Diccionario_Dfs[Nombre_Df] = Calcular_Todos_Indices(Df)

    print("\n✓ Índices ideológicos calculados.")

    # ========================================================
    # PASO 4: CREACIÓN DE VARIABLES DE CAMBIO
    # ========================================================

    print("\n" + "#"*70)
    print("PASO 4: CREACIÓN DE VARIABLES DE CAMBIO (CO Y CT)")
    print("#"*70)

    from Calculo_Variables_Cambio import (
        Calcular_Variables_Cambio
    )

    Diccionario_Dfs = Calcular_Variables_Cambio(
        Diccionario_Dfs,
        Incluir_Congruencia=True,
        Incluir_Agregadas=True
    )

    # ========================================================
    # PASO 5: LIMPIEZA FINAL
    # ========================================================

    print("\n" + "#"*70)
    print("PASO 5: LIMPIEZA FINAL")
    print("#"*70)

    from Limpieza_Datos import Limpiar_Diccionario_Dataframes

    Diccionario_Dfs = Limpiar_Diccionario_Dataframes(
        Diccionario_Dfs,
        Eliminar_Warm_Up=False,  # Ya se hizo en Paso 2.
        Filtrar_Categorias=True,
        Filtrar_Tiempos=True,
        Numero_Desviaciones=3
    )

    # ========================================================
    # RESUMEN FINAL
    # ========================================================

    print("\n" + "="*70)
    print("RESUMEN FINAL DEL PIPELINE")
    print("="*70)

    for Nombre_Df, Df in Diccionario_Dfs.items():
        print(f"\n{Nombre_Df}:")
        print(f"  Participantes: {len(Df)}")
        print(f"  Columnas: {len(Df.columns)}")
        print(f"  Variables CO: {len([c for c in Df.columns if c.startswith('CO_')])}")
        print(f"  Variables CT: {len([c for c in Df.columns if c.startswith('CT_')])}")

    print("\n" + "="*70)
    print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*70 + "\n")

    return Diccionario_Dfs


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    Diccionario_Dfs = Ejecutar_Pipeline_Completo()
