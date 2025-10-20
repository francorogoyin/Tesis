from typing import Any, Dict, List
import pandas as pd
import re
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def Crear_Variables_De_Orden_IP_Items(df):

    """
    Procesa todo el DataFrame para extraer orden de IP Items y último Item.

    Parámetros:
    - df: DataFrame con la columna 'results' conteniendo JSON.

    Retorna:
    - DataFrame modificado con las nuevas columnas agregadas.

    """

    def Extraer_Datos_JSON(Fila_JSON):
        try:
            # Convertir el string JSON a diccionario de Python.
            Datos_Sujeto = json.loads(Fila_JSON)

            # Extraer el orden de aparición de los IP Items.
            Orden_IP_Items = [
                    int(Clave.split('_')[-1]) for Clave in 
                    Datos_Sujeto['results'][1]['fase_3']['IP'].keys() 
                    if Clave.startswith('IP_item_')
                                ]

            # Obtener el último IP Item de la lista.
            Ultimo_IP_Item = Orden_IP_Items[-1] if Orden_IP_Items else None

            return Orden_IP_Items, Ultimo_IP_Item

        except (KeyError, IndexError, json.JSONDecodeError):
            # En caso de error, retornar valores vacíos.
            return [], None

    # Aplicar la función a todas las filas del DataFrame.
    Resultados_Procesados = df['results'].apply(
        Extraer_Datos_JSON
    )

    # Agregar las nuevas columnas al DataFrame.
    df['Orden_IP_Items'] = [
        Resultado[0] for Resultado in Resultados_Procesados
    ]
    df['Ultimo_IP_Item'] = [
        Resultado[1] for Resultado in Resultados_Procesados
    ]

    return df

def Crear_Variables_De_Orden_IP_Items_Asociados(df):
    
    """
    Procesa todo el DataFrame para extraer orden de IP Items asociados a candidatos y último Item.
    
    Parámetros:
    - df: DataFrame con la columna 'results' conteniendo JSON.
    
    Retorna:
    - DataFrame modificado con las nuevas columnas agregadas.
    
    """
    
    import json
    
    Lista_Orden_IP_Items = []
    Lista_Ultimo_IP_Item = []
    
    for Fila_JSON in df['results']:
        try:
            # Convertir el string JSON a diccionario de Python.
            Datos_Sujeto = json.loads(Fila_JSON)
            
            # Extraer números de IP Items con sufijo _Izq/_Der de la sección "IP_modificada".
            Orden_IP_Items = [
                Clave.split('_')[2] + '_' + Clave.split('_')[3] for Clave in 
                Datos_Sujeto['results'][1]['fase_3']['IP_modificada'].keys() 
                if Clave.startswith('IP_item_') and len(Clave.split('_')) > 3
            ]
            
            # Obtener el último IP Item de la lista.
            Ultimo_IP_Item = Orden_IP_Items[-1] if Orden_IP_Items else None
            
            Lista_Orden_IP_Items.append(Orden_IP_Items)
            Lista_Ultimo_IP_Item.append(Ultimo_IP_Item)
            
        except (KeyError, IndexError, json.JSONDecodeError):
            # En caso de error, agregar valores vacíos.
            Lista_Orden_IP_Items.append([])
            Lista_Ultimo_IP_Item.append(None)
    
    # Agregar las nuevas columnas al DataFrame.
    df['Orden_IP_Items_Asociados'] = Lista_Orden_IP_Items
    df['Ultimo_IP_Item_Asociado'] = Lista_Ultimo_IP_Item
    
    return df

def Crear_Primeros_IP_Items_Asociados(df, n):

    """
    Crea una nueva columna con los primeros N elementos de 'Orden_IP_Items_Asociados'.
    
    Parámetros:
    - df: DataFrame con la columna 'Orden_IP_Items_Asociados'
    - n: Número de primeros elementos a extraer
    
    Retorna:
    - DataFrame modificado con la nueva columna 'Primeros_IP_Items_Asociados'

    """
    
    # Crear la nueva columna tomando los primeros n elementos de cada lista
    df['Primeros_IP_Items_Asociados'] = df['Orden_IP_Items_Asociados'].apply(
        lambda lista: lista[:n] if isinstance(lista, list) and len(lista) >= n else lista
    )
    
    return df

