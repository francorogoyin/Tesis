# ============================================================
# CALCULO_VARIABLES_CAMBIO.PY
# ============================================================
# Creación de variables de Cambio de Opinión (CO) y Cambio
# de Tiempo (CT) comparando respuestas base vs asociadas a
# candidatos. Incluye cálculo de cambios congruentes e
# incongruentes según tipo de item e ideología.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Funciones_Comunes import (
    Crear_Columnas_Cambio_Opinion,
    Crear_Columnas_Cambio_Tiempo
)
from Configuracion import (
    NUMEROS_ITEMS_IP,
    ITEMS_PROGRESISTAS,
    ITEMS_CONSERVADORES,
    CATEGORIAS_IZQUIERDA,
    CATEGORIAS_DERECHA,
    PREFIJO_CO,
    SUFIJO_IZQ,
    SUFIJO_DER
)


# ============================================================
# FUNCIONES DE CONGRUENCIA
# ============================================================

def Calcular_CO_Congruentes_E_Incongruentes(
    Df: pd.DataFrame,
    Nombre_Columna_Categoria: str = 'Categoria_PASO_2023'
) -> pd.DataFrame:

    """
    Calcula variables agregadas de CO_Congruentes y
    CO_Incongruentes según la ideología del participante
    y el tipo de item.

    Congruente: Item progresista + Candidato izquierda O
                Item conservador + Candidato derecha.
    Incongruente: Item progresista + Candidato derecha O
                  Item conservador + Candidato izquierda.

    Parámetros:
    - Df: DataFrame con variables CO ya calculadas.
    - Nombre_Columna_Categoria: Nombre de columna con
      categoría ideológica.

    Retorna:
    - DataFrame con nuevas columnas CO_Congruentes_Promedio
      y CO_Incongruentes_Promedio.

    """

    Df_Resultado = Df.copy()

    # Listas para almacenar columnas relevantes.
    Columnas_Congruentes = []
    Columnas_Incongruentes = []

    # Iterar sobre cada fila para clasificar.
    for Index, Fila in Df_Resultado.iterrows():
        Categoria = Fila.get(Nombre_Columna_Categoria, None)

        # Determinar si es izquierda o derecha.
        Es_Izquierda = Categoria in CATEGORIAS_IZQUIERDA
        Es_Derecha = Categoria in CATEGORIAS_DERECHA

        # Buscar columnas CO.
        Columnas_CO = [
            col for col in Df_Resultado.columns
            if col.startswith(PREFIJO_CO)
        ]

        # Clasificar cada variable CO.
        for Col_CO in Columnas_CO:
            # Extraer número de item.
            try:
                Partes = Col_CO.replace(PREFIJO_CO, '').replace(
                    'Item_',
                    ''
                ).split('_')
                Numero_Item = int(Partes[0])
                Sufijo = '_' + '_'.join(Partes[1:])
            except:
                continue

            # Determinar si es progresista o conservador.
            Es_Progresista = Numero_Item in ITEMS_PROGRESISTAS
            Es_Conservador = Numero_Item in ITEMS_CONSERVADORES

            # Determinar si terminó en Izq o Der.
            Es_Item_Izq = SUFIJO_IZQ in Col_CO
            Es_Item_Der = SUFIJO_DER in Col_CO

            # Clasificar según congruencia.
            if Es_Izquierda:
                if Es_Progresista and Es_Item_Izq:
                    Columnas_Congruentes.append(Col_CO)
                elif Es_Conservador and Es_Item_Der:
                    Columnas_Congruentes.append(Col_CO)
                elif Es_Progresista and Es_Item_Der:
                    Columnas_Incongruentes.append(Col_CO)
                elif Es_Conservador and Es_Item_Izq:
                    Columnas_Incongruentes.append(Col_CO)

            elif Es_Derecha:
                if Es_Conservador and Es_Item_Der:
                    Columnas_Congruentes.append(Col_CO)
                elif Es_Progresista and Es_Item_Izq:
                    Columnas_Congruentes.append(Col_CO)
                elif Es_Conservador and Es_Item_Izq:
                    Columnas_Incongruentes.append(Col_CO)
                elif Es_Progresista and Es_Item_Der:
                    Columnas_Incongruentes.append(Col_CO)

    # Eliminar duplicados.
    Columnas_Congruentes = list(set(Columnas_Congruentes))
    Columnas_Incongruentes = list(set(Columnas_Incongruentes))

    # Calcular promedios.
    if Columnas_Congruentes:
        Df_Resultado['CO_Congruentes_Promedio'] = (
            Df_Resultado[Columnas_Congruentes].mean(axis=1)
        )
    else:
        Df_Resultado['CO_Congruentes_Promedio'] = None

    if Columnas_Incongruentes:
        Df_Resultado['CO_Incongruentes_Promedio'] = (
            Df_Resultado[Columnas_Incongruentes].mean(axis=1)
        )
    else:
        Df_Resultado['CO_Incongruentes_Promedio'] = None

    print(
        f"✓ Variables de congruencia creadas: "
        f"{len(Columnas_Congruentes)} congruentes, "
        f"{len(Columnas_Incongruentes)} incongruentes"
    )

    return Df_Resultado


