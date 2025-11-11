# ============================================================
# PROCESAR_REDES_Y_MEDIOS.PY
# ============================================================
# Procesamiento de columnas de redes sociales y medios
# de prensa. Crea variables binarias indicadoras por cada
# red social y medio de comunicación mencionado.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import unidecode
from typing import Dict


# ============================================================
# CONSTANTES
# ============================================================

# Lista de redes sociales a detectar.
REDES_SOCIALES = [
    'twitter',
    'facebook',
    'instagram',
    'threads',
    'tiktok',
    'youtube',
    'whatsapp',
    'telegram'
]

# Lista de medios de prensa a detectar.
MEDIOS_PRENSA = [
    'ambito financiero',
    'prensa obrera',
    'diario universal',
    'popular',
    'izquierda diario',
    'clarin',
    'perfil',
    'pagina 12',
    'infobae',
    'el cronista',
    'la nacion',
    'tiempo argentino',
    'ninguno'
]


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def Procesar_Redes_Sociales(
    Df: pd.DataFrame,
    Columna_Origen: str = 'Red_Social'
) -> pd.DataFrame:

    """
    Procesa columna de redes sociales y crea columnas
    binarias.

    Proceso:
    1. Normalizar columna Red_Social (minúsculas, sin acentos).
    2. Crear columna binaria para cada red social.
    3. Capitalizar nombres de columnas.

    Parámetros:
    - Df: DataFrame con columna de redes sociales.
    - Columna_Origen: Nombre de la columna origen
      (default: 'Red_Social').

    Retorna:
    - DataFrame con columnas binarias por red social.

    """

    print("\n" + "="*60)
    print("PROCESAMIENTO DE REDES SOCIALES")
    print("="*60)

    Df_Resultado = Df.copy()

    # Verificar que existe la columna.
    if Columna_Origen not in Df_Resultado.columns:
        print(f"✗ Error: Columna '{Columna_Origen}' "
              f"no encontrada.")
        return Df_Resultado

    # Paso 1: Normalizar columna.
    print("Paso 1: Normalizando columna...")
    Df_Resultado[Columna_Origen] = (
        Df_Resultado[Columna_Origen]
        .apply(
            lambda x: unidecode.unidecode(str(x)).lower()
            if pd.notna(x) else x
        )
    )
    print("✓ Columna normalizada")

    # Paso 2: Crear columnas binarias.
    print("\nPaso 2: Creando columnas binarias...")
    Columnas_Creadas = 0

    for Red in REDES_SOCIALES:
        Nombre_Columna = Red
        Df_Resultado[Nombre_Columna] = (
            Df_Resultado[Columna_Origen]
            .str.contains(Red, case=False, na=False)
            .astype(int)
        )
        Columnas_Creadas += 1

    print(f"✓ {Columnas_Creadas} columnas creadas")

    # Paso 3: Capitalizar nombres.
    print("\nPaso 3: Capitalizando nombres de columnas...")
    Mapeo_Redes = {
        Red: Red.capitalize()
        for Red in REDES_SOCIALES
    }

    Columnas_Existentes = [
        Col for Col in REDES_SOCIALES
        if Col in Df_Resultado.columns
    ]

    if Columnas_Existentes:
        Mapeo_Actual = {
            Col: Col.capitalize()
            for Col in Columnas_Existentes
        }
        Df_Resultado.rename(
            columns=Mapeo_Actual,
            inplace=True
        )

    print("✓ Columnas renombradas")

    # Paso 4: Reporte.
    print("\nPaso 4: Reporte de uso:")
    Columnas_Capitalizadas = [
        Red.capitalize()
        for Red in REDES_SOCIALES
    ]

    for Red_Cap in Columnas_Capitalizadas:
        if Red_Cap in Df_Resultado.columns:
            Usuarios = Df_Resultado[Red_Cap].sum()
            Porcentaje = (Usuarios / len(Df_Resultado)) * 100
            print(f"  {Red_Cap:<12}: {Usuarios:5} usuarios "
                  f"({Porcentaje:5.1f}%)")

    print("\n" + "="*60)
    print("✓ PROCESAMIENTO DE REDES SOCIALES COMPLETADO")
    print("="*60)

    return Df_Resultado


