# ============================================================
# EJECUTAR_PIPELINE_COMPLETO.PY
# ============================================================
# Script principal para ejecutar el pipeline completo de
# preprocesamiento y análisis de datos del estudio de
# personalidad implícita y cambio de opinión política.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from pathlib import Path
from typing import Dict
from datetime import datetime
import sys
import os

# Configurar codificación UTF-8 para Windows.
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8',
        errors='replace'
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer,
        encoding='utf-8',
        errors='replace'
    )

# Agregar rutas al path.
Ruta_Actual = Path(__file__).parent
Ruta_Utilidades = Ruta_Actual / "Codigo" / "Utilidades"
Ruta_Procesamiento = Ruta_Actual / "Codigo" / "Procesamiento"

sys.path.append(str(Ruta_Utilidades))
sys.path.append(str(Ruta_Procesamiento))

# Importar módulos de procesamiento.
from Construccion_Bases import (
    Combinar_Archivos_Generales,
    Combinar_Archivos_Ballotage,
    Procesar_Base_Completa
)
from Calculo_Indices import Calcular_Todos_Indices
from Calculo_Variables_Cambio import Calcular_Variables_Cambio
from Limpieza_Datos import Limpiar_Diccionario_Dataframes
from Relleno_Medianas import Rellenar_Medianas_Completo
from Procesar_Redes_Y_Medios import (
    Procesar_Redes_Sociales,
    Procesar_Medios_Prensa
)
from Agrupamiento_Variables import (
    Aplicar_Agrupamientos_Completos
)
from Crear_Variables_Dummy import Crear_Variables_Dummy_Completo
from Ordenamiento_Columnas import Aplicar_Ordenamiento_Completo
from Agregar_Clusters import Agregar_Clusters_A_DataFrame

# Importar configuración.
from Configuracion import (
    RUTA_TABLAS_BASES,
    RUTA_DATA_CRUDOS
)


# ============================================================
# FUNCIÓN PRINCIPAL DEL PIPELINE
# ============================================================