# ============================================================
# FUNCIONES DE DIFERENCIA DE DIFERENCIAS (DIFDIF)
# ============================================================

def Calcular_DifDif_Para_Tipo(
    Df_Generales: pd.DataFrame,
    Df_Ballotage: pd.DataFrame,
    Tipo: str = 'CO'
) -> pd.DataFrame:

    """
    Calcula variables de Diferencia de Diferencias (DifDif)
    para un tipo específico (CO o CT).

    El DifDif mide cómo cambió la asimetría izquierda-derecha
    entre Generales y Ballotage.

    Fórmula:
    1. Dif_Gen = Izq - Der (en Generales)
    2. Dif_Bal = Izq - Der (en Ballotage)
    3. DifDif = Dif_Bal - Dif_Gen

    Interpretación:
    - DifDif > 0: Diferencia Izq-Der aumentó en Ballotage.
    - DifDif < 0: Diferencia Izq-Der disminuyó en Ballotage.
    - DifDif = 0: Sin cambio en asimetría Izq-Der.

    Parámetros:
    - Df_Generales: DataFrame de elecciones Generales.
    - Df_Ballotage: DataFrame de elecciones Ballotage.
    - Tipo: 'CO' (Cambio de Opinión) o 'CT' (Cambio de Tiempo).

    Retorna:
    - DataFrame con columnas Dif_Gen, Dif_Bal y DifDif.

    """

    if Tipo not in ['CO', 'CT']:
        print(
            f"⚠️ Tipo '{Tipo}' inválido. "
            f"Debe ser 'CO' o 'CT'."
        )
        return pd.DataFrame()

    # Verificar que ambos DataFrames tengan mismo número de filas.
    if len(Df_Generales) != len(Df_Ballotage):
        print(
            f"⚠️ Los DataFrames tienen diferente número "
            f"de filas."
        )
        print(
            f"   Generales: {len(Df_Generales)}, "
            f"Ballotage: {len(Df_Ballotage)}"
        )
        return pd.DataFrame()

    # DataFrame resultado.
    Df_Resultado = pd.DataFrame()

    # Para cada item IP.
    for Item in NUMEROS_ITEMS_IP:
        # Nombres de las variables.
        Var_Izq = f'{Tipo}_Item_{Item}_Izq'
        Var_Der = f'{Tipo}_Item_{Item}_Der'

        # Verificar que existan en ambos DataFrames.
        Existe_En_Gen = (
            Var_Izq in Df_Generales.columns and
            Var_Der in Df_Generales.columns
        )
        Existe_En_Bal = (
            Var_Izq in Df_Ballotage.columns and
            Var_Der in Df_Ballotage.columns
        )

        if Existe_En_Gen and Existe_En_Bal:
            # Paso 1: Diferencia en Generales (Izq - Der).
            Dif_Gen = (
                Df_Generales[Var_Izq] -
                Df_Generales[Var_Der]
            )

            # Paso 2: Diferencia en Ballotage (Izq - Der).
            Dif_Bal = (
                Df_Ballotage[Var_Izq] -
                Df_Ballotage[Var_Der]
            )

            # Paso 3: Diferencia de Diferencias.
            DifDif = Dif_Bal - Dif_Gen

            # Nombres de columnas resultado.
            Nombre_Dif_Gen = f'Dif_Gen_{Tipo}_Item_{Item}'
            Nombre_Dif_Bal = f'Dif_Bal_{Tipo}_Item_{Item}'
            Nombre_DifDif = f'DifDif_{Tipo}_Item_{Item}'

            # Agregar al DataFrame resultado.
            Df_Resultado[Nombre_Dif_Gen] = Dif_Gen
            Df_Resultado[Nombre_Dif_Bal] = Dif_Bal
            Df_Resultado[Nombre_DifDif] = DifDif

    print(
        f"✓ Calculadas {len(Df_Resultado.columns)} "
        f"variables para {Tipo}"
    )

    return Df_Resultado


