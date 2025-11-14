# ============================================================
# FUNCIONES_COMUNES.PY
# ============================================================
# Funciones reutilizables para procesamiento de datos del
# experimento de personalidad implícita y política.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

from typing import Any, Dict, List
import pandas as pd
import re
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


# ============================================================
# PROCESAMIENTO DE JSON Y EXTRACCION DE DATOS
# ============================================================

def Crear_Variables_De_Orden_IP_Items(
    Data_Frame: pd.DataFrame
) -> pd.DataFrame:

    """
    Procesa el DataFrame completo para extraer orden de IP Items
    y último Item desde la columna 'results' con formato JSON.

    Parámetros:
    - Data_Frame: DataFrame con columna 'results' en JSON.

    Retorna:
    - DataFrame con columnas 'Orden_IP_Items' y 'Ultimo_IP_Item'.

    """

    def Extraer_Datos_JSON(Fila_JSON):

        """
        Función interna para extraer datos de cada fila JSON.

        """

        try:
            # Convertir string JSON a diccionario Python.
            Datos_Sujeto = json.loads(Fila_JSON)

            # Extraer orden de aparición de IP Items.
            Orden_IP_Items = [
                int(Clave.split('_')[-1]) for Clave in
                Datos_Sujeto['results'][1]['fase_3']['IP'].keys()
                if Clave.startswith('IP_item_')
            ]

            # Obtener el último IP Item de la lista.
            Ultimo_IP_Item = (
                Orden_IP_Items[-1] if Orden_IP_Items else None
            )

            return Orden_IP_Items, Ultimo_IP_Item

        except (KeyError, IndexError, json.JSONDecodeError):
            # En caso de error, retornar valores vacíos.
            return [], None

    # Aplicar la función a todas las filas del DataFrame.
    Resultados_Procesados = Data_Frame['results'].apply(
        Extraer_Datos_JSON
    )

    # Agregar las nuevas columnas al DataFrame.
    Data_Frame['Orden_IP_Items'] = [
        Resultado[0] for Resultado in Resultados_Procesados
    ]
    Data_Frame['Ultimo_IP_Item'] = [
        Resultado[1] for Resultado in Resultados_Procesados
    ]

    return Data_Frame


def Crear_Variables_De_Orden_IP_Items_Asociados(
    Data_Frame: pd.DataFrame
) -> pd.DataFrame:

    """
    Procesa el DataFrame para extraer orden de IP Items asociados
    a candidatos (con sufijos _Izq/_Der) y último Item.

    Parámetros:
    - Data_Frame: DataFrame con columna 'results' en JSON.

    Retorna:
    - DataFrame con columnas 'Orden_IP_Items_Asociados' y
      'Ultimo_IP_Item_Asociado'.

    """

    Lista_Orden_IP_Items = []
    Lista_Ultimo_IP_Item = []

    for Fila_JSON in Data_Frame['results']:
        try:
            # Convertir el string JSON a diccionario Python.
            Datos_Sujeto = json.loads(Fila_JSON)

            # Extraer números de IP Items con sufijo _Izq/_Der.
            Orden_IP_Items = [
                Clave.split('_')[2] + '_' + Clave.split('_')[3]
                for Clave in
                Datos_Sujeto['results'][1]['fase_3'][
                    'IP_modificada'
                ].keys()
                if (Clave.startswith('IP_item_') and
                    len(Clave.split('_')) > 3)
            ]

            # Obtener el último IP Item de la lista.
            Ultimo_IP_Item = (
                Orden_IP_Items[-1] if Orden_IP_Items else None
            )

            Lista_Orden_IP_Items.append(Orden_IP_Items)
            Lista_Ultimo_IP_Item.append(Ultimo_IP_Item)

        except (KeyError, IndexError, json.JSONDecodeError):
            # En caso de error, agregar valores vacíos.
            Lista_Orden_IP_Items.append([])
            Lista_Ultimo_IP_Item.append(None)

    # Agregar las nuevas columnas al DataFrame.
    Data_Frame['Orden_IP_Items_Asociados'] = Lista_Orden_IP_Items
    Data_Frame['Ultimo_IP_Item_Asociado'] = Lista_Ultimo_IP_Item

    return Data_Frame


