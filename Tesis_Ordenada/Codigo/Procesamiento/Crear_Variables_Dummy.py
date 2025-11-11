# ============================================================
# CREAR_VARIABLES_DUMMY.PY
# ============================================================
# Creación de variables dummy (one-hot encoding) para
# variables categóricas. Convierte cada categoría en una
# columna binaria indicadora para uso en modelos estadísticos.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from typing import Dict, List


# ============================================================
# CONSTANTES
# ============================================================

# Lista de variables categóricas a convertir en dummies.
VARIABLES_A_DUMMEAR = [
    'Genero',
    'Estrato_Social',
    'Nivel_Educativo',
    'Fuente_Ingreso',
    'Inmueble_Residencia',
    'Voto_2019',
    'Voto_PASO_2023',
    'Candidato_PASO_2023',
    'Afiliacion_Politica',
    'Edad_Agrupada',
    'Votara_2023',
    'Autopercepcion_Izq_Der_Agrupada',
    'Autopercepcion_Con_Pro_Agrupada',
    'Autopercepcion_Per_Antiper_Agrupada',
    'Region',
    'Categoria_PASO_2023'
]


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def Crear_Variables_Dummy(
    Df: pd.DataFrame,
    Variables: List[str] = None,
    Prefijo_Separador: str = '_',
    Incluir_NaN: bool = False
) -> pd.DataFrame:

    """
    Crea variables dummy para variables categóricas
    especificadas.

    Proceso:
    1. Verificar existencia de variables en DataFrame.
    2. Aplicar pd.get_dummies a cada variable.
    3. Concatenar columnas dummy al DataFrame original.
    4. Reportar columnas creadas.

    Parámetros:
    - Df: DataFrame con variables categóricas.
    - Variables: Lista de nombres de columnas a dummear.
      Si es None, usa VARIABLES_A_DUMMEAR.
    - Prefijo_Separador: Separador entre nombre de variable
      y categoría (default: '_').
    - Incluir_NaN: Si crear columna para valores NaN.

    Retorna:
    - DataFrame con columnas dummy agregadas.

    """

    print("\n" + "="*60)
    print("CREACIÓN DE VARIABLES DUMMY")
    print("="*60)

    Df_Resultado = Df.copy()

    # Usar lista por defecto si no se proporciona.
    if Variables is None:
        Variables = VARIABLES_A_DUMMEAR

    # Paso 1: Identificar variables existentes.
    print("\nPaso 1: Identificando variables disponibles...")
    Variables_Existentes = [
        Var for Var in Variables
        if Var in Df_Resultado.columns
    ]
    Variables_Faltantes = [
        Var for Var in Variables
        if Var not in Df_Resultado.columns
    ]

    print(f"  Variables encontradas: {len(Variables_Existentes)}")
    print(f"  Variables faltantes: {len(Variables_Faltantes)}")

    if Variables_Faltantes:
        print(f"\n  Variables no encontradas en DataFrame:")
        for Var in Variables_Faltantes:
            print(f"    - {Var}")

    # Paso 2: Crear dummies para cada variable.
    print("\nPaso 2: Creando variables dummy...")
    Total_Columnas_Creadas = 0

    for Variable in Variables_Existentes:
        print(f"\n  Procesando: {Variable}")

        # Contar valores únicos.
        Valores_Unicos = Df_Resultado[Variable].nunique(dropna=True)
        print(f"    Valores únicos: {Valores_Unicos}")

        # Crear dummies.
        Dummies = pd.get_dummies(
            Df_Resultado[Variable],
            prefix=Variable,
            prefix_sep=Prefijo_Separador,
            dummy_na=Incluir_NaN
        )

        # Concatenar al DataFrame.
        Df_Resultado = pd.concat(
            [Df_Resultado, Dummies],
            axis=1
        )

        Num_Columnas_Creadas = len(Dummies.columns)
        Total_Columnas_Creadas += Num_Columnas_Creadas

        print(f"    Columnas dummy creadas: {Num_Columnas_Creadas}")

        # Mostrar nombres de columnas si son pocas.
        if Num_Columnas_Creadas <= 5:
            for Col in Dummies.columns:
                print(f"      - {Col}")

    # Paso 3: Reporte final.
    print("\nPaso 3: Reporte final:")
    print(f"  Variables procesadas: {len(Variables_Existentes)}")
    print(f"  Total columnas dummy creadas: "
          f"{Total_Columnas_Creadas}")
    print(f"  Total columnas finales: {len(Df_Resultado.columns)}")

    print("\n" + "="*60)
    print("✓ CREACIÓN DE VARIABLES DUMMY COMPLETADA")
    print("="*60)

    return Df_Resultado