def Calcular_Todas_Variables_DifDif(
    Df_Generales: pd.DataFrame,
    Df_Ballotage: pd.DataFrame,
    Incluir_CO: bool = True,
    Incluir_CT: bool = True
) -> pd.DataFrame:

    """
    Calcula todas las variables DifDif (CO y CT) entre
    Generales y Ballotage.

    Retorna un DataFrame con:
    - Columnas de identificación (ID, Categoria_PASO_2023).
    - Variables Dif_Gen, Dif_Bal y DifDif para CO.
    - Variables Dif_Gen, Dif_Bal y DifDif para CT.

    Parámetros:
    - Df_Generales: DataFrame de elecciones Generales.
    - Df_Ballotage: DataFrame de elecciones Ballotage.
    - Incluir_CO: Si calcular DifDif para CO.
    - Incluir_CT: Si calcular DifDif para CT.

    Retorna:
    - DataFrame con todas las variables DifDif.

    """

    print("\n" + "="*70)
    print("CÁLCULO DE DIFERENCIA DE DIFERENCIAS (DIFDIF)")
    print("="*70)

    Df_Elecciones = pd.DataFrame()

    # Calcular DifDif para CO.
    if Incluir_CO:
        print("\nCalculando DifDif para CO (Cambio de Opinión)...")
        Df_DifDif_CO = Calcular_DifDif_Para_Tipo(
            Df_Generales,
            Df_Ballotage,
            Tipo='CO'
        )
        Df_Elecciones = pd.concat(
            [Df_Elecciones, Df_DifDif_CO],
            axis=1
        )

    # Calcular DifDif para CT.
    if Incluir_CT:
        print("\nCalculando DifDif para CT (Cambio de Tiempo)...")
        Df_DifDif_CT = Calcular_DifDif_Para_Tipo(
            Df_Generales,
            Df_Ballotage,
            Tipo='CT'
        )
        Df_Elecciones = pd.concat(
            [Df_Elecciones, Df_DifDif_CT],
            axis=1
        )

    # Agregar columnas de identificación desde Generales.
    Columnas_Identificacion = ['Categoria_PASO_2023']

    if 'ID' in Df_Generales.columns:
        Columnas_Identificacion.insert(0, 'ID')

    for Col in Columnas_Identificacion:
        if Col in Df_Generales.columns:
            Df_Elecciones.insert(
                0,
                Col,
                Df_Generales[Col].values
            )

    # Contar variables DifDif.
    Columnas_DifDif = [
        col for col in Df_Elecciones.columns
        if col.startswith('DifDif')
    ]

    print("\n" + "="*70)
    print("RESUMEN DE VARIABLES DIFDIF")
    print("="*70)
    print(f"Total variables DifDif: {len(Columnas_DifDif)}")
    print(
        f"Dimensiones DataFrame: "
        f"{Df_Elecciones.shape[0]} filas × "
        f"{Df_Elecciones.shape[1]} columnas"
    )
    print("="*70 + "\n")

    return Df_Elecciones


# ============================================================
# FUNCIONES DE VARIABLES AGREGADAS (PROMEDIOS)
# ============================================================