def Aplanar_Diccionario(Diccionario, Prefijo = ''):
    
    """
    Convierte un diccionario anidado en uno plano,
    usando puntos para separar los niveles de anidamiento.
    
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
            # Convertir listas a strings separados por comas.
            Diccionario_Plano[Nueva_Clave] = ', '.join(map(str, Valor))
        else:
            Diccionario_Plano[Nueva_Clave] = Valor
    
    return Diccionario_Plano

def Procesar_Columna_Results(df):
    
    """
    Extrae y procesa la columna 'results' de un DataFrame,
    convirtiendo el contenido JSON en un DataFrame de pandas.
    Maneja valores NaN y datos faltantes.
    
    """
    
    # Extraer solo la columna 'results'.
    Columna_Results = df['results']
    
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
            
            # Agregar identificadores para mantener la trazabilidad.
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

def Rellenar_IP_Items_Asociados_Faltantes(df):
   
   """
   Rellena los valores faltantes en columnas IP_Item_X_Izq/Der cuando 
   uno tiene valor y el otro es NaN, usando la mediana por categoria.
   
   """
   
   # Obtener todos los numeros de IP_Items unicos.
   Numeros_IP = set()
   for Columna in df.columns:
       if 'IP_Item_' in Columna and ('_Izq_' in Columna or '_Der_' in Columna):
           # Extraer numero del Item (ej: de IP_Item_5_Izq_Respuesta -> 5).
           Partes = Columna.split('_')
           if len(Partes) >= 3:
               Numero = Partes[2]
               Numeros_IP.add(Numero)
   
   #print(f"  IP_Items encontrados: {sorted(Numeros_IP)}")
   
   Total_Rellenos = 0
   
   # Para cada numero de IP_Item, procesar Respuesta y Tiempo.
   for Numero in sorted(Numeros_IP):
       for Tipo in ['Respuesta', 'Tiempo']:
           Col_Izq = f'IP_Item_{Numero}_Izq_{Tipo}'
           Col_Der = f'IP_Item_{Numero}_Der_{Tipo}'
           
           # Verificar que ambas columnas existen.
           if Col_Izq in df.columns and Col_Der in df.columns:
               
               # Contar datos iniciales.
               Datos_Iniciales_Izq = df[Col_Izq].notna().sum()
               Datos_Iniciales_Der = df[Col_Der].notna().sum()
               
               # Convertir a numerico si es necesario.
               df[Col_Izq] = pd.to_numeric(df[Col_Izq], errors='coerce')
               df[Col_Der] = pd.to_numeric(df[Col_Der], errors='coerce')
               
               # Encontrar filas donde uno tiene valor y otro es NaN.
               Mask_Izq_Lleno_Der_Vacio = (
                   df[Col_Izq].notna() & df[Col_Der].isna()
               )
               Mask_Der_Lleno_Izq_Vacio = (
                   df[Col_Der].notna() & df[Col_Izq].isna()
               )
               
               Casos_Izq_Der = Mask_Izq_Lleno_Der_Vacio.sum()
               Casos_Der_Izq = Mask_Der_Lleno_Izq_Vacio.sum()
               
               #if Casos_Izq_Der > 0 or Casos_Der_Izq > 0:
                #    print(f"    {Col_Izq}/{Col_Der}:")
                #    print(f"      - Datos iniciales: Izq={Datos_Iniciales_Izq}, "
                #          f"Der={Datos_Iniciales_Der}")
                #    print(f"      - Casos Izq→Der: {Casos_Izq_Der}")
                #    print(f"      - Casos Der→Izq: {Casos_Der_Izq}")
               
               # Calcular medianas por categoria para cada columna.
               Medianas_Izq = df.groupby('Categoria_PASO_2023')[Col_Izq].median()
               Medianas_Der = df.groupby('Categoria_PASO_2023')[Col_Der].median()
               
               # Mostrar las medianas calculadas si hay casos para rellenar.
            #    if Casos_Izq_Der > 0:
            #        print(f"      - Medianas para {Col_Der}: "
            #              f"{Medianas_Der.to_dict()}")
               
            #    if Casos_Der_Izq > 0:
            #        print(f"      - Medianas para {Col_Izq}: "
            #              f"{Medianas_Izq.to_dict()}")
               
               # Rellenar valores faltantes en Der cuando Izq tiene valor.
               Rellenos_Der = 0
               for Indice in df[Mask_Izq_Lleno_Der_Vacio].index:
                   Categoria = df.loc[Indice, 'Categoria_PASO_2023']
                   Valor_Izq = df.loc[Indice, Col_Izq]
                   Id_Participante = df.loc[Indice, 'ID']
                   
                   if (Categoria in Medianas_Der.index and 
                       pd.notna(Medianas_Der[Categoria])):
                       Valor_Mediana = Medianas_Der[Categoria]
                       df.loc[Indice, Col_Der] = Valor_Mediana
                       Rellenos_Der += 1
                    #    if Rellenos_Der <= 3:  # Mostrar primeros 3 casos.
                    #        print(f"        ID={Id_Participante}, "
                    #              f"Categoría={Categoria}, "
                    #              f"Izq={Valor_Izq} → Der={Valor_Mediana}")
               
               # Rellenar valores faltantes en Izq cuando Der tiene valor.
               Rellenos_Izq = 0
               for Indice in df[Mask_Der_Lleno_Izq_Vacio].index:
                   Categoria = df.loc[Indice, 'Categoria_PASO_2023']
                   Valor_Der = df.loc[Indice, Col_Der]
                   Id_Participante = df.loc[Indice, 'ID']
                   
                   if (Categoria in Medianas_Izq.index and 
                       pd.notna(Medianas_Izq[Categoria])):
                       Valor_Mediana = Medianas_Izq[Categoria]
                       df.loc[Indice, Col_Izq] = Valor_Mediana
                       Rellenos_Izq += 1
                      # if Rellenos_Izq <= 3:  # Mostrar primeros 3 casos.
                        #    print(f"        ID={Id_Participante}, "
                        #          f"Categoría={Categoria}, "
                        #          f"Der={Valor_Der} → Izq={Valor_Mediana}")
               
               # Contar datos finales.
               Datos_Finales_Izq = df[Col_Izq].notna().sum()
               Datos_Finales_Der = df[Col_Der].notna().sum()
               
               Total_Rellenos += Rellenos_Der + Rellenos_Izq               
              # if Casos_Izq_Der > 0 or Casos_Der_Izq > 0:
    #                    print(f"      - Rellenos realizados: Der={Rellenos_Der}, "
    #                          f"Izq={Rellenos_Izq}")
    #                    print(f"      - Datos finales: Izq={Datos_Finales_Izq}, "
    #                          f"Der={Datos_Finales_Der}")
    #                    print()
    
    #    print(f"  Total de rellenos realizados: {Total_Rellenos}")

def Eliminar_Primeros_Datos_IP_Items_Asociados(df):

    """
    Elimina los datos (no las columnas) de IP Items basándose en 'Orden_IP_Items_Asociados'.
    Toma los primeros números únicos necesarios para obtener exactamente 3 números diferentes.
    Para cada IP Item, elimina tanto la versión _Izq como _Der.
    
    Parámetros:
    - df: DataFrame con columnas 'Orden_IP_Items_Asociados' y columnas IP_Item_X_Y_Z
    
    Retorna:
    - DataFrame modificado con los datos eliminados (Valores = NaN)
    
    """
    
    import pandas as pd
    
    # Crear una copia del DataFrame para no modificar el original.
    df_Modificado = df.copy()
    
    # Sufijos de columnas a eliminar.
    Sufijos = ['_Respuesta', '_Candidato', '_Tiempo']
    
    # Iterar por cada fila del DataFrame.
    for Index, Fila in df_Modificado.iterrows():
        
        # Obtener la lista de orden de IP Items para esta fila.
        Orden_IP_Items = Fila['Orden_IP_Items_Asociados']
        
        # Si la lista no está vacía o no es NaN.
        if isinstance(Orden_IP_Items, list) and len(Orden_IP_Items) > 0:
            
            # Estrategia: Tomar ítems hasta obtener 3 números únicos.
            Numeros_IP_Unicos = set()
            Items_A_Procesar = []
            
            # Recorrer la lista de orden hasta obtener 3 números únicos.
            for Item in Orden_IP_Items:
                if isinstance(Item, str) and '_' in Item:
                    Numero = Item.split('_')[0]  # Extraer solo el número.
                    
                    # Agregar el ítem a procesar.
                    Items_A_Procesar.append(Item)
                    Numeros_IP_Unicos.add(Numero)
                    
                    # Parar cuando tengamos 3 números únicos.
                    if len(Numeros_IP_Unicos) >= 3:
                        break
            
            # Eliminar datos para los 3 números únicos encontrados.
            for Numero in Numeros_IP_Unicos:
                for Direccion in ['_Izq', '_Der']:
                    for Sufijo in Sufijos:
                        # Construir el nombre de la columna.
                        Columna = f'IP_Item_{Numero}{Direccion}{Sufijo}'
                        
                        # Si la columna existe en el DataFrame, eliminar el dato.
                        if Columna in df_Modificado.columns:
                            df_Modificado.at[Index, Columna] = pd.NA
    
    return df_Modificado

def Eliminar_Filas_Por_Desviacion_Estandar(
    Data_Frame: pd.DataFrame,
    Columnas_Tiempo: List[str],
    Numero_Desviaciones: int = 3
) -> pd.DataFrame:

    """
    
    Elimina filas donde algún valor de tiempo exceda el número
    especificado de desvíos estándar desde la media global de todas
    las columnas de tiempo.
    
    Parámetros:
    - Data_Frame: DataFrame a procesar.
    - Columnas_Tiempo: Lista de nombres de columnas a analizar.
    - Numero_Desviaciones: Número de desvíos estándar como límite
      (por defecto 3).
    
    Retorna:
    - DataFrame con las filas válidas únicamente.
    
    """

    # Filtrar columnas que existen en el DataFrame.
    Columnas_Existentes: List[str] = [
        Columna for Columna in Columnas_Tiempo
        if Columna in Data_Frame.columns
    ]
    if len(Columnas_Existentes) == 0:
        print("⚠️ Ninguna columna de tiempo encontrada;")
        print("   regresando el DataFrame sin cambios.")
        return Data_Frame

    # Recopilar todos los valores numéricos no nulos.
    Todos_Los_Valores: List[float] = []
    for Columna in Columnas_Existentes:
        Valores_Limpios = pd.to_numeric(
            Data_Frame[Columna],
            errors = 'coerce'
        ).dropna().tolist()
        Todos_Los_Valores.extend(Valores_Limpios)

    if len(Todos_Los_Valores) == 0:
        print("⚠️ No hay valores numéricos para calcular estadísticos;")
        print("   regresando el DataFrame sin cambios.")
        return Data_Frame

    # Calcular estadísticos globales.
    Media_Global: float = sum(Todos_Los_Valores) / len(Todos_Los_Valores)
    Varianza: float = sum(
        (Valor - Media_Global) ** 2 for Valor in Todos_Los_Valores
    ) / len(Todos_Los_Valores)
    Desviacion_Estandar_Global: float = Varianza ** 0.5
    Limite_Superior: float = Media_Global + (
        Numero_Desviaciones * Desviacion_Estandar_Global
    )

    print(f"Media global: {Media_Global:.2f}")
    print(f"Desvío estándar global: {Desviacion_Estandar_Global:.2f}")
    print(
        f"Límite superior ({Numero_Desviaciones} desvíos): "
        f"{Limite_Superior:.2f}"
    )

    # Detectar y eliminar filas con al menos un valor atípico.
    Filas_Validas: List[int] = []
    for Indice, Fila in Data_Frame.iterrows():
        Fila_Valida = True
        for Columna in Columnas_Existentes:
            Valor = pd.to_numeric(Fila[Columna], errors = 'coerce')
            # Ensure Valor is a scalar, not a Series
            if isinstance(Valor, pd.Series):
                if not Valor.empty:
                    Valor = Valor.iloc[0]
                else:
                    continue
            if pd.notna(Valor) and Valor > Limite_Superior:
                print(
                    f"Eliminando fila ID={Fila.get('ID', Indice)}: "
                    f"{Columna}={Valor:.2f} supera {Limite_Superior:.2f}"
                )
                Fila_Valida = False
                break
        if Fila_Valida:
            Filas_Validas.append(Indice) # type: ignore

    Data_Frame_Resultante = Data_Frame.loc[Filas_Validas]

    return Data_Frame_Resultante

def Crear_Columnas_Cambio_Opinion(Diccionario_Dataframes):

    """
    Crea columnas de cambio de opinión para cada ítem IP comparando 
    las respuestas con candidatos de izquierda/derecha versus las 
    respuestas base de cada ítem.
    
    """

    # Lista de números de ítems IP disponibles.
    Items_IP = [3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 19, 20, 22, 23, 24, 
                25, 27, 28, 29, 30]
    
    for Nombre_Df, Dataframe in Diccionario_Dataframes.items():
        
        for Numero_Item in Items_IP:
            
            # Nombres de las columnas base y con candidatos.
            Columna_Base = f'IP_Item_{Numero_Item}_Respuesta'
            Columna_Izq = f'IP_Item_{Numero_Item}_Izq_Respuesta'
            Columna_Der = f'IP_Item_{Numero_Item}_Der_Respuesta'
            
            # Nombres de las nuevas columnas de cambio de opinión.
            Nueva_Columna_Izq = f'CO_Item_{Numero_Item}_Izq'
            Nueva_Columna_Der = f'CO_Item_{Numero_Item}_Der'
            
            # Verificar que todas las columnas necesarias existen.
            if all(Columna in Dataframe.columns for Columna in 
                   [Columna_Base, Columna_Izq, Columna_Der]):
                
                # Convertir a numérico manteniendo NaN para valores inválidos.
                Base_Numerica = pd.to_numeric(Dataframe[Columna_Base], 
                                            errors='coerce')
                Izq_Numerica = pd.to_numeric(Dataframe[Columna_Izq], 
                                           errors='coerce')
                Der_Numerica = pd.to_numeric(Dataframe[Columna_Der], 
                                           errors='coerce')
                
                # Calcular cambio de opinión para izquierda.
                Dataframe[Nueva_Columna_Izq] = Izq_Numerica - Base_Numerica
                
                # Calcular cambio de opinión para derecha.
                Dataframe[Nueva_Columna_Der] = Der_Numerica - Base_Numerica
    
    return Diccionario_Dataframes

def Crear_Columnas_Cambio_Tiempo(Diccionario_Dataframes):

   """
   Crea columnas de cambio de tiempo para cada ítem IP comparando 
   los tiempos de respuesta con candidatos de izquierda/derecha versus 
   los tiempos base de cada ítem.
   
   """

   # Lista de números de ítems IP disponibles.
   Items_IP = [3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 19, 20, 22, 23, 24, 
               25, 27, 28, 29, 30]
   
   for Nombre_Df, Dataframe in Diccionario_Dataframes.items():
       
       for Numero_Item in Items_IP:
           
           # Nombres de las columnas base y con candidatos para tiempo.
           Columna_Base = f'IP_Item_{Numero_Item}_Tiempo'
           Columna_Izq = f'IP_Item_{Numero_Item}_Izq_Tiempo'
           Columna_Der = f'IP_Item_{Numero_Item}_Der_Tiempo'
           
           # Nombres de las nuevas columnas de cambio de tiempo.
           Nueva_Columna_Izq = f'CT_Item_{Numero_Item}_Izq'
           Nueva_Columna_Der = f'CT_Item_{Numero_Item}_Der'
           
           # Verificar que todas las columnas necesarias existen.
           if all(Columna in Dataframe.columns for Columna in 
                  [Columna_Base, Columna_Izq, Columna_Der]):
               
               # Convertir a numérico manteniendo NaN para valores inválidos.
               Base_Numerica = pd.to_numeric(Dataframe[Columna_Base], 
                                           errors='coerce')
               Izq_Numerica = pd.to_numeric(Dataframe[Columna_Izq], 
                                          errors='coerce')
               Der_Numerica = pd.to_numeric(Dataframe[Columna_Der], 
                                          errors='coerce')
               
               # Calcular cambio de tiempo para izquierda.
               Dataframe[Nueva_Columna_Izq] = Izq_Numerica - Base_Numerica
               
               # Calcular cambio de tiempo para derecha.
               Dataframe[Nueva_Columna_Der] = Der_Numerica - Base_Numerica
   
   return Diccionario_Dataframes

def Limpiar_Texto(texto):
   
   """
   Limpia el texto removiendo guiones bajos y capitalizando solo la primera letra.
   
   """

   return texto.replace('_', ' ').capitalize()

def Crear_Boxplots_Items(
    Data_Frame: pd.DataFrame,
    Diccionario_Items: dict[int, dict[str, Any]],
    Tipo_Columna: str = 'IP_Respuesta',
    Nombre_Df: str = 'df'
) -> None:

    """
    
    Crea boxplots para cada ítem segmentado por categoría PASO 2023,
    incluyendo IP, CO y CT. Guarda cada gráfico en formatos PNG y SVG
    en la carpeta 'Boxplots/'. Aplica límites verticales según tipo de
    columna y usa colores específicos por categoría.

    Parámetros:
    - Data_Frame: DataFrame sobre el que graficar.
    - Diccionario_Items: metadata de cada ítem (número, título, tipo).
    - Tipo_Columna: uno de:
        'IP_Respuesta',
        'IP_Izq_Respuesta','IP_Der_Respuesta',
        'IP_Tiempo','IP_Izq_Tiempo','IP_Der_Tiempo',
        'CO_Pro_Izq','CO_Con_Izq','CO_Pro_Der','CO_Con_Der',
        'CT_Pro_Izq','CT_Con_Izq','CT_Pro_Der','CT_Con_Der'
    - Nombre_Df: nombre para los archivos de salida.

    """

    import os
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

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
            Nombre_Columna = f'IP_Item_{Numero_Item}_Izq_Respuesta'
        elif Tipo_Columna == 'IP_Der_Respuesta':
            Nombre_Columna = f'IP_Item_{Numero_Item}_Der_Respuesta'
        elif Tipo_Columna == 'IP_Tiempo':
            Nombre_Columna = f'IP_Item_{Numero_Item}_Tiempo'
        elif Tipo_Columna == 'IP_Izq_Tiempo':
            Nombre_Columna = f'IP_Item_{Numero_Item}_Izq_Tiempo'
        elif Tipo_Columna == 'IP_Der_Tiempo':
            Nombre_Columna = f'IP_Item_{Numero_Item}_Der_Tiempo'
        elif Tipo_Columna == 'CO_Pro_Izq':
            Nombre_Columna = f'CO_Item_{Numero_Item}_Izq'
        elif Tipo_Columna == 'CO_Con_Izq':
            Nombre_Columna = f'CO_Item_{Numero_Item}_Izq'
        elif Tipo_Columna == 'CO_Pro_Der':
            Nombre_Columna = f'CO_Item_{Numero_Item}_Der'
        elif Tipo_Columna == 'CO_Con_Der':
            Nombre_Columna = f'CO_Item_{Numero_Item}_Der'
        elif Tipo_Columna == 'CT_Pro_Izq':
            Nombre_Columna = f'CT_Item_{Numero_Item}_Izq'
        elif Tipo_Columna == 'CT_Con_Izq':
            Nombre_Columna = f'CT_Item_{Numero_Item}_Izq'
        elif Tipo_Columna == 'CT_Pro_Der':
            Nombre_Columna = f'CT_Item_{Numero_Item}_Der'
        elif Tipo_Columna == 'CT_Con_Der':
            Nombre_Columna = f'CT_Item_{Numero_Item}_Der'
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
        Filas, Columnas,
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
        Datos = Datos[~Datos['Categoria_PASO_2023'].
            isin(['No apply','No response','Other'])]

        if Datos.empty:
            Grafico.text(
                0.5, 0.5, 'Sin datos válidos',
                ha='center', va='center',
                transform=Grafico.transAxes
            )
        else:
            Orden_Categorias = [
                'Left_Wing','Progressivism','Centre',
                'Moderate_Right_A','Moderate_Right_B',
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
                Subdatos = Datos[Datos['Categoria_PASO_2023'] == Categoria][Columna]
                if not Subdatos.empty:
                    Media = Subdatos.mean()
                    if abs(Media) < 1:
                        Etiqueta = f"{Categoria.replace('_', ' ')}\n({Media:.3f})"
                    else:
                        Etiqueta = f"{Categoria.replace('_', ' ')}\n({Media:.2f})"
                else:
                    Etiqueta = Categoria.replace('_', ' ') + "\n(N/A)"
                Etiquetas_Categorias.append(Etiqueta)

            Grafico.set_xticklabels(Etiquetas_Categorias, rotation=45, ha='right')
            Grafico.set_title(
                f"Item {Item_Data['Info']['Numero_Item']}: "
                f"{Item_Data['Info']['Titulo']}\n"
                f"{Item_Data['Info']['Tipo']} - {Tipo_Columna}",
                fontsize=10, pad=15
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
        f"{Nombre_Base}.png", format='png',
        bbox_inches='tight', dpi=300
    )
    Figura.savefig(
        f"{Nombre_Base}.svg", format='svg',
        bbox_inches='tight', dpi=300
    )

def Obtener_Nombre_Archivo() -> str:

   """
   Obtiene automáticamente el nombre del archivo notebook actual.
   
   Intenta varios métodos para determinar el nombre del notebook
   de Jupyter en ejecución. Si no puede determinarlo automáticamente,
   solicita al usuario que lo introduzca manualmente.
   
   Returns:
       str: El nombre del notebook sin la extensión .ipynb
   
   """

   import os
   import json
   import ipykernel

   try:
       # Obtiene el archivo de conexión del kernel actual.
       Archivo_Conexion: str = ipykernel.get_connection_file()
       
       # Extrae el ID del kernel del nombre del archivo de conexión.
       Kernel_Id: str = (os.path.basename(Archivo_Conexion)
                        .split('-')[1]
                        .split('.')[0])
       
       # Busca el nombre en las variables de entorno de Jupyter.
       Nombre_Notebook: str = os.environ.get('JPY_SESSION_NAME', 
                                            'Desconocido')
       
       if Nombre_Notebook == 'Desconocido':
           # Intenta obtener desde el directorio de trabajo actual.
           Ruta_Trabajo: str = os.getcwd()
           Archivos_Notebook: list[str] = [archivo for archivo in 
                                         os.listdir(Ruta_Trabajo) 
                                         if archivo.endswith('.ipynb')]
           
           if Archivos_Notebook:
               # Toma el primer notebook encontrado en el directorio.
               Nombre_Notebook = Archivos_Notebook[0]
           else:
               Nombre_Notebook = "notebook_actual"
       
       return os.path.splitext(Nombre_Notebook)[0]
       
   except Exception as Error:
       print("No se pudo determinar automáticamente el nombre.")
       print(f"Error: {Error}")
       # Solicita al usuario que introduzca el nombre manualmente.
       Nombre_Notebook_Input: str = input("Introduce el nombre del notebook: ")
       return os.path.splitext(Nombre_Notebook_Input)[0]