def Ejecutar_Pipeline_Completo(
    Guardar_Intermedios: bool = False,
    Verbose: bool = True
) -> Dict[str, pd.DataFrame]:

    """
    Ejecuta pipeline completo de preprocesamiento de datos.

    Pipeline de 11 pasos:
    1. Construcción de bases desde CSVs crudos.
    2. Limpieza de datos y eliminación de outliers.
    3. Relleno de medianas por categoría ideológica.
    4. Cálculo de índices (Positividad, Progresismo,
       Conservadurismo).
    5. Cálculo de variables CO y CT.
    6. Procesamiento de redes sociales y medios.
    7. Agrupamiento de variables sociodemográficas.
    8. Creación de variables dummy.
    9. Ordenamiento de columnas.
    10. Agregado de variables de clustering.
    11. Exportación de bases finales.

    Parámetros:
    - Guardar_Intermedios: Si guardar DataFrames intermedios
      después de cada paso.
    - Verbose: Si mostrar mensajes detallados de progreso.

    Retorna:
    - Diccionario con claves 'Generales' y 'Ballotage', valores
      DataFrames procesados.

    """

    Inicio = datetime.now()

    print("\n" + "="*70)
    print("PIPELINE COMPLETO DE PREPROCESAMIENTO")
    print("="*70)
    print("\nEstudio: Personalidad Implícita y Cambio de Opinión")
    print("Elecciones: Generales 2023 y Ballotage 2023")
    print("="*70)

    # ========================================================
    # PASO 1: CONSTRUCCIÓN DE BASES
    # ========================================================

    print("\n" + "="*70)
    print("PASO 1/11: CONSTRUCCIÓN DE BASES DESDE CSVs")
    print("="*70)

    if Verbose:
        print("\nCombinando archivos CSV crudos...")

    # Generales.
    Df_Generales_Crudo = Combinar_Archivos_Generales()
    Df_Generales = Procesar_Base_Completa(Df_Generales_Crudo)

    # Ballotage.
    Df_Ballotage_Crudo = Combinar_Archivos_Ballotage()
    Df_Ballotage = Procesar_Base_Completa(Df_Ballotage_Crudo)

    Diccionario_Dfs = {
        'Generales': Df_Generales,
        'Ballotage': Df_Ballotage
    }

    print(f"\n✓ Bases construidas:")
    for Nombre, Df in Diccionario_Dfs.items():
        print(
            f"  {Nombre}: {len(Df)} participantes, "
            f"{len(Df.columns)} columnas"
        )

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "01_Construccion")

    # ========================================================
    # PASO 2: LIMPIEZA DE DATOS
    # ========================================================

    print("\n" + "="*70)
    print("PASO 2/11: LIMPIEZA DE DATOS Y OUTLIERS")
    print("="*70)

    if Verbose:
        print("\nFiltrando categorías inválidas y outliers "
              "de tiempo...")

    # Guardar tamaños pre-limpieza.
    Tamaños_Pre = {
        Nombre: len(Df) for Nombre, Df in Diccionario_Dfs.items()
    }

    Diccionario_Dfs = Limpiar_Diccionario_Dataframes(
        Diccionario_Dfs,
        Filtrar_Categorias=True,
        Filtrar_Tiempos=True,
        Numero_Desviaciones=3
    )

    print("\n✓ Datos limpios:")
    for Nombre, Df in Diccionario_Dfs.items():
        Eliminados = Tamaños_Pre[Nombre] - len(Df)
        Porcentaje = (Eliminados / Tamaños_Pre[Nombre]) * 100
        print(
            f"  {Nombre}: {len(Df)} casos "
            f"({Eliminados} eliminados, {Porcentaje:.1f}%)"
        )

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "02_Limpieza")

    # ========================================================
    # PASO 3: CÁLCULO DE VARIABLES CO Y CT
    # ========================================================

    print("\n" + "="*70)
    print("PASO 3/11: CÁLCULO DE VARIABLES DE CAMBIO (CO/CT)")
    print("="*70)

    if Verbose:
        print("\nCreando variables CO (Cambio de Opinión) y "
              "CT (Cambio de Tiempo)...")

    Diccionario_Dfs = Calcular_Variables_Cambio(
        Diccionario_Dfs,
        Incluir_Congruencia=True
    )

    print("\n✓ Variables de cambio creadas (80 columnas por base)")

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "03_Variables_Cambio")

    # ========================================================
    # PASO 4: LIMPIEZA DE DATOS
    # ========================================================

    print("\n" + "="*70)
    print("PASO 4/11: LIMPIEZA DE DATOS Y OUTLIERS")
    print("="*70)

    if Verbose:
        print("\nFiltrando categorías inválidas y outliers "
              "de tiempo...")

    # Guardar tamaños pre-limpieza.
    Tamaños_Pre = {
        Nombre: len(Df) for Nombre, Df in Diccionario_Dfs.items()
    }

    Diccionario_Dfs = Limpiar_Diccionario_Dataframes(
        Diccionario_Dfs,
        Filtrar_Categorias=True,
        Filtrar_Tiempos=True,
        Numero_Desviaciones=3
    )

    print("\n✓ Datos limpios:")
    for Nombre, Df in Diccionario_Dfs.items():
        Eliminados = Tamaños_Pre[Nombre] - len(Df)
        Porcentaje = (Eliminados / Tamaños_Pre[Nombre]) * 100
        print(
            f"  {Nombre}: {len(Df)} casos "
            f"({Eliminados} eliminados, {Porcentaje:.1f}%)"
        )

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "04_Limpieza")

    # ========================================================
    # PASO 5: RELLENO DE MEDIANAS
    # ========================================================

    print("\n" + "="*70)
    print("PASO 5/11: RELLENO DE NaN CON MEDIANAS")
    print("="*70)

    if Verbose:
        print("\nRellenando valores faltantes con medianas por "
              "categoría ideológica...")

    for Nombre, Df in Diccionario_Dfs.items():
        Diccionario_Dfs[Nombre] = (
            Rellenar_Medianas_Completo(
                Df,
                Variable_Agrupacion='Categoria_PASO_2023'
            )
        )

    print("\n✓ Medianas aplicadas")

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "05_Medianas")

    # ========================================================
    # PASO 6: PROCESAMIENTO DE REDES Y MEDIOS
    # ========================================================

    print("\n" + "="*70)
    print("PASO 6/11: PROCESAMIENTO REDES SOCIALES Y MEDIOS")
    print("="*70)

    if Verbose:
        print("\nConvirtiendo columnas de texto en variables "
              "binarias...")

    for Nombre, Df in Diccionario_Dfs.items():
        Df = Procesar_Redes_Sociales(Df)
        Df = Procesar_Medios_Prensa(Df)
        Diccionario_Dfs[Nombre] = Df

    print("\n✓ Redes y medios procesados (~20 columnas agregadas)")

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "06_Redes_Medios")

    # ========================================================
    # PASO 7: AGRUPAMIENTO DE VARIABLES
    # ========================================================

    print("\n" + "="*70)
    print("PASO 7/11: AGRUPAMIENTO VARIABLES SOCIODEMOGRÁFICAS")
    print("="*70)

    if Verbose:
        print("\nCreando versiones agrupadas de variables "
              "categóricas...")

    for Nombre, Df in Diccionario_Dfs.items():
        Diccionario_Dfs[Nombre] = (
            Aplicar_Agrupamientos_Completos(Df)
        )

    print("\n✓ Agrupamientos aplicados (~5 columnas agregadas)")

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "07_Agrupamientos")

    # ========================================================
    # PASO 8: CREACIÓN DE VARIABLES DUMMY
    # ========================================================

    print("\n" + "="*70)
    print("PASO 8/11: CREACIÓN DE VARIABLES DUMMY")
    print("="*70)

    if Verbose:
        print("\nCreando variables dummy para modelado "
              "estadístico...")

    for Nombre, Df in Diccionario_Dfs.items():
        Diccionario_Dfs[Nombre] = Crear_Variables_Dummy_Completo(Df)

    print("\n✓ Variables dummy creadas (~30 columnas agregadas)")

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "08_Dummies")

    # ========================================================
    # PASO 9: ORDENAMIENTO DE COLUMNAS
    # ========================================================

    print("\n" + "="*70)
    print("PASO 9/11: ORDENAMIENTO Y RENOMBRAMIENTO")
    print("="*70)

    if Verbose:
        print("\nOrdenando columnas por grupos temáticos...")

    for Nombre, Df in Diccionario_Dfs.items():
        Diccionario_Dfs[Nombre] = (
            Aplicar_Ordenamiento_Completo(Df)
        )

    print("\n✓ Columnas ordenadas")

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "09_Ordenamiento")

    # ========================================================
    # PASO 10: AGREGADO DE CLUSTERS
    # ========================================================

    print("\n" + "="*70)
    print("PASO 10/11: AGREGADO DE VARIABLES DE CLUSTERING")
    print("="*70)

    if Verbose:
        print("\nIncorporando resultados de clustering "
              "(Kmeans, Jerárquico, DBSCAN)...")

    Ruta_Clusters = RUTA_DATA_CRUDOS / "Resultados_Clustering"

    if Ruta_Clusters.exists():
        for Nombre, Df in Diccionario_Dfs.items():
            try:
                Diccionario_Dfs[Nombre] = (
                    Agregar_Clusters_A_DataFrame(Df, str(Ruta_Clusters))
                )
            except FileNotFoundError:
                print(
                    f"⚠️ {Nombre}: Archivos de clustering no "
                    f"encontrados"
                )

        print("\n✓ Clusters agregados (3 columnas)")
    else:
        print(
            "\n⚠️ Carpeta de clustering no encontrada. "
            "Saltando paso."
        )

    if Guardar_Intermedios:
        Guardar_Intermedios_Paso(Diccionario_Dfs, "10_Clusters")

    # ========================================================
    # PASO 11: EXPORTACIÓN DE BASES FINALES
    # ========================================================

    print("\n" + "="*70)
    print("PASO 11/11: EXPORTACIÓN DE BASES FINALES")
    print("="*70)

    if Verbose:
        print("\nGuardando bases procesadas en "
              "'Data/Bases definitivas/'...")

    Ruta_Export = Path(RUTA_TABLAS_BASES)
    Ruta_Export.mkdir(parents=True, exist_ok=True)

    for Nombre, Df in Diccionario_Dfs.items():
        Archivo_Salida = (
            Ruta_Export / f"Base_Final_{Nombre}.xlsx"
        )

        Df.to_excel(Archivo_Salida, index=False)
        print(f"  ✓ {Nombre}: {Archivo_Salida.name}")

    # Generar metadatos.
    Archivo_Metadatos = Ruta_Export / "Metadatos_Pipeline.txt"

    with open(Archivo_Metadatos, 'w', encoding='utf-8') as F:
        F.write("="*60 + "\n")
        F.write("METADATOS DEL PIPELINE DE PREPROCESAMIENTO\n")
        F.write("="*60 + "\n")
        F.write(f"\nFecha de ejecución: {datetime.now()}\n")
        F.write("\n")

        for Nombre, Df in Diccionario_Dfs.items():
            F.write(f"\n{Nombre}:\n")
            F.write(f"  Casos: {len(Df)}\n")
            F.write(f"  Columnas: {len(Df.columns)}\n")
            F.write(
                f"  Memoria: "
                f"{Df.memory_usage(deep=True).sum() / 1024**2:.1f} MB\n"
            )
            F.write("\n  Columnas incluidas:\n")

            for i, Col in enumerate(Df.columns, 1):
                F.write(f"    {i}. {Col}\n")

            F.write("\n")

    print(f"  ✓ Metadatos: {Archivo_Metadatos.name}")

    # ========================================================
    # FINALIZACIÓN
    # ========================================================

    Fin = datetime.now()
    Duracion = Fin - Inicio

    print("\n" + "="*70)
    print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*70)
    print(f"\nDuración total: {Duracion}")
    print(f"\nBases finales guardadas en:")
    print(f"  {Ruta_Export}")
    print(f"\nResumen de bases procesadas:")

    for Nombre, Df in Diccionario_Dfs.items():
        print(f"\n  {Nombre}:")
        print(f"    Casos: {len(Df)}")
        print(f"    Columnas: {len(Df.columns)}")
        print(
            f"    Memoria: "
            f"{Df.memory_usage(deep=True).sum() / 1024**2:.1f} MB"
        )

    print("\n" + "="*70)

    return Diccionario_Dfs


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def Guardar_Intermedios_Paso(
    Diccionario_Dfs: Dict[str, pd.DataFrame],
    Nombre_Paso: str
) -> None:

    """
    Guarda DataFrames intermedios de un paso del pipeline.

    Parámetros:
    - Diccionario_Dfs: Diccionario con DataFrames.
    - Nombre_Paso: Nombre del paso (ej: '01_Construccion').

    """

    Ruta_Intermedios = (
        Path(RUTA_DATA_CRUDOS).parent / "Intermedios" / Nombre_Paso
    )
    Ruta_Intermedios.mkdir(parents=True, exist_ok=True)

    for Nombre, Df in Diccionario_Dfs.items():
        Archivo = (
            Ruta_Intermedios / f"{Nombre}_{Nombre_Paso}.xlsx"
        )
        Df.to_excel(Archivo, index=False)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("EJECUCIÓN DIRECTA DEL PIPELINE")
    print("="*70)

    # Ejecutar pipeline completo.
    Dfs_Finales = Ejecutar_Pipeline_Completo(
        Guardar_Intermedios=False,
        Verbose=True
    )

    print("\n✅ Ejecución completada")
    print(f"✅ {len(Dfs_Finales)} bases procesadas\n")