def Calcular_Variables_Agregadas_CO(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Calcula variables agregadas (promedios) de Cambio de
    Opinión agrupando por tipo de item y dirección.

    Variables creadas:
    - CO_Pro: Promedio de todos los CO progresistas.
    - CO_Pro_Izq: Promedio CO progresistas izquierda.
    - CO_Pro_Der: Promedio CO progresistas derecha.
    - CO_Con: Promedio de todos los CO conservadores.
    - CO_Con_Izq: Promedio CO conservadores izquierda.
    - CO_Con_Der: Promedio CO conservadores derecha.

    Parámetros:
    - Df: DataFrame con variables CO individuales.

    Retorna:
    - DataFrame con nuevas columnas agregadas.

    """

    Df_Resultado = Df.copy()

    # Listas de columnas para progresistas.
    Columnas_CO_Pro_Izq = [
        f'CO_Item_{Item}_Izq'
        for Item in ITEMS_PROGRESISTAS
    ]
    Columnas_CO_Pro_Der = [
        f'CO_Item_{Item}_Der'
        for Item in ITEMS_PROGRESISTAS
    ]
    Columnas_CO_Pro = Columnas_CO_Pro_Izq + Columnas_CO_Pro_Der

    # Listas de columnas para conservadores.
    Columnas_CO_Con_Izq = [
        f'CO_Item_{Item}_Izq'
        for Item in ITEMS_CONSERVADORES
    ]
    Columnas_CO_Con_Der = [
        f'CO_Item_{Item}_Der'
        for Item in ITEMS_CONSERVADORES
    ]
    Columnas_CO_Con = Columnas_CO_Con_Izq + Columnas_CO_Con_Der

    # Verificar que existan las columnas necesarias.
    Columnas_Existentes = set(Df_Resultado.columns)

    # Filtrar solo columnas que existan.
    Columnas_CO_Pro_Izq = [
        c for c in Columnas_CO_Pro_Izq
        if c in Columnas_Existentes
    ]
    Columnas_CO_Pro_Der = [
        c for c in Columnas_CO_Pro_Der
        if c in Columnas_Existentes
    ]
    Columnas_CO_Pro = [
        c for c in Columnas_CO_Pro
        if c in Columnas_Existentes
    ]
    Columnas_CO_Con_Izq = [
        c for c in Columnas_CO_Con_Izq
        if c in Columnas_Existentes
    ]
    Columnas_CO_Con_Der = [
        c for c in Columnas_CO_Con_Der
        if c in Columnas_Existentes
    ]
    Columnas_CO_Con = [
        c for c in Columnas_CO_Con
        if c in Columnas_Existentes
    ]

    # Calcular promedios.
    if Columnas_CO_Pro:
        Df_Resultado['CO_Pro'] = (
            Df_Resultado[Columnas_CO_Pro].mean(axis=1)
        )
    if Columnas_CO_Pro_Izq:
        Df_Resultado['CO_Pro_Izq'] = (
            Df_Resultado[Columnas_CO_Pro_Izq].mean(axis=1)
        )
    if Columnas_CO_Pro_Der:
        Df_Resultado['CO_Pro_Der'] = (
            Df_Resultado[Columnas_CO_Pro_Der].mean(axis=1)
        )
    if Columnas_CO_Con:
        Df_Resultado['CO_Con'] = (
            Df_Resultado[Columnas_CO_Con].mean(axis=1)
        )
    if Columnas_CO_Con_Izq:
        Df_Resultado['CO_Con_Izq'] = (
            Df_Resultado[Columnas_CO_Con_Izq].mean(axis=1)
        )
    if Columnas_CO_Con_Der:
        Df_Resultado['CO_Con_Der'] = (
            Df_Resultado[Columnas_CO_Con_Der].mean(axis=1)
        )

    print("✓ Variables agregadas CO creadas.")

    return Df_Resultado


def Calcular_Variables_Agregadas_CT(
    Df: pd.DataFrame
) -> pd.DataFrame:

    """
    Calcula variables agregadas (promedios) de Cambio de
    Tiempo agrupando por tipo de item y dirección.

    Variables creadas:
    - CT_Pro: Promedio de todos los CT progresistas.
    - CT_Pro_Izq: Promedio CT progresistas izquierda.
    - CT_Pro_Der: Promedio CT progresistas derecha.
    - CT_Con: Promedio de todos los CT conservadores.
    - CT_Con_Izq: Promedio CT conservadores izquierda.
    - CT_Con_Der: Promedio CT conservadores derecha.

    Parámetros:
    - Df: DataFrame con variables CT individuales.

    Retorna:
    - DataFrame con nuevas columnas agregadas.

    """

    Df_Resultado = Df.copy()

    # Listas de columnas para progresistas.
    Columnas_CT_Pro_Izq = [
        f'CT_Item_{Item}_Izq'
        for Item in ITEMS_PROGRESISTAS
    ]
    Columnas_CT_Pro_Der = [
        f'CT_Item_{Item}_Der'
        for Item in ITEMS_PROGRESISTAS
    ]
    Columnas_CT_Pro = Columnas_CT_Pro_Izq + Columnas_CT_Pro_Der

    # Listas de columnas para conservadores.
    Columnas_CT_Con_Izq = [
        f'CT_Item_{Item}_Izq'
        for Item in ITEMS_CONSERVADORES
    ]
    Columnas_CT_Con_Der = [
        f'CT_Item_{Item}_Der'
        for Item in ITEMS_CONSERVADORES
    ]
    Columnas_CT_Con = Columnas_CT_Con_Izq + Columnas_CT_Con_Der

    # Verificar que existan las columnas necesarias.
    Columnas_Existentes = set(Df_Resultado.columns)

    # Filtrar solo columnas que existan.
    Columnas_CT_Pro_Izq = [
        c for c in Columnas_CT_Pro_Izq
        if c in Columnas_Existentes
    ]
    Columnas_CT_Pro_Der = [
        c for c in Columnas_CT_Pro_Der
        if c in Columnas_Existentes
    ]
    Columnas_CT_Pro = [
        c for c in Columnas_CT_Pro
        if c in Columnas_Existentes
    ]
    Columnas_CT_Con_Izq = [
        c for c in Columnas_CT_Con_Izq
        if c in Columnas_Existentes
    ]
    Columnas_CT_Con_Der = [
        c for c in Columnas_CT_Con_Der
        if c in Columnas_Existentes
    ]
    Columnas_CT_Con = [
        c for c in Columnas_CT_Con
        if c in Columnas_Existentes
    ]

    # Calcular promedios.
    if Columnas_CT_Pro:
        Df_Resultado['CT_Pro'] = (
            Df_Resultado[Columnas_CT_Pro].mean(axis=1)
        )
    if Columnas_CT_Pro_Izq:
        Df_Resultado['CT_Pro_Izq'] = (
            Df_Resultado[Columnas_CT_Pro_Izq].mean(axis=1)
        )
    if Columnas_CT_Pro_Der:
        Df_Resultado['CT_Pro_Der'] = (
            Df_Resultado[Columnas_CT_Pro_Der].mean(axis=1)
        )
    if Columnas_CT_Con:
        Df_Resultado['CT_Con'] = (
            Df_Resultado[Columnas_CT_Con].mean(axis=1)
        )
    if Columnas_CT_Con_Izq:
        Df_Resultado['CT_Con_Izq'] = (
            Df_Resultado[Columnas_CT_Con_Izq].mean(axis=1)
        )
    if Columnas_CT_Con_Der:
        Df_Resultado['CT_Con_Der'] = (
            Df_Resultado[Columnas_CT_Con_Der].mean(axis=1)
        )

    print("✓ Variables agregadas CT creadas.")

    return Df_Resultado


# ============================================================
# FUNCIONES WRAPPER
# ============================================================

def Calcular_Variables_Cambio(
    Diccionario_Dfs: dict,
    Incluir_Congruencia: bool = True,
    Incluir_Agregadas: bool = True
) -> dict:

    """
    Calcula variables CO y CT para todos los DataFrames en
    el diccionario.

    Parámetros:
    - Diccionario_Dfs: Diccionario con DataFrames.
    - Incluir_Congruencia: Si calcular CO_Congruentes e
      CO_Incongruentes.
    - Incluir_Agregadas: Si calcular variables agregadas
      (promedios por tipo).

    Retorna:
    - Diccionario actualizado con variables de cambio.

    """

    print("\nCalculando variables de Cambio de Opinión...")
    Diccionario_Dfs = Crear_Columnas_Cambio_Opinion(
        Diccionario_Dfs
    )
    print("✓ Variables CO creadas.")

    print("\nCalculando variables de Cambio de Tiempo...")
    Diccionario_Dfs = Crear_Columnas_Cambio_Tiempo(
        Diccionario_Dfs
    )
    print("✓ Variables CT creadas.")

    if Incluir_Agregadas:
        print(
            "\nCalculando variables agregadas "
            "(promedios por tipo)..."
        )
        for Nombre_Df, Df in Diccionario_Dfs.items():
            Df = Calcular_Variables_Agregadas_CO(Df)
            Df = Calcular_Variables_Agregadas_CT(Df)
            Diccionario_Dfs[Nombre_Df] = Df
        print("✓ Variables agregadas creadas.\n")

    if Incluir_Congruencia:
        print(
            "\nCalculando variables de congruencia "
            "(CO_Congruentes/Incongruentes)..."
        )
        for Nombre_Df, Df in Diccionario_Dfs.items():
            Diccionario_Dfs[Nombre_Df] = (
                Calcular_CO_Congruentes_E_Incongruentes(Df)
            )
        print("✓ Variables de congruencia creadas.\n")
    else:
        print()

    return Diccionario_Dfs


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    print("Módulo de variables de cambio cargado.")