def Crear_Primeros_IP_Items_Asociados(
    Data_Frame: pd.DataFrame,
    Numero_Primeros: int
) -> pd.DataFrame:

    """
    Crea columna con los primeros N elementos de
    'Orden_IP_Items_Asociados'.

    Parámetros:
    - Data_Frame: DataFrame con columna
                  'Orden_IP_Items_Asociados'.
    - Numero_Primeros: Número de primeros elementos a extraer.

    Retorna:
    - DataFrame con columna 'Primeros_IP_Items_Asociados'.

    """

    # Crear columna tomando primeros n elementos de cada lista.
    Data_Frame['Primeros_IP_Items_Asociados'] = (
        Data_Frame['Orden_IP_Items_Asociados'].apply(
            lambda lista: (
                lista[:Numero_Primeros]
                if (isinstance(lista, list) and
                    len(lista) >= Numero_Primeros)
                else lista
            )
        )
    )

    return Data_Frame


def Aplanar_Diccionario(
    Diccionario: Dict,
    Prefijo: str = ''
) -> Dict:

    """
    Convierte un diccionario anidado en uno plano usando puntos
    para separar niveles de anidamiento.

    Parámetros:
    - Diccionario: Diccionario anidado a aplanar.
    - Prefijo: Prefijo para las claves (uso interno recursivo).

    Retorna:
    - Diccionario plano con claves concatenadas.

    """

    Diccionario_Plano = {}

    for Clave, Valor in Diccionario.items():
        Nueva_Clave = f"{Prefijo}.{Clave}" if Prefijo else Clave

        if isinstance(Valor, dict):
            # Recursión para diccionarios anidados.
            Diccionario_Plano.update(
                Aplanar_Diccionario(Valor, Nueva_Clave)
            )
        elif isinstance(Valor, list):
            # Si la lista tiene un solo elemento, extraerlo.
            if len(Valor) == 1:
                Diccionario_Plano[Nueva_Clave] = Valor[0]
            else:
                # Convertir listas a strings separados por comas.
                Diccionario_Plano[Nueva_Clave] = ', '.join(
                    map(str, Valor)
                )
        else:
            Diccionario_Plano[Nueva_Clave] = Valor

    return Diccionario_Plano


def Procesar_Columna_Results(
    Data_Frame: pd.DataFrame
) -> pd.DataFrame:

    """
    Extrae y procesa la columna 'results' de un DataFrame,
    convirtiendo el contenido JSON en DataFrame de pandas.
    Maneja valores NaN y datos faltantes.

    Parámetros:
    - Data_Frame: DataFrame con columna 'results' en JSON.

    Retorna:
    - DataFrame procesado con datos aplanados.

    """

    # Extraer solo la columna 'results'.
    Columna_Results = Data_Frame['results']

    # Lista para almacenar los datos procesados.
    Lista_Datos_Procesados = []

    # Procesar cada fila de la columna results.
    for Indice, Contenido_JSON in enumerate(Columna_Results):
        try:
            # Verificar si el contenido no es NaN o nulo.
            if pd.isna(Contenido_JSON) or Contenido_JSON is None:
                continue

            # Verificar que sea string.
            if not isinstance(Contenido_JSON, str):
                continue

            # Convertir el string JSON a diccionario Python.
            Datos_JSON = json.loads(Contenido_JSON)

            # Extraer el array 'results' del JSON.
            Array_Results = Datos_JSON.get('results', [])

            # Agregar identificadores para mantener trazabilidad.
            Fila_Procesada = {
                'id': Datos_JSON.get('subject')
            }

            # Procesar cada elemento del array results.
            for Item in Array_Results:
                if isinstance(Item, dict):
                    # Aplanar el diccionario anidado.
                    Datos_Aplanados = Aplanar_Diccionario(Item)
                    Fila_Procesada.update(Datos_Aplanados)

            Lista_Datos_Procesados.append(Fila_Procesada)

        except json.JSONDecodeError as Error:
            continue
        except Exception as Error:
            continue

    # Verificar si se procesaron datos.
    if not Lista_Datos_Procesados:
        return pd.DataFrame()

    # Crear DataFrame con los datos procesados.
    DataFrame_Final = pd.DataFrame(Lista_Datos_Procesados)

    return DataFrame_Final


# ============================================================
# LIMPIEZA Y RELLENO DE DATOS
# ============================================================

