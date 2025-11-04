# ============================================================
# EJECUTAR_PIPELINE_COMPLETO.PY
# ============================================================
# Script principal que ejecuta todo el pipeline de
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

from Configuracion import Crear_Carpetas_Salida
from Construccion_Bases import Ejecutar_Construccion_Bases


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def Ejecutar_Pipeline():

    """
    Ejecuta el pipeline completo de procesamiento y análisis.

    """

    print("\n" + "="*70)
    print(" " * 15 + "PIPELINE COMPLETO DE ANÁLISIS")
    print(" " * 10 + "Tesis: Ideología y Cambio de Opinión")
    print("="*70 + "\n")

    # Paso 1: Crear carpetas de salida.
    print("Paso 1: Creando estructura de carpetas...")
    Crear_Carpetas_Salida()
    print("✓ Carpetas creadas.\n")

    # Paso 2: Construcción de bases de datos.
    print("Paso 2: Construcción de bases de datos...")
    Ejecutar_Construccion_Bases()

    # Paso 3: Cálculo de índices.
    print("\nPaso 3: Cálculo de índices ideológicos...")
    # TODO: Implementar cuando se ejecute por primera vez.
    print("⚠ Pendiente de implementación.\n")

    # Paso 4: Variables de cambio.
    print("Paso 4: Cálculo de variables de cambio...")
    # TODO: Implementar.
    print("⚠ Pendiente de implementación.\n")

    # Paso 5: Tests estadísticos.
    print("Paso 5: Ejecución de tests estadísticos...")
    # TODO: Implementar.
    print("⚠ Pendiente de implementación.\n")

    # Paso 6: Modelos SEM.
    print("Paso 6: Modelado con ecuaciones estructurales...")
    # TODO: Implementar.
    print("⚠ Pendiente de implementación.\n")

    # Paso 7: Visualizaciones.
    print("Paso 7: Generación de visualizaciones...")
    # TODO: Implementar.
    print("⚠ Pendiente de implementación.\n")

    print("="*70)
    print(" " * 20 + "PIPELINE COMPLETADO")
    print("="*70 + "\n")


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    Ejecutar_Pipeline()