def Procesar_Medios_Prensa(
    Df: pd.DataFrame,
    Columna_Origen: str = 'Medios_Prensa'
) -> pd.DataFrame:

    """
    Procesa columna de medios de prensa y crea columnas
    binarias.

    Proceso:
    1. Normalizar columna Medios_Prensa.
    2. Crear columna binaria para cada medio.
    3. Convertir nombres a Pascal_Snake_Case.
    4. Renombrar "Ninguno" a "Medios_Prensa_Ninguno".

    Parámetros:
    - Df: DataFrame con columna de medios.
    - Columna_Origen: Nombre de la columna origen.

    Retorna:
    - DataFrame con columnas binarias por medio.

    """

    print("\n" + "="*60)
    print("PROCESAMIENTO DE MEDIOS DE PRENSA")
    print("="*60)

    Df_Resultado = Df.copy()

    # Verificar que existe la columna.
    if Columna_Origen not in Df_Resultado.columns:
        print(f"✗ Error: Columna '{Columna_Origen}' "
              f"no encontrada.")
        return Df_Resultado

    # Paso 1: Normalizar columna.
    print("Paso 1: Normalizando columna...")
    Df_Resultado[Columna_Origen] = (
        Df_Resultado[Columna_Origen]
        .apply(
            lambda x: unidecode.unidecode(str(x)).lower()
            if pd.notna(x) else x
        )
    )
    print("✓ Columna normalizada")

    # Paso 2: Crear columnas binarias.
    print("\nPaso 2: Creando columnas binarias...")
    Columnas_Creadas = 0

    for Medio in MEDIOS_PRENSA:
        Nombre_Columna = Medio
        Df_Resultado[Nombre_Columna] = (
            Df_Resultado[Columna_Origen]
            .str.contains(Medio, case=False, na=False)
            .astype(int)
        )
        Columnas_Creadas += 1

    print(f"✓ {Columnas_Creadas} columnas creadas")

    # Paso 3: Convertir a Pascal_Snake_Case.
    print("\nPaso 3: Convirtiendo a Pascal_Snake_Case...")
    Mapeo_Medios = {
        Medio: Medio.title().replace(' ', '_')
        for Medio in MEDIOS_PRENSA
    }

    Columnas_Existentes = [
        Col for Col in MEDIOS_PRENSA
        if Col in Df_Resultado.columns
    ]

    if Columnas_Existentes:
        Mapeo_Actual = {
            Col: Col.title().replace(' ', '_')
            for Col in Columnas_Existentes
        }
        Df_Resultado.rename(
            columns=Mapeo_Actual,
            inplace=True
        )

    print("✓ Columnas renombradas")

    # Paso 4: Renombrar "Ninguno".
    print("\nPaso 4: Renombrando 'Ninguno'...")
    if 'Ninguno' in Df_Resultado.columns:
        Df_Resultado.rename(
            columns={'Ninguno': 'Medios_Prensa_Ninguno'},
            inplace=True
        )
        print("✓ 'Ninguno' → 'Medios_Prensa_Ninguno'")

    # Paso 5: Reporte.
    print("\nPaso 5: Reporte de uso:")
    Columnas_Pascal_Snake = [
        Medio.title().replace(' ', '_')
        for Medio in MEDIOS_PRENSA
        if Medio != 'ninguno'
    ]

    # Agregar Medios_Prensa_Ninguno si existe.
    if 'Medios_Prensa_Ninguno' in Df_Resultado.columns:
        Columnas_Pascal_Snake.append('Medios_Prensa_Ninguno')

    for Medio_Pascal in Columnas_Pascal_Snake:
        if Medio_Pascal in Df_Resultado.columns:
            Usuarios = Df_Resultado[Medio_Pascal].sum()
            Porcentaje = (
                (Usuarios / len(Df_Resultado)) * 100
            )
            print(f"  {Medio_Pascal:<25}: {Usuarios:5} "
                  f"usuarios ({Porcentaje:5.1f}%)")

    print("\n" + "="*60)
    print("✓ PROCESAMIENTO DE MEDIOS DE PRENSA COMPLETADO")
    print("="*60)

    return Df_Resultado


def Procesar_Redes_Y_Medios_Completo(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Aplica procesamiento completo de redes sociales y medios.

    Parámetros:
    - Df: DataFrame con columnas Red_Social y Medios_Prensa.

    Retorna:
    - DataFrame con columnas binarias de redes y medios.

    """

    print("\n" + "="*70)
    print("PROCESAMIENTO COMPLETO DE REDES Y MEDIOS")
    print("="*70)

    # Paso 1: Redes sociales.
    Df_Resultado = Procesar_Redes_Sociales(Df)

    # Paso 2: Medios de prensa.
    Df_Resultado = Procesar_Medios_Prensa(Df_Resultado)

    print("\n" + "="*70)
    print("✓ PROCESAMIENTO COMPLETO FINALIZADO")
    print("="*70)

    return Df_Resultado


def Procesar_Redes_Y_Medios_Diccionario(
    Diccionario_Dfs: Dict[str, pd.DataFrame]
) -> Dict[str, pd.DataFrame]:

    """
    Aplica procesamiento a un diccionario de DataFrames.

    Parámetros:
    - Diccionario_Dfs: Dict con DataFrames.

    Retorna:
    - Diccionario con DataFrames procesados.

    """

    Diccionario_Resultado = {}

    for Nombre, Df in Diccionario_Dfs.items():
        print(f"\n{'='*70}")
        print(f"PROCESANDO: {Nombre}")
        print(f"{'='*70}")

        Diccionario_Resultado[Nombre] = (
            Procesar_Redes_Y_Medios_Completo(Df)
        )

    return Diccionario_Resultado


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Este módulo debe ser importado, no ejecutado "
          "directamente.")
    print("Uso:")
    print("  from Procesar_Redes_Y_Medios import "
          "Procesar_Redes_Y_Medios_Completo")
    print("  Df = Procesar_Redes_Y_Medios_Completo(Df)")
