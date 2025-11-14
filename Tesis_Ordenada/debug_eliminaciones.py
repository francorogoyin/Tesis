import sys
import io

# Configurar UTF-8 para Windows.
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8',
        errors='replace'
    )

sys.path.append('Codigo/Utilidades')
sys.path.append('Codigo/Procesamiento')

from Construccion_Bases import (
    Combinar_Archivos_Generales,
    Procesar_Base_Completa
)
from Limpieza_Datos import Limpiar_Datos_Completo

print("="*70)
print("DEBUG: SEGUIMIENTO DE ELIMINACIONES PASO A PASO")
print("="*70)

# Paso 1: Construcción.
print("\n[PASO 1] Combinando archivos...")
df_crudo = Combinar_Archivos_Generales()
print(f"Despues de combinar CSVs: {len(df_crudo)} filas")

print("\n[PASO 1] Procesando base completa...")
df = Procesar_Base_Completa(df_crudo)
print(f"Despues de Procesar_Base_Completa: {len(df)} filas")

# Paso 4: Limpieza (simulando lo que hace el pipeline).
print("\n[PASO 4] Aplicando limpieza completa...")
print(f"ANTES de limpieza: {len(df)} filas")

df_limpio = Limpiar_Datos_Completo(
    df,
    Eliminar_Warm_Up=True,
    Num_Items_Warm_Up=3,
    Filtrar_Categorias=True,
    Filtrar_Tiempos=True,
    Numero_Desviaciones=3
)

print(f"\nDESPUES de limpieza: {len(df_limpio)} filas")
print(f"Total eliminadas: {len(df) - len(df_limpio)}")
print(f"Porcentaje eliminado: "
      f"{((len(df) - len(df_limpio))/len(df)*100):.1f}%")

print("\n" + "="*70)
print("FIN DEL DEBUG")
print("="*70)