def Rellenar_IP_Items_Asociados_Faltantes(
    Data_Frame: pd.DataFrame
) -> pd.DataFrame:

    """
    Rellena valores faltantes en columnas IP_Item_X_Izq/Der
    cuando uno tiene valor y el otro es NaN, usando la mediana
    por categoría ideológica.

    Parámetros:
    - Data_Frame: DataFrame con columnas IP_Item_X_Izq/Der.

    Retorna:
    - DataFrame con valores faltantes rellenados.

    """

    # Obtener todos los números de IP_Items únicos.
    Numeros_IP = set()
    for Columna in Data_Frame.columns:
        if ('IP_Item_' in Columna and
            ('_Izq_' in Columna or '_Der_' in Columna)):
            # Extraer número del Item.
            Partes = Columna.split('_')
            if len(Partes) >= 3:
                Numero = Partes[2]
                Numeros_IP.add(Numero)

    Total_Rellenos = 0

    # Para cada número de IP_Item, procesar Respuesta y Tiempo.
    for Numero in sorted(Numeros_IP):
        for Tipo in ['Respuesta', 'Tiempo']:
            Col_Izq = f'IP_Item_{Numero}_Izq_{Tipo}'
            Col_Der = f'IP_Item_{Numero}_Der_{Tipo}'

            # Verificar que ambas columnas existen.
            if Col_Izq in Data_Frame.columns and Col_Der in Data_Frame.columns:

                # Convertir a numérico si es necesario.
                Data_Frame[Col_Izq] = pd.to_numeric(
                    Data_Frame[Col_Izq],
                    errors='coerce'
                )
                Data_Frame[Col_Der] = pd.to_numeric(
                    Data_Frame[Col_Der],
                    errors='coerce'
                )

                # Encontrar filas donde uno tiene valor y otro NaN.
                Mask_Izq_Lleno_Der_Vacio = (
                    Data_Frame[Col_Izq].notna() &
                    Data_Frame[Col_Der].isna()
                )
                Mask_Der_Lleno_Izq_Vacio = (
                    Data_Frame[Col_Der].notna() &
                    Data_Frame[Col_Izq].isna()
                )

                # Calcular medianas por categoría para cada columna.
                Medianas_Izq = Data_Frame.groupby(
                    'Categoria_PASO_2023'
                )[Col_Izq].median()
                Medianas_Der = Data_Frame.groupby(
                    'Categoria_PASO_2023'
                )[Col_Der].median()

                # Rellenar valores faltantes en Der cuando Izq
                # tiene valor.
                Rellenos_Der = 0
                for Indice in Data_Frame[
                    Mask_Izq_Lleno_Der_Vacio
                ].index:
                    Categoria = Data_Frame.loc[
                        Indice,
                        'Categoria_PASO_2023'
                    ]

                    if (Categoria in Medianas_Der.index and
                        pd.notna(Medianas_Der[Categoria])):
                        Valor_Mediana = Medianas_Der[Categoria]
                        Data_Frame.loc[Indice, Col_Der] = (
                            Valor_Mediana
                        )
                        Rellenos_Der += 1

                # Rellenar valores faltantes en Izq cuando Der
                # tiene valor.
                Rellenos_Izq = 0
                for Indice in Data_Frame[
                    Mask_Der_Lleno_Izq_Vacio
                ].index:
                    Categoria = Data_Frame.loc[
                        Indice,
                        'Categoria_PASO_2023'
                    ]

                    if (Categoria in Medianas_Izq.index and
                        pd.notna(Medianas_Izq[Categoria])):
                        Valor_Mediana = Medianas_Izq[Categoria]
                        Data_Frame.loc[Indice, Col_Izq] = (
                            Valor_Mediana
                        )
                        Rellenos_Izq += 1

                Total_Rellenos += Rellenos_Der + Rellenos_Izq

    return Data_Frame