def Crear_Variables_Dummy_Completo(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Crea variables dummy para todas las variables categóricas
    estándar del estudio.

    Utiliza la lista predefinida VARIABLES_A_DUMMEAR que
    incluye 16 variables categóricas: demográficas, políticas
    y de autopercepción.

    Parámetros:
    - Df: DataFrame con variables categóricas procesadas.

    Retorna:
    - DataFrame con todas las variables dummy agregadas.

    """

    print("\n" + "="*60)
    print("CREACIÓN COMPLETA DE VARIABLES DUMMY")
    print("="*60)

    Df_Resultado = Crear_Variables_Dummy(
        Df,
        Variables=VARIABLES_A_DUMMEAR,
        Incluir_NaN=False
    )

    print("\n" + "="*60)
    print("✓ CREACIÓN COMPLETA FINALIZADA")
    print("="*60)

    return Df_Resultado


def Crear_Variables_Dummy_Diccionario(
    Diccionario_Dfs: Dict[str, pd.DataFrame],
    Variables: List[str] = None
) -> Dict[str, pd.DataFrame]:

    """
    Aplica creación de variables dummy a un diccionario de
    DataFrames.

    Parámetros:
    - Diccionario_Dfs: Dict con DataFrames.
    - Variables: Lista de variables a dummear. Si es None,
      usa VARIABLES_A_DUMMEAR.

    Retorna:
    - Diccionario con DataFrames procesados.

    """

    Diccionario_Resultado = {}

    for Nombre, Df in Diccionario_Dfs.items():
        print(f"\n{'='*70}")
        print(f"PROCESANDO: {Nombre}")
        print(f"{'='*70}")

        Diccionario_Resultado[Nombre] = Crear_Variables_Dummy(
            Df,
            Variables=Variables,
            Incluir_NaN=False
        )

    return Diccionario_Resultado


def Verificar_Variables_Dummy(
    Df: pd.DataFrame,
    Variables: List[str] = None
) -> Dict[str, Dict]:

    """
    Verifica integridad de variables dummy creadas.

    Comprueba:
    - Columnas son binarias (0/1)
    - Suma por fila es consistente
    - Correspondencia con variable original
    - Distribución de categorías

    Parámetros:
    - Df: DataFrame con variables dummy.
    - Variables: Lista de variables a verificar. Si es None,
      usa VARIABLES_A_DUMMEAR.

    Retorna:
    - Diccionario con resultados de verificación por variable.

    """

    print("\n" + "="*60)
    print("VERIFICACIÓN DE VARIABLES DUMMY")
    print("="*60)

    if Variables is None:
        Variables = VARIABLES_A_DUMMEAR

    Reporte = {}

    for Variable in Variables:
        # Buscar columnas dummy de esta variable.
        Prefijo = f'{Variable}_'
        Columnas_Dummy = [
            Col for Col in Df.columns
            if Col.startswith(Prefijo)
        ]

        if not Columnas_Dummy:
            print(f"\n  {Variable}: No se encontraron columnas dummy")
            continue

        print(f"\n  {Variable}:")
        print(f"    Columnas dummy: {len(Columnas_Dummy)}")

        Verificacion = {
            'num_columnas': len(Columnas_Dummy),
            'columnas': Columnas_Dummy,
            'es_binario': True,
            'suma_consistente': True,
            'distribucion': {}
        }

        # Verificar que sean binarias.
        for Col in Columnas_Dummy:
            Valores_Unicos = Df[Col].dropna().unique()
            if not set(Valores_Unicos).issubset({0, 1}):
                Verificacion['es_binario'] = False
                print(f"    ✗ {Col} no es binaria")

        if Verificacion['es_binario']:
            print("    ✓ Todas las columnas son binarias")

        # Verificar suma por fila.
        if len(Columnas_Dummy) > 1:
            Suma_Por_Fila = Df[Columnas_Dummy].sum(axis=1)
            Valores_Suma = Suma_Por_Fila.unique()

            if set(Valores_Suma) == {1}:
                print("    ✓ Cada fila suma exactamente 1")
            else:
                Verificacion['suma_consistente'] = False
                Filas_Cero = (Suma_Por_Fila == 0).sum()
                if Filas_Cero > 0:
                    print(f"    ⚠ {Filas_Cero} filas suman 0 "
                          f"(valores NaN)")

        # Calcular distribución.
        for Col in Columnas_Dummy:
            Categoria = Col.replace(Prefijo, '')
            Frecuencia = Df[Col].sum()
            Porcentaje = (Frecuencia / len(Df)) * 100
            Verificacion['distribucion'][Categoria] = {
                'frecuencia': int(Frecuencia),
                'porcentaje': round(Porcentaje, 1)
            }

        # Mostrar distribución.
        print("    Distribución:")
        Distribucion_Ordenada = sorted(
            Verificacion['distribucion'].items(),
            key=lambda x: x[1]['frecuencia'],
            reverse=True
        )

        for Categoria, Stats in Distribucion_Ordenada[:5]:
            Frec = Stats['frecuencia']
            Porc = Stats['porcentaje']
            print(f"      {Categoria}: {Frec} ({Porc}%)")

        if len(Distribucion_Ordenada) > 5:
            print(f"      ... y {len(Distribucion_Ordenada) - 5} "
                  f"más")

        Reporte[Variable] = Verificacion

    print("\n" + "="*60)
    print("✓ VERIFICACIÓN COMPLETADA")
    print("="*60)

    return Reporte


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Este módulo debe ser importado, no ejecutado "
          "directamente.")
    print("Uso:")
    print("  from Crear_Variables_Dummy import "
          "Crear_Variables_Dummy_Completo")
    print("  Df = Crear_Variables_Dummy_Completo(Df)")
