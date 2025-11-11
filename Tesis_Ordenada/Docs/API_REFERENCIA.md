# API REFERENCIA - Funciones y Módulos

Este documento contiene la referencia completa de todas las funciones públicas del proyecto, organizadas por módulo.

---

## ÍNDICE

1. [Módulos de Procesamiento](#módulos-de-procesamiento)
2. [Módulos de Análisis Estadístico](#módulos-de-análisis-estadístico)
3. [Módulos de Modelado](#módulos-de-modelado)
4. [Módulos de Visualización](#módulos-de-visualización)
5. [Módulos de Utilidades](#módulos-de-utilidades)
6. [Sistema de Control](#sistema-de-control)

---

## MÓDULOS DE PROCESAMIENTO

### Construccion_Bases.py

**Ubicación**: `Codigo/Procesamiento/Construccion_Bases.py`

**Propósito**: Construcción y combinación de bases de datos desde CSVs crudos.

#### `Combinar_Archivos_Generales() -> pd.DataFrame`

Combina los 5 archivos CSV de Generales en un único DataFrame.

**Retorna**: DataFrame con ~2786 filas.

**Ejemplo**:
```python
from Construccion_Bases import Combinar_Archivos_Generales

Df_Generales = Combinar_Archivos_Generales()
```

---

#### `Combinar_Archivos_Ballotage() -> pd.DataFrame`

Combina los 2 archivos CSV de Ballotage en un único DataFrame.

**Retorna**: DataFrame con ~1254 filas.

**Ejemplo**:
```python
from Construccion_Bases import Combinar_Archivos_Ballotage

Df_Ballotage = Combinar_Archivos_Ballotage()
```

---

#### `Procesar_Base_Completa(Df: pd.DataFrame) -> pd.DataFrame`

Procesa DataFrame crudo: expande columna JSON, rellena items faltantes, crea variables de orden.

**Parámetros**:
- `Df`: DataFrame crudo con columna JSON.

**Retorna**: DataFrame con columnas expandidas (60 columnas por 20 items).

**Ejemplo**:
```python
from Construccion_Bases import Procesar_Base_Completa

Df = Procesar_Base_Completa(Df_Crudo)
```

---

### Calculo_Indices.py

**Ubicación**: `Codigo/Procesamiento/Calculo_Indices.py`

**Propósito**: Cálculo de índices ideológicos (Progresismo, Conservadurismo, Positividad).

#### `Calcular_Indice_Progresismo(Df: pd.DataFrame) -> pd.Series`

Calcula índice de progresismo como promedio de items progresistas.

**Parámetros**:
- `Df`: DataFrame con columnas `IP_Item_N_Respuesta`.

**Retorna**: Serie con índice de progresismo (rango 1-5).

**Items Progresistas**: 3, 4, 5, 6, 7, 9, 10, 16, 22, 24.

---

#### `Calcular_Indice_Conservadurismo(Df: pd.DataFrame) -> pd.Series`

Calcula índice de conservadurismo como promedio de items conservadores.

**Parámetros**:
- `Df`: DataFrame con columnas `IP_Item_N_Respuesta`.

**Retorna**: Serie con índice de conservadurismo (rango 1-5).

**Items Conservadores**: 8, 11, 19, 20, 23, 25, 27, 28, 29, 30.

---

#### `Calcular_Indice_Positividad(Df: pd.DataFrame) -> pd.Series`

Calcula índice de positividad como promedio de TODOS los items.

**Retorna**: Serie con índice de positividad (rango 1-5).

---

#### `Calcular_Todos_Indices(Df: pd.DataFrame) -> pd.DataFrame`

Calcula todos los índices (Progresismo, Conservadurismo, Positividad, Tiempos) y los agrega al DataFrame.

**Parámetros**:
- `Df`: DataFrame con columnas IP_Item.

**Retorna**: DataFrame con 5 columnas adicionales de índices.

**Ejemplo**:
```python
from Calculo_Indices import Calcular_Todos_Indices

Df = Calcular_Todos_Indices(Df)
# Agrega: Indice_Progresismo, Indice_Conservadurismo,
#         Indice_Positividad, Indice_Progresismo_Tiempo,
#         Indice_Conservadurismo_Tiempo
```

---

### Calculo_Variables_Cambio.py

**Ubicación**: `Codigo/Procesamiento/Calculo_Variables_Cambio.py`

**Propósito**: Creación de variables CO (Cambio de Opinión) y CT (Cambio de Tiempo).

#### `Calcular_Variables_Cambio(Diccionario_Dfs: Dict[str, pd.DataFrame], Incluir_Congruencia: bool = False) -> Dict[str, pd.DataFrame]`

Calcula variables CO y CT para todos los items y direcciones.

**Parámetros**:
- `Diccionario_Dfs`: Diccionario con claves 'Generales' y 'Ballotage', valores DataFrames.
- `Incluir_Congruencia`: Si True, calcula también CO_Congruentes/Incongruentes.

**Retorna**: Diccionario con DataFrames actualizados (80 columnas adicionales por DataFrame).

**Ejemplo**:
```python
from Calculo_Variables_Cambio import Calcular_Variables_Cambio

Diccionario_Dfs = {
    'Generales': Df_Generales,
    'Ballotage': Df_Ballotage
}

Diccionario_Dfs = Calcular_Variables_Cambio(
    Diccionario_Dfs,
    Incluir_Congruencia=True
)

Df_Generales = Diccionario_Dfs['Generales']
Df_Ballotage = Diccionario_Dfs['Ballotage']
```

---

#### `Calcular_CO_Congruentes_E_Incongruentes(Df: pd.DataFrame, Nombre_Eleccion: str) -> pd.DataFrame`

Calcula promedios de variables CO congruentes e incongruentes con ideología participante.

**Parámetros**:
- `Df`: DataFrame con variables CO y categoría ideológica.
- `Nombre_Eleccion`: 'Generales' o 'Ballotage'.

**Retorna**: DataFrame con columnas `CO_Congruentes_Promedio` y `CO_Incongruentes_Promedio`.

**Clasificación**:
- **Congruente**: Progresista→Izquierda, Conservador→Derecha.
- **Incongruente**: Progresista→Derecha, Conservador→Izquierda.

---

### Limpieza_Datos.py

**Ubicación**: `Codigo/Procesamiento/Limpieza_Datos.py`

**Propósito**: Filtrado de categorías inválidas y outliers de tiempo.

#### `Filtrar_Categorias_Invalidas(Df: pd.DataFrame) -> pd.DataFrame`

Elimina participantes con categorías problemáticas ('Other', 'No apply', 'No response', 'Blank').

**Parámetros**:
- `Df`: DataFrame con columna `Categoria_PASO_2023`.

**Retorna**: DataFrame filtrado.

---

#### `Filtrar_Outliers_Por_Tiempo(Df: pd.DataFrame, Numero_Desviaciones: int = 3) -> pd.DataFrame`

Elimina participantes con tiempos de respuesta extremos.

**Parámetros**:
- `Df`: DataFrame con columnas de tiempo.
- `Numero_Desviaciones`: Umbral de desviaciones estándar (default: 3).

**Retorna**: DataFrame sin outliers de tiempo.

**Criterio**: Elimina fila si CUALQUIER tiempo > Media + (N × Desv).

---

#### `Limpiar_Datos_Completo(Df: pd.DataFrame, Filtrar_Categorias: bool = True, Filtrar_Tiempos: bool = True, Numero_Desviaciones: int = 3) -> pd.DataFrame`

Aplica TODOS los filtros de limpieza en secuencia.

**Parámetros**:
- `Df`: DataFrame a limpiar.
- `Filtrar_Categorias`: Si True, elimina categorías inválidas.
- `Filtrar_Tiempos`: Si True, elimina outliers de tiempo.
- `Numero_Desviaciones`: Umbral para outliers (default: 3).

**Retorna**: DataFrame limpio.

**Ejemplo**:
```python
from Limpieza_Datos import Limpiar_Datos_Completo

Df_Limpio = Limpiar_Datos_Completo(
    Df,
    Filtrar_Categorias=True,
    Filtrar_Tiempos=True,
    Numero_Desviaciones=3
)
```

---

### Relleno_Medianas.py

**Ubicación**: `Codigo/Procesamiento/Relleno_Medianas.py`

**Propósito**: Relleno de valores faltantes con medianas por categoría ideológica.

#### `Rellenar_Con_Medianas_Por_Categoria(Df: pd.DataFrame, Columna_Categoria: str = 'Categoria_PASO_2023') -> pd.DataFrame`

Rellena valores faltantes en variables CO/CT con medianas calculadas por categoría ideológica.

**Parámetros**:
- `Df`: DataFrame con variables CO/CT y columna de categoría.
- `Columna_Categoria`: Nombre de columna para agrupar (default: 'Categoria_PASO_2023').

**Retorna**: DataFrame con NaN rellenados y columnas `_Original` como backup.

**Ejemplo**:
```python
from Relleno_Medianas import Rellenar_Con_Medianas_Por_Categoria

Df = Rellenar_Con_Medianas_Por_Categoria(
    Df,
    Columna_Categoria='Categoria_PASO_2023'
)
```

---

### Procesar_Redes_Y_Medios.py

**Ubicación**: `Codigo/Procesamiento/Procesar_Redes_Y_Medios.py`

**Propósito**: Conversión de columnas de texto con múltiples valores en columnas binarias.

#### `Procesar_Redes_Sociales(Df: pd.DataFrame) -> pd.DataFrame`

Crea columnas binarias (0/1) para cada red social mencionada.

**Parámetros**:
- `Df`: DataFrame con columna `Red_Social` (texto separado por comas).

**Retorna**: DataFrame con columnas adicionales `Red_Social_Twitter`, `Red_Social_Facebook`, etc.

**Redes Procesadas**: Twitter, Facebook, Instagram, Threads, Tiktok, Youtube, Whatsapp, Telegram.

---

#### `Procesar_Medios_Prensa(Df: pd.DataFrame) -> pd.DataFrame`

Crea columnas binarias (0/1) para cada medio de prensa mencionado.

**Parámetros**:
- `Df`: DataFrame con columna `Medios_Prensa` (texto separado por comas).

**Retorna**: DataFrame con columnas adicionales `Medios_Prensa_Clarin`, `Medios_Prensa_La_Nacion`, etc.

**Medios Procesados**: 13 medios de prensa argentinos.

---

### Agrupamiento_Variables.py

**Ubicación**: `Codigo/Procesamiento/Agrupamiento_Variables.py`

**Propósito**: Creación de versiones agrupadas de variables categóricas.

#### `Agrupar_Edad(Serie_Edad: pd.Series) -> pd.Series`

Agrupa edades en rangos.

**Parámetros**:
- `Serie_Edad`: Serie con edades numéricas.

**Retorna**: Serie con categorías ('18-25', '26-35', '36-45', '46-55', '56-65', '66+').

---

#### `Mapear_Provincia_A_Region(Serie_Provincia: pd.Series) -> pd.Series`

Mapea provincias argentinas a regiones geográficas.

**Parámetros**:
- `Serie_Provincia`: Serie con nombres de provincias.

**Retorna**: Serie con regiones (NOA, NEA, Centro, Cuyo, Patagonia, AMBA).

---

#### `Agrupar_Nivel_Educativo(Serie_Nivel: pd.Series) -> pd.Series`

Agrupa niveles educativos en categorías simplificadas.

**Retorna**: Serie con categorías (Primario, Secundario, Terciario, Universitario, Posgrado).

---

### Crear_Variables_Dummy.py

**Ubicación**: `Codigo/Procesamiento/Crear_Variables_Dummy.py`

**Propósito**: Creación de variables dummy para modelado estadístico.

#### `Crear_Todas_Variables_Dummy(Df: pd.DataFrame) -> pd.DataFrame`

Crea variables dummy para todas las categóricas relevantes.

**Parámetros**:
- `Df`: DataFrame con variables categóricas.

**Retorna**: DataFrame con columnas dummy adicionales (~30 columnas).

**Variables Procesadas**:
- Sexo
- Nivel_Educativo
- Region
- Edad_Agrupada
- Categoria_PASO_2023

**Criterio**: Se crean n-1 dummies para evitar multicolinealidad.

**Ejemplo**:
```python
from Crear_Variables_Dummy import Crear_Todas_Variables_Dummy

Df = Crear_Todas_Variables_Dummy(Df)
# Agrega: Sexo_Masculino, Sexo_Femenino,
#         Nivel_Educativo_Primario, etc.
```

---

### Ordenamiento_Columnas.py

**Ubicación**: `Codigo/Procesamiento/Ordenamiento_Columnas.py`

**Propósito**: Organización de columnas en orden temático.

#### `Ordenar_Columnas_Por_Tematica(Df: pd.DataFrame) -> pd.DataFrame`

Ordena columnas del DataFrame en grupos temáticos.

**Orden**:
1. ID (primera columna)
2. Demográficas
3. Índices
4. Variables CO
5. Variables CT
6. Redes sociales
7. Medios de prensa
8. Variables dummy

**Ejemplo**:
```python
from Ordenamiento_Columnas import Ordenar_Columnas_Por_Tematica

Df = Ordenar_Columnas_Por_Tematica(Df)
```

---

### Agregar_Clusters.py

**Ubicación**: `Codigo/Procesamiento/Agregar_Clusters.py`

**Propósito**: Incorporación de resultados de clustering a la base final.

#### `Agregar_Clusters_A_Base(Df: pd.DataFrame, Ruta_Clusters: str) -> pd.DataFrame`

Carga resultados de clustering y los agrega al DataFrame principal.

**Parámetros**:
- `Df`: DataFrame principal.
- `Ruta_Clusters`: Ruta a directorio con archivos de clusters.

**Retorna**: DataFrame con columnas adicionales de cluster (Cluster_Kmeans, Cluster_Jerarquico, Cluster_DBSCAN).

**Ejemplo**:
```python
from Agregar_Clusters import Agregar_Clusters_A_Base

Df = Agregar_Clusters_A_Base(
    Df,
    Ruta_Clusters='Data/Resultados_Clustering/'
)
```

---

### Ejecutar_Pipeline_Completo.py

**Ubicación**: `Codigo/Procesamiento/Ejecutar_Pipeline_Completo.py`

**Propósito**: Ejecución automatizada del pipeline completo de preprocesamiento.

#### `Ejecutar_Pipeline_Preprocesamiento(Guardar_Intermedios: bool = False, Verbose: bool = True) -> Dict[str, pd.DataFrame]`

Ejecuta los 11 pasos de preprocesamiento secuencialmente.

**Parámetros**:
- `Guardar_Intermedios`: Si True, guarda bases intermedias en cada paso.
- `Verbose`: Si True, muestra mensajes de progreso detallados.

**Retorna**: Diccionario con claves 'Generales' y 'Ballotage', valores DataFrames procesados.

**Ejemplo**:
```python
from Ejecutar_Pipeline_Completo import (
    Ejecutar_Pipeline_Preprocesamiento
)

Diccionario_Dfs = Ejecutar_Pipeline_Preprocesamiento(
    Guardar_Intermedios=False,
    Verbose=True
)

Df_Generales = Diccionario_Dfs['Generales']
Df_Ballotage = Diccionario_Dfs['Ballotage']
```

---

## MÓDULOS DE ANÁLISIS ESTADÍSTICO

### Mann_Whitney.py

**Ubicación**: `Codigo/Test_Estadisticos/Mann_Whitney.py`

**Propósito**: Tests de Mann-Whitney U para comparaciones no paramétricas.

#### `Ejecutar_Mann_Whitney(Df: pd.DataFrame, Variable: str, Grupos_A: List[str], Grupos_B: List[str]) -> Dict`

Ejecuta test U de Mann-Whitney comparando dos grupos.

**Parámetros**:
- `Df`: DataFrame con datos.
- `Variable`: Nombre de variable a comparar (ej: 'CO_Item_3_Izq').
- `Grupos_A`: Lista de categorías del primer grupo (ej: ['Left_Wing', 'Progressivism']).
- `Grupos_B`: Lista de categorías del segundo grupo (ej: ['Right_Wing_Libertarian']).

**Retorna**: Diccionario con:
- `U`: Estadístico U.
- `P_Valor`: Significancia.
- `Significativo`: Boolean (p < 0.05).
- `Tamaño_Efecto`: Magnitud del efecto (r).
- `Mediana_Grupo_A`: Mediana del grupo A.
- `Mediana_Grupo_B`: Mediana del grupo B.

**Ejemplo**:
```python
from Mann_Whitney import Ejecutar_Mann_Whitney

Resultado = Ejecutar_Mann_Whitney(
    Df_Generales,
    'CO_Item_3_Izq',
    ['Left_Wing', 'Progressivism'],
    ['Right_Wing_Libertarian']
)

print(f"P-valor: {Resultado['P_Valor']:.4f}")
print(f"Significativo: {Resultado['Significativo']}")
```

---

### Congruencia_Ideologica.py

**Ubicación**: `Codigo/Test_Estadisticos/Congruencia_Ideologica.py`

**Propósito**: Análisis de congruencia ideológica (congruente vs incongruente).

#### `Analizar_Congruencia_Por_Candidato(Df: pd.DataFrame, Lista_Candidatos: List[str]) -> pd.DataFrame`

Analiza diferencias entre cambios congruentes e incongruentes para cada candidato.

**Parámetros**:
- `Df`: DataFrame con variables CO_Congruentes/Incongruentes.
- `Lista_Candidatos`: Lista de candidatos a analizar.

**Retorna**: DataFrame con resultados por candidato (medianas, p-valores, significancia).

**Ejemplo**:
```python
from Congruencia_Ideologica import (
    Analizar_Congruencia_Por_Candidato
)

Resultados = Analizar_Congruencia_Por_Candidato(
    Df_Generales,
    Lista_Candidatos=['Milei', 'Bullrich', 'Bregman', 'Solano']
)
```

---

### Validacion_Cruzada.py

**Ubicación**: `Codigo/Test_Estadisticos/Validacion_Cruzada.py`

**Propósito**: Validación cruzada de items significativos entre Generales y Ballotage.

#### `Validar_Items_Cruzados(Df_Generales: pd.DataFrame, Df_Ballotage: pd.DataFrame, Umbral_P: float = 0.05) -> Dict`

Identifica items significativos en ambas elecciones.

**Parámetros**:
- `Df_Generales`: DataFrame de Generales.
- `Df_Ballotage`: DataFrame de Ballotage.
- `Umbral_P`: Umbral de significancia (default: 0.05).

**Retorna**: Diccionario con items robustos (significativos en ambas elecciones).

---

### Diferencia_Diferencias.py

**Ubicación**: `Codigo/Test_Estadisticos/Diferencia_Diferencias.py`

**Propósito**: Análisis de diferencia de diferencias entre Generales y Ballotage.

#### `Calcular_Diferencia_De_Diferencias(Df_Generales: pd.DataFrame, Df_Ballotage: pd.DataFrame, Variable: str) -> Dict`

Calcula diferencia de diferencias para una variable entre elecciones.

**Parámetros**:
- `Df_Generales`: DataFrame de Generales.
- `Df_Ballotage`: DataFrame de Ballotage.
- `Variable`: Variable a analizar (ej: 'CO_Item_3_Izq').

**Retorna**: Diccionario con diferencias y test estadístico.

---

## MÓDULOS DE MODELADO

### Modelos_SEM.py

**Ubicación**: `Codigo/Modelado_Estadistico/Modelos_SEM.py`

**Propósito**: Modelos de ecuaciones estructurales (SEM).

#### `Ejecutar_Modelo_SEM_Simple(Df: pd.DataFrame, Variable_Predictora: str, Variable_Outcome: str) -> Dict`

Ejecuta modelo SEM simple (una variable predictora → una variable outcome).

**Parámetros**:
- `Df`: DataFrame con datos.
- `Variable_Predictora`: Nombre de variable independiente (ej: 'Indice_Progresismo').
- `Variable_Outcome`: Nombre de variable dependiente (ej: 'CO_Item_3_Izq').

**Retorna**: Diccionario con:
- `Exito`: Boolean.
- `N`: Número de observaciones.
- `Coeficiente`: β estimado.
- `P_Valor`: Significancia.
- `R2`: Proporción de varianza explicada.

**Ejemplo**:
```python
from Modelos_SEM import Ejecutar_Modelo_SEM_Simple

Resultado = Ejecutar_Modelo_SEM_Simple(
    Df_Generales,
    'Indice_Progresismo',
    'CO_Item_3_Izq'
)

if Resultado['Exito']:
    print(f"Coeficiente: {Resultado['Coeficiente']:.3f}")
    print(f"R²: {Resultado['R2']:.3f}")
```

---

### Correlaciones.py

**Ubicación**: `Codigo/Modelado_Estadistico/Correlaciones.py`

**Propósito**: Cálculo de correlaciones de Spearman.

#### `Calcular_Matriz_Correlaciones_Spearman(Df: pd.DataFrame, Variables: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]`

Calcula matriz de correlaciones de Spearman y p-valores.

**Parámetros**:
- `Df`: DataFrame con datos.
- `Variables`: Lista de variables a correlacionar.

**Retorna**: Tupla con (Matriz_Correlaciones, Matriz_P_Valores).

**Ejemplo**:
```python
from Correlaciones import Calcular_Matriz_Correlaciones_Spearman

Variables = [
    'Indice_Progresismo',
    'Indice_Conservadurismo',
    'CO_Item_3_Izq'
]

Matriz, P_Valores = Calcular_Matriz_Correlaciones_Spearman(
    Df_Generales,
    Variables
)
```

---

### Clusters.py

**Ubicación**: `Codigo/Modelado_Estadistico/Clusters.py`

**Propósito**: Algoritmos de clustering (Kmeans, Jerárquico, DBSCAN).

#### `Ejecutar_Kmeans(Df: pd.DataFrame, Variables: List[str], N_Clusters: int = 3) -> pd.Series`

Ejecuta K-means clustering.

**Parámetros**:
- `Df`: DataFrame con datos.
- `Variables`: Lista de variables para clustering.
- `N_Clusters`: Número de clusters (default: 3).

**Retorna**: Serie con asignación de clusters.

---

## MÓDULOS DE VISUALIZACIÓN

### Graficos_Cleveland.py

**Ubicación**: `Codigo/Visualizacion/Graficos_Cleveland.py`

**Propósito**: Gráficos de Cleveland (dot plots) para comparaciones.

#### `Crear_Cleveland_Comparativo(Df_Resultados: pd.DataFrame, Titulo: str, Nombre_Archivo: str) -> None`

Crea gráfico de Cleveland comparando dos grupos.

**Parámetros**:
- `Df_Resultados`: DataFrame con resultados (columnas: Item, Grupo_A, Grupo_B).
- `Titulo`: Título del gráfico.
- `Nombre_Archivo`: Nombre base del archivo (sin extensión).

**Salida**: Archivos PNG y SVG en `Graficos/Cleveland/`.

**Ejemplo**:
```python
from Graficos_Cleveland import Crear_Cleveland_Comparativo

Crear_Cleveland_Comparativo(
    Df_Resultados,
    'Comparación CO Congruentes vs Incongruentes',
    'Cleveland_CO_Congruente_vs_Incongruente_Generales'
)
```

---

### Heatmaps.py

**Ubicación**: `Codigo/Visualizacion/Heatmaps.py`

**Propósito**: Heatmaps de matrices de correlación.

#### `Crear_Heatmap_Correlaciones(Matriz: pd.DataFrame, Titulo: str, Nombre_Archivo: str) -> None`

Crea heatmap de matriz de correlaciones.

**Parámetros**:
- `Matriz`: Matriz de correlaciones.
- `Titulo`: Título del gráfico.
- `Nombre_Archivo`: Nombre base del archivo.

**Salida**: Archivos PNG y SVG en `Graficos/Heatmaps/`.

---

### Graficos_Violin.py

**Ubicación**: `Codigo/Visualizacion/Graficos_Violin.py`

**Propósito**: Gráficos de violín para distribuciones por categoría.

#### `Crear_Violin_Por_Categoria(Df: pd.DataFrame, Variable: str, Columna_Categoria: str, Titulo: str, Nombre_Archivo: str) -> None`

Crea gráfico de violín mostrando distribución de variable por categoría.

**Parámetros**:
- `Df`: DataFrame con datos.
- `Variable`: Variable a graficar.
- `Columna_Categoria`: Columna para agrupar.
- `Titulo`: Título del gráfico.
- `Nombre_Archivo`: Nombre base del archivo.

**Salida**: Archivos PNG y SVG en `Graficos/Violin/`.

---

### Graficos_Barras.py

**Ubicación**: `Codigo/Visualizacion/Graficos_Barras.py`

**Propósito**: Gráficos de barras con barras de error.

#### `Crear_Barras_Con_Error(Df: pd.DataFrame, Variable: str, Columna_Categoria: str, Titulo: str, Nombre_Archivo: str) -> None`

Crea gráfico de barras mostrando medias y errores estándar por categoría.

**Salida**: Archivos PNG y SVG en `Graficos/Barras/`.

---

### Graficos_Boxplot.py

**Ubicación**: `Codigo/Visualizacion/Graficos_Boxplot.py`

**Propósito**: Boxplots para distribuciones con outliers.

#### `Crear_Boxplot_Por_Categoria(Df: pd.DataFrame, Variable: str, Columna_Categoria: str, Titulo: str, Nombre_Archivo: str) -> None`

Crea boxplot mostrando distribución con cuartiles y outliers.

**Salida**: Archivos PNG y SVG en `Graficos/Boxplot/`.

---

## MÓDULOS DE UTILIDADES

### Funciones_Comunes.py

**Ubicación**: `Codigo/Utilidades/Funciones_Comunes.py`

**Propósito**: Funciones reutilizables para operaciones comunes.

#### `Aplanar_Diccionario(Diccionario: Dict, Prefijo: str = '') -> Dict`

Aplana diccionario anidado en claves planas.

**Parámetros**:
- `Diccionario`: Diccionario anidado.
- `Prefijo`: Prefijo para claves (default: '').

**Retorna**: Diccionario con claves planas.

**Ejemplo**:
```python
from Funciones_Comunes import Aplanar_Diccionario

Dic_Anidado = {'IP_Item_3': {'Respuesta': 5, 'Tiempo': 1200}}
Dic_Plano = Aplanar_Diccionario(Dic_Anidado)
# {'IP_Item_3_Respuesta': 5, 'IP_Item_3_Tiempo': 1200}
```

---

#### `Eliminar_Filas_Por_Desviacion_Estandar(Df: pd.DataFrame, Columnas: List[str], Numero_Desviaciones: int) -> pd.DataFrame`

Elimina filas con valores extremos en columnas especificadas.

**Parámetros**:
- `Df`: DataFrame.
- `Columnas`: Lista de columnas a verificar.
- `Numero_Desviaciones`: Umbral de desviaciones estándar.

**Retorna**: DataFrame filtrado.

---

### Configuracion.py

**Ubicación**: `Codigo/Utilidades/Configuracion.py`

**Propósito**: Constantes y configuración global del proyecto.

**Constantes Principales**:

```python
# Rutas.
RUTA_BASE = Path(__file__).parent.parent.parent
RUTA_DATOS_CRUDOS = RUTA_BASE / "Data" / "Datos_Crudos"
RUTA_BASES_DEFINITIVAS = RUTA_BASE / "Data" / "Bases definitivas"
RUTA_GRAFICOS = RUTA_BASE / "Graficos"
RUTA_TABLAS = RUTA_BASE / "Tablas"
RUTA_REPORTES = RUTA_BASE / "Reportes"

# Parámetros de limpieza.
NUM_DESVIACIONES_OUTLIERS = 3
CATEGORIAS_EXCLUIR = ['Other', 'No apply', 'No response', 'Blank']

# Items progresistas y conservadores.
ITEMS_PROGRESISTAS = [3, 4, 5, 6, 7, 9, 10, 16, 22, 24]
ITEMS_CONSERVADORES = [8, 11, 19, 20, 23, 25, 27, 28, 29, 30]

# Candidatos por dirección.
CANDIDATOS_IZQUIERDA = ['Bregman', 'Solano']
CANDIDATOS_DERECHA = ['Milei', 'Bullrich']
```

---

## SISTEMA DE CONTROL

### Control_01_Construccion_Bases.py

**Ubicación**: `Codigo/Control/Control_01_Construccion_Bases.py`

**Propósito**: Verificar construcción correcta de bases.

#### `Ejecutar_Control_Construccion_Bases(Nombre_Base: str, Df: pd.DataFrame) -> bool`

Ejecuta control de construcción de bases y genera reporte PDF.

**Verificaciones**:
- IDs únicos sin duplicados.
- Existencia de columnas críticas.
- Tipos de datos correctos.
- Sin NaN en columnas críticas.
- Rangos de edad válidos [18-100].

**Retorna**: True si aprueba todas las verificaciones, False en caso contrario.

---

### Control_16_Ejecutar_Todos.py

**Ubicación**: `Codigo/Control/Control_16_Ejecutar_Todos.py`

**Propósito**: Script maestro para ejecutar todos los controles.

#### `Ejecutar_Todos_Los_Controles() -> None`

Ejecuta los 16 controles secuencialmente para Generales y Ballotage.

**Proceso**:
1. Carga bases de `Data/Bases definitivas/`.
2. Ejecuta controles 01-10 y 15 para cada base.
3. Genera reporte consolidado PDF.
4. Muestra resumen con controles aprobados/fallidos.

**Ejemplo**:
```bash
cd Codigo/Control
python Control_16_Ejecutar_Todos.py
```

**Salida**: Reporte PDF en `Reportes/Control/Control_Consolidado_YYYYMMDD_HHMMSS.pdf`.

Ver `Docs/GUIA_CONTROLES.md` para documentación completa de todos los controles.

---

## CONVENCIONES DE CÓDIGO

### Nomenclatura

- **Pascal_Snake_Case**: Todas las variables, funciones, clases, archivos.
- **Nombres descriptivos**: No abreviaciones genéricas.
- **Funciones con verbos**: `Calcular_Indice`, `Ejecutar_Control`, `Crear_Grafico`.

### Docstrings

Todas las funciones públicas incluyen:
- Descripción detallada del propósito.
- Type hinting en parámetros y retorno.
- Ejemplos de uso (cuando relevante).

### Formato

```python
def Funcion_Ejemplo(Parametro_Uno: str,
                    Parametro_Dos: int) -> bool:

    """
    Descripción detallada de qué hace esta función.
    Puede incluir múltiples líneas explicativas.

    """

    return True
```

---

## CONTACTO Y SOPORTE

Para más información, consultar:
- **README.md**: Documentación general.
- **PIPELINE_TECNICO.md**: Flujo técnico completo.
- **GUIA_CONTROLES.md**: Sistema de control.

---

**Última actualización**: 2025-01-10
**Versión**: 1.0