def Eliminar_Primeros_Datos_IP_Items_Asociados(
    Data_Frame: pd.DataFrame
) -> pd.DataFrame:

    """
    Elimina datos (no columnas) de IP Items basándose en
    'Orden_IP_Items_Asociados'. Toma primeros números únicos
    necesarios para obtener exactamente 3 números diferentes.
    Para cada IP Item, elimina tanto versión _Izq como _Der.

    Parámetros:
    - Data_Frame: DataFrame con columna
                  'Orden_IP_Items_Asociados'.

    Retorna:
    - DataFrame con datos eliminados (valores = NaN).

    """

    # Crear copia del DataFrame.
    df_Modificado = Data_Frame.copy()

    # Sufijos de columnas a eliminar.
    Sufijos = ['_Respuesta', '_Candidato', '_Tiempo']

    # Iterar por cada fila del DataFrame.
    for Index, Fila in df_Modificado.iterrows():

        # Obtener lista de orden de IP Items para esta fila.
        Orden_IP_Items = Fila['Orden_IP_Items_Asociados']

        # Si la lista no está vacía o no es NaN.
        if isinstance(Orden_IP_Items, list) and len(
            Orden_IP_Items
        ) > 0:

            # Tomar ítems hasta obtener 3 números únicos.
            Numeros_IP_Unicos = set()
            Items_A_Procesar = []

            # Recorrer lista de orden hasta obtener 3 únicos.
            for Item in Orden_IP_Items:
                if isinstance(Item, str) and '_' in Item:
                    # Extraer solo el número.
                    Numero = Item.split('_')[0]

                    # Agregar el ítem a procesar.
                    Items_A_Procesar.append(Item)
                    Numeros_IP_Unicos.add(Numero)

                    # Parar cuando tengamos 3 números únicos.
                    if len(Numeros_IP_Unicos) >= 3:
                        break

            # Eliminar datos para 3 números únicos encontrados.
            for Numero in Numeros_IP_Unicos:
                for Direccion in ['_Izq', '_Der']:
                    for Sufijo in Sufijos:
                        # Construir nombre de la columna.
                        Columna = (
                            f'IP_Item_{Numero}{Direccion}{Sufijo}'
                        )

                        # Si columna existe, eliminar el dato.
                        if Columna in df_Modificado.columns:
                            df_Modificado.at[Index, Columna] = (
                                pd.NA
                            )

    return df_Modificado


def Eliminar_Filas_Por_Desviacion_Estandar(
    Data_Frame: pd.DataFrame,
    Columnas_Tiempo: List[str],
    Numero_Desviaciones: int = 3
) -> pd.DataFrame:

    """
    Elimina filas donde algún valor de tiempo exceda el número
    especificado de desvíos estándar desde la media global de
    todas las columnas de tiempo.

    Parámetros:
    - Data_Frame: DataFrame a procesar.
    - Columnas_Tiempo: Lista de nombres de columnas a analizar.
    - Numero_Desviaciones: Número de desvíos estándar límite.

    Retorna:
    - DataFrame con las filas válidas únicamente.

    """

    # Filtrar columnas que existen en el DataFrame.
    Columnas_Existentes: List[str] = [
        Columna for Columna in Columnas_Tiempo
        if Columna in Data_Frame.columns
    ]
    if len(Columnas_Existentes) == 0:
        print(
            "⚠️ Ninguna columna de tiempo encontrada;"
        )
        print("   regresando el DataFrame sin cambios.")
        return Data_Frame

    # Recopilar todos los valores numéricos no nulos.
    Todos_Los_Valores: List[float] = []
    for Columna in Columnas_Existentes:
        Valores_Limpios = pd.to_numeric(
            Data_Frame[Columna],
            errors='coerce'
        ).dropna().tolist()
        Todos_Los_Valores.extend(Valores_Limpios)

    if len(Todos_Los_Valores) == 0:
        print(
            "⚠️ No hay valores numéricos para calcular "
            "estadísticos;"
        )
        print("   regresando el DataFrame sin cambios.")
        return Data_Frame

    # Calcular estadísticos globales.
    Media_Global: float = (
        sum(Todos_Los_Valores) / len(Todos_Los_Valores)
    )
    Varianza: float = sum(
        (Valor - Media_Global) ** 2
        for Valor in Todos_Los_Valores
    ) / len(Todos_Los_Valores)
    Desviacion_Estandar_Global: float = Varianza ** 0.5
    Limite_Superior: float = Media_Global + (
        Numero_Desviaciones * Desviacion_Estandar_Global
    )

    print(f"Media global: {Media_Global:.2f}")
    print(
        f"Desvío estándar global: "
        f"{Desviacion_Estandar_Global:.2f}"
    )
    print(
        f"Límite superior ({Numero_Desviaciones} desvíos): "
        f"{Limite_Superior:.2f}"
    )

    # Detectar y eliminar filas con al menos un valor atípico.
    Filas_Validas: List[int] = []
    for Indice, Fila in Data_Frame.iterrows():
        Fila_Valida = True
        for Columna in Columnas_Existentes:
            Valor = pd.to_numeric(Fila[Columna], errors='coerce')
            # Asegurar que Valor es escalar, no Serie.
            if isinstance(Valor, pd.Series):
                if not Valor.empty:
                    Valor = Valor.iloc[0]
                else:
                    continue
            if pd.notna(Valor) and Valor > Limite_Superior:
                print(
                    f"Eliminando fila ID={Fila.get('ID', Indice)}: "
                    f"{Columna}={Valor:.2f} supera "
                    f"{Limite_Superior:.2f}"
                )
                Fila_Valida = False
                break
        if Fila_Valida:
            Filas_Validas.append(Indice)  # type: ignore

    Data_Frame_Resultante = Data_Frame.loc[Filas_Validas]

    return Data_Frame_Resultante


# ============================================================
# CREACION DE VARIABLES DE CAMBIO
# ============================================================

def Crear_Columnas_Cambio_Opinion(
    Diccionario_Dataframes: Dict[str, pd.DataFrame]
) -> Dict[str, pd.DataFrame]:

    """
    Crea columnas de cambio de opinión (CO) para cada ítem IP
    comparando respuestas con candidatos de izquierda/derecha
    versus respuestas base de cada ítem.

    Parámetros:
    - Diccionario_Dataframes: Diccionario con DataFrames.

    Retorna:
    - Diccionario con DataFrames actualizados.

    """

    # Lista de números de ítems IP disponibles.
    Items_IP = [
        3, 4, 5, 6, 7, 8, 9, 10, 11, 16,
        19, 20, 22, 23, 24, 25, 27, 28, 29, 30
    ]

    for Nombre_Df, Dataframe in Diccionario_Dataframes.items():

        for Numero_Item in Items_IP:

            # Nombres de las columnas base y con candidatos.
            Columna_Base = f'IP_Item_{Numero_Item}_Respuesta'
            Columna_Izq = f'IP_Item_{Numero_Item}_Izq_Respuesta'
            Columna_Der = f'IP_Item_{Numero_Item}_Der_Respuesta'

            # Nombres de las nuevas columnas de cambio opinión.
            Nueva_Columna_Izq = f'CO_Item_{Numero_Item}_Izq'
            Nueva_Columna_Der = f'CO_Item_{Numero_Item}_Der'

            # Verificar que todas las columnas necesarias existen.
            if all(
                Columna in Dataframe.columns for Columna in
                [Columna_Base, Columna_Izq, Columna_Der]
            ):

                # Convertir a numérico manteniendo NaN.
                Base_Numerica = pd.to_numeric(
                    Dataframe[Columna_Base],
                    errors='coerce'
                )
                Izq_Numerica = pd.to_numeric(
                    Dataframe[Columna_Izq],
                    errors='coerce'
                )
                Der_Numerica = pd.to_numeric(
                    Dataframe[Columna_Der],
                    errors='coerce'
                )

                # Calcular cambio de opinión.
                Dataframe[Nueva_Columna_Izq] = (
                    Izq_Numerica - Base_Numerica
                )
                Dataframe[Nueva_Columna_Der] = (
                    Der_Numerica - Base_Numerica
                )

    return Diccionario_Dataframes


def Crear_Columnas_Cambio_Tiempo(
    Diccionario_Dataframes: Dict[str, pd.DataFrame]
) -> Dict[str, pd.DataFrame]:

    """
    Crea columnas de cambio de tiempo (CT) para cada ítem IP
    comparando tiempos de respuesta con candidatos de
    izquierda/derecha versus tiempos base de cada ítem.

    Parámetros:
    - Diccionario_Dataframes: Diccionario con DataFrames.

    Retorna:
    - Diccionario con DataFrames actualizados.

    """

    # Lista de números de ítems IP disponibles.
    Items_IP = [
        3, 4, 5, 6, 7, 8, 9, 10, 11, 16,
        19, 20, 22, 23, 24, 25, 27, 28, 29, 30
    ]

    for Nombre_Df, Dataframe in Diccionario_Dataframes.items():

        for Numero_Item in Items_IP:

            # Nombres de columnas base y con candidatos (tiempo).
            Columna_Base = f'IP_Item_{Numero_Item}_Tiempo'
            Columna_Izq = f'IP_Item_{Numero_Item}_Izq_Tiempo'
            Columna_Der = f'IP_Item_{Numero_Item}_Der_Tiempo'

            # Nombres de las nuevas columnas de cambio tiempo.
            Nueva_Columna_Izq = f'CT_Item_{Numero_Item}_Izq'
            Nueva_Columna_Der = f'CT_Item_{Numero_Item}_Der'

            # Verificar que todas las columnas necesarias existen.
            if all(
                Columna in Dataframe.columns for Columna in
                [Columna_Base, Columna_Izq, Columna_Der]
            ):

                # Convertir a numérico manteniendo NaN.
                Base_Numerica = pd.to_numeric(
                    Dataframe[Columna_Base],
                    errors='coerce'
                )
                Izq_Numerica = pd.to_numeric(
                    Dataframe[Columna_Izq],
                    errors='coerce'
                )
                Der_Numerica = pd.to_numeric(
                    Dataframe[Columna_Der],
                    errors='coerce'
                )

                # Calcular cambio de tiempo.
                Dataframe[Nueva_Columna_Izq] = (
                    Izq_Numerica - Base_Numerica
                )
                Dataframe[Nueva_Columna_Der] = (
                    Der_Numerica - Base_Numerica
                )

    return Diccionario_Dataframes


# ============================================================
# VISUALIZACION
# ============================================================

def Limpiar_Texto(Texto: str) -> str:

    """
    Limpia texto removiendo guiones bajos y capitalizando solo
    la primera letra.

    Parámetros:
    - Texto: Texto a limpiar.

    Retorna:
    - Texto limpio.

    """

    return Texto.replace('_', ' ').capitalize()


def Crear_Boxplots_Items(
    Data_Frame: pd.DataFrame,
    Diccionario_Items: dict[int, dict[str, Any]],
    Tipo_Columna: str = 'IP_Respuesta',
    Nombre_Df: str = 'df'
) -> None:

    """
    Crea boxplots para cada ítem segmentado por categoría
    PASO 2023, incluyendo IP, CO y CT. Guarda cada gráfico
    en formatos PNG y SVG en la carpeta 'Boxplots/'.
    Aplica límites verticales según tipo de columna y usa
    colores específicos por categoría.

    Parámetros:
    - Data_Frame: DataFrame sobre el que graficar.
    - Diccionario_Items: metadata de cada ítem.
    - Tipo_Columna: tipo de datos a graficar.
    - Nombre_Df: nombre para los archivos de salida.

    """

    # Crear carpeta si no existe.
    os.makedirs("Boxplots", exist_ok=True)

    Mapa_Colores_Categorias = {
        'Progressivism': '#0078bf',
        'Moderate_Right_A': '#f7d117',
        'Moderate_Right_B': '#f7d117',
        'Left_Wing': '#f65058',
        'Blank': '#FFFFFF',
        'Centre': '#009cdd',
        'Right_Wing_Libertarian': '#753bbd'
    }

    Items_Disponibles: dict[int, dict[str, Any]] = {}
    for Numero_Item, Info_Item in Diccionario_Items.items():

        if Tipo_Columna == 'IP_Respuesta':
            Nombre_Columna = f'IP_Item_{Numero_Item}_Respuesta'
        elif Tipo_Columna == 'IP_Izq_Respuesta':
            Nombre_Columna = (
                f'IP_Item_{Numero_Item}_Izq_Respuesta'
            )
        elif Tipo_Columna == 'IP_Der_Respuesta':
            Nombre_Columna = (
                f'IP_Item_{Numero_Item}_Der_Respuesta'
            )
        elif Tipo_Columna == 'IP_Tiempo':
            Nombre_Columna = f'IP_Item_{Numero_Item}_Tiempo'
        elif Tipo_Columna == 'IP_Izq_Tiempo':
            Nombre_Columna = f'IP_Item_{Numero_Item}_Izq_Tiempo'
        elif Tipo_Columna == 'IP_Der_Tiempo':
            Nombre_Columna = f'IP_Item_{Numero_Item}_Der_Tiempo'
        elif Tipo_Columna in [
            'CO_Pro_Izq',
            'CO_Con_Izq',
            'CO_Pro_Der',
            'CO_Con_Der'
        ]:
            Nombre_Columna = f'CO_Item_{Numero_Item}_Izq' if (
                'Izq' in Tipo_Columna
            ) else f'CO_Item_{Numero_Item}_Der'
        elif Tipo_Columna in [
            'CT_Pro_Izq',
            'CT_Con_Izq',
            'CT_Pro_Der',
            'CT_Con_Der'
        ]:
            Nombre_Columna = f'CT_Item_{Numero_Item}_Izq' if (
                'Izq' in Tipo_Columna
            ) else f'CT_Item_{Numero_Item}_Der'
        else:
            continue

        if Nombre_Columna in Data_Frame.columns:
            Items_Disponibles[Numero_Item] = {
                'Info': Info_Item,
                'Columna': Nombre_Columna
            }

    if not Items_Disponibles:
        print(f"No hay columnas del tipo {Tipo_Columna}")
        return

    Num_Items = len(Items_Disponibles)
    Filas = int(np.ceil(Num_Items / 3))
    Columnas = min(3, Num_Items)

    Figura, Graficos = plt.subplots(
        Filas,
        Columnas,
        figsize=(50, 5 * Filas)
    )

    Graficos_Aplanados = np.array(Graficos).flatten()

    for IDX, (Num_Item, Item_Data) in enumerate(
        Items_Disponibles.items()
    ):
        Grafico = Graficos_Aplanados[IDX]
        Columna = Item_Data['Columna']

        Datos = Data_Frame.dropna(
            subset=[Columna, 'Categoria_PASO_2023']
        )
        Datos = Datos[
            ~Datos['Categoria_PASO_2023'].isin(
                ['No apply', 'No response', 'Other']
            )
        ]

        if Datos.empty:
            Grafico.text(
                0.5,
                0.5,
                'Sin datos válidos',
                ha='center',
                va='center',
                transform=Grafico.transAxes
            )
        else:
            Orden_Categorias = [
                'Left_Wing',
                'Progressivism',
                'Centre',
                'Moderate_Right_A',
                'Moderate_Right_B',
                'Right_Wing_Libertarian'
            ]
            Paleta_Colores = [
                Mapa_Colores_Categorias.get(cat, '#999999')
                for cat in Orden_Categorias
            ]
            sns.boxplot(
                data=Datos,
                x='Categoria_PASO_2023',
                y=Columna,
                order=Orden_Categorias,
                palette=Paleta_Colores,
                ax=Grafico
            )
            Etiquetas_Categorias = []
            for Categoria in Orden_Categorias:
                Subdatos = Datos[
                    Datos['Categoria_PASO_2023'] == Categoria
                ][Columna]
                if not Subdatos.empty:
                    Media = Subdatos.mean()
                    if abs(Media) < 1:
                        Etiqueta = (
                            f"{Categoria.replace('_', ' ')}\n"
                            f"({Media:.3f})"
                        )
                    else:
                        Etiqueta = (
                            f"{Categoria.replace('_', ' ')}\n"
                            f"({Media:.2f})"
                        )
                else:
                    Etiqueta = (
                        Categoria.replace('_', ' ') + "\n(N/A)"
                    )
                Etiquetas_Categorias.append(Etiqueta)

            Grafico.set_xticklabels(
                Etiquetas_Categorias,
                rotation=45,
                ha='right'
            )
            Grafico.set_title(
                f"Item {Item_Data['Info']['Numero_Item']}: "
                f"{Item_Data['Info']['Titulo']}\n"
                f"{Item_Data['Info']['Tipo']} - {Tipo_Columna}",
                fontsize=10,
                pad=15
            )
            YLabel = 'Valor'
            if 'Tiempo' in Tipo_Columna:
                YLabel = 'Tiempo de Respuesta'
            elif 'CO_' in Tipo_Columna:
                YLabel = 'Cambio de Opinión'
            Grafico.set_ylabel(YLabel, fontsize=9)

            # Aplicar límites verticales si corresponde.
            if 'CO_' in Tipo_Columna:
                Grafico.set_ylim(-2, 2)
            elif 'IP_Respuesta' in Tipo_Columna:
                Grafico.set_ylim(1, 5)

    for j in range(Num_Items, len(Graficos_Aplanados)):
        Graficos_Aplanados[j].set_visible(False)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.6, wspace=0.3)

    Nombre_Base = (
        f"Boxplots/Boxplots_Items_{Nombre_Df}_"
        f"{Tipo_Columna}_Por_Categoria_PASO"
    )

    Figura.savefig(
        f"{Nombre_Base}.png",
        format='png',
        bbox_inches='tight',
        dpi=300
    )
    Figura.savefig(
        f"{Nombre_Base}.svg",
        format='svg',
        bbox_inches='tight',
        dpi=300
    )
