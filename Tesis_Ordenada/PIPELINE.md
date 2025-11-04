# PIPELINE COMPLETO DE PROCESAMIENTO Y ANÁLISIS

Este documento describe **TODO** el flujo de procesamiento y análisis del experimento de personalidad implícita y política en las elecciones argentinas 2023, desde los datos crudos hasta los resultados finales.

---

## ÍNDICE

1. [Objetivo del Experimento](#objetivo-del-experimento)
2. [Datos de Entrada](#datos-de-entrada)
3. [Paso 1: Construcción de Bases de Datos](#paso-1-construcción-de-bases-de-datos)
4. [Paso 2: Procesamiento de Columna JSON](#paso-2-procesamiento-de-columna-json)
5. [Paso 3: Cálculo de Índices Ideológicos](#paso-3-cálculo-de-índices-ideológicos)
6. [Paso 4: Creación de Variables de Cambio](#paso-4-creación-de-variables-de-cambio)
7. [Paso 5: Limpieza y Eliminación de Outliers](#paso-5-limpieza-y-eliminación-de-outliers)
8. [Paso 6: Tests Estadísticos Mann-Whitney](#paso-6-tests-estadísticos-mann-whitney)
9. [Paso 7: Modelos de Ecuaciones Estructurales](#paso-7-modelos-de-ecuaciones-estructurales)
10. [Paso 8: Modelos Robustos de Regresión](#paso-8-modelos-robustos-de-regresión)
11. [Paso 9: Visualizaciones](#paso-9-visualizaciones)
12. [Paso 10: Exportación de Resultados](#paso-10-exportación-de-resultados)
13. [Resumen de Variables Generadas](#resumen-de-variables-generadas)

---

## OBJETIVO DEL EXPERIMENTO

**Pregunta de investigación**: ¿Cómo influye la ideología política en los cambios de opinión (CO) y tiempos de respuesta (CT) cuando se asocian items ideológicos con candidatos políticos?

### Diseño Experimental

1. **Fase Base**: Participantes evalúan 20 items ideológicos (IP Items) en escala 1-5 y registran tiempo de respuesta.
2. **Fase Asociada**: Mismos items presentados asociados a candidatos políticos (izquierda o derecha), participantes vuelven a evaluar.
3. **Medición**: Cambio de Opinión (CO) = Respuesta Asociada - Respuesta Base.
4. **Medición**: Cambio de Tiempo (CT) = Tiempo Asociado - Tiempo Base.

### Hipótesis Principal

Participantes cambiarán más su opinión hacia candidatos congruentes con su ideología:
- **Progresistas** → Mayor CO hacia candidatos de izquierda en items progresistas.
- **Conservadores** → Mayor CO hacia candidatos de derecha en items conservadores.

### Contexto

- **Elecciones**: Argentina 2023 (Generales y Ballotage).
- **Items**: 10 progresistas + 10 conservadores.
- **Participantes**: ~2786 (Generales), ~1254 (Ballotage).
- **Categorías ideológicas**: Left_Wing, Progressivism, Centre, Moderate_Right_A, Moderate_Right_B, Right_Wing_Libertarian.

---

## DATOS DE ENTRADA

### Ubicación

```
Tesis_Ordenada/Data/Datos_Crudos/
```

### Archivos CSV

**Generales (5 archivos)**:
1. `Generales_Base.csv`
2. `Generales_Izquierda_1.csv`
3. `Generales_Izquierda_2.csv`
4. `Generales_Derecha_1.csv`
5. `Generales_Derecha_2.csv`

**Ballotage (2 archivos)**:
1. `Ballotage_Base.csv`
2. `Ballotage_Asociados.csv`

### Estructura de Datos Crudos

**Columnas principales**:
- `ID`: Identificador único del participante.
- `JSON`: Columna con diccionario anidado conteniendo:
  - `IP_Item_N_Respuesta`: Respuesta 1-5 al item N.
  - `IP_Item_N_Tiempo`: Tiempo de respuesta (ms).
  - `IP_Item_N_Candidato`: Candidato asociado (si aplica).
- Variables demográficas: Edad, Género, Región, etc.
- Variables políticas: Voto 2019, Categoría PASO 2023, etc.

### Tamaño

Aproximadamente 22 MB totales (7 archivos CSV).

---

## PASO 1: CONSTRUCCIÓN DE BASES DE DATOS

### Módulo

`Codigo/Procesamiento/Construccion_Bases.py`

### Funciones

#### `Combinar_Archivos_Generales()`

Combina los 5 archivos CSV de Generales en un único DataFrame.

```python
from Construccion_Bases import Combinar_Archivos_Generales

Df_Generales_Crudo = Combinar_Archivos_Generales()
# Resultado: DataFrame con ~2786 filas
```

#### `Combinar_Archivos_Ballotage()`

Combina los 2 archivos CSV de Ballotage en un único DataFrame.

```python
from Construccion_Bases import Combinar_Archivos_Ballotage

Df_Ballotage_Crudo = Combinar_Archivos_Ballotage()
# Resultado: DataFrame con ~1254 filas
```

### Salida

- **Df_Generales_Crudo**: DataFrame crudo con datos de Generales.
- **Df_Ballotage_Crudo**: DataFrame crudo con datos de Ballotage.

**Columnas**: ID, JSON (diccionario), variables demográficas.

---

## PASO 2: PROCESAMIENTO DE COLUMNA JSON

### Módulo

`Codigo/Procesamiento/Construccion_Bases.py` (función `Procesar_Base_Completa`)

### Proceso

1. **Aplanar diccionario JSON**: Convierte el diccionario anidado en columnas individuales.
2. **Rellenar items faltantes**: Items que no fueron presentados se marcan como NaN.
3. **Crear variables de orden**: Para items progresistas/conservadores.

### Funciones Auxiliares (en `Funciones_Comunes.py`)

#### `Aplanar_Diccionario(Diccionario, Prefijo)`

Convierte diccionario anidado en claves planas:
- `{'IP_Item_3': {'Respuesta': 5}}` → `'IP_Item_3_Respuesta': 5`

#### `Rellenar_IP_Items_Asociados_Faltantes(Df)`

Rellena con NaN los items que no fueron presentados a cada participante (diseño contrabalanceado).

#### `Crear_Variables_De_Orden_IP_Items(Df)`

Crea columnas `Orden_Item_N` indicando en qué posición se presentó cada item.

### Uso

```python
from Construccion_Bases import Procesar_Base_Completa

Df_Generales = Procesar_Base_Completa(Df_Generales_Crudo)
Df_Ballotage = Procesar_Base_Completa(Df_Ballotage_Crudo)
```

### Salida

DataFrames con columnas expandidas:
- `IP_Item_3_Respuesta`, `IP_Item_3_Tiempo`, `IP_Item_3_Candidato`
- `IP_Item_4_Respuesta`, `IP_Item_4_Tiempo`, `IP_Item_4_Candidato`
- ... (para los 20 items IP)

---

## PASO 3: CÁLCULO DE ÍNDICES IDEOLÓGICOS

### Módulo

`Codigo/Procesamiento/Calculo_Indices.py`

### Índices Calculados

#### 1. Índice de Progresismo

**Fórmula**: Promedio de respuestas a items progresistas (3, 4, 5, 6, 7, 9, 10, 16, 22, 24).

```python
from Calculo_Indices import Calcular_Indice_Progresismo

Df['Indice_Progresismo'] = Calcular_Indice_Progresismo(Df)
```

**Rango**: 1-5 (mayor = más progresista).

#### 2. Índice de Conservadurismo

**Fórmula**: Promedio de respuestas a items conservadores (8, 11, 19, 20, 23, 25, 27, 28, 29, 30).

```python
from Calculo_Indices import Calcular_Indice_Conservadurismo

Df['Indice_Conservadurismo'] = (
    Calcular_Indice_Conservadurismo(Df)
)
```

**Rango**: 1-5 (mayor = más conservador).

#### 3. Índice de Positividad

**Fórmula**: Promedio de TODOS los 20 items IP.

```python
from Calculo_Indices import Calcular_Indice_Positividad

Df['Indice_Positividad'] = Calcular_Indice_Positividad(Df)
```

**Interpretación**: Tendencia general a estar de acuerdo con afirmaciones.

#### 4. Índices de Tiempo

También se calculan:
- `Indice_Progresismo_Tiempo`: Promedio de tiempos en items progresistas.
- `Indice_Conservadurismo_Tiempo`: Promedio de tiempos en items conservadores.

### Función Consolidada

```python
from Calculo_Indices import Calcular_Todos_Indices

Df = Calcular_Todos_Indices(Df)
# Agrega las 5 columnas de índices al DataFrame
```

### Salida

Nuevas columnas en el DataFrame:
- `Indice_Progresismo`
- `Indice_Conservadurismo`
- `Indice_Positividad`
- `Indice_Progresismo_Tiempo`
- `Indice_Conservadurismo_Tiempo`

---

## PASO 4: CREACIÓN DE VARIABLES DE CAMBIO

### Módulo

`Codigo/Procesamiento/Calculo_Variables_Cambio.py`

### Variables Calculadas

#### 1. Cambio de Opinión (CO)

**Fórmula**: CO = Respuesta_Asociada - Respuesta_Base

Se crean variables para cada item y cada dirección política:
- `CO_Item_3_Izq`: Cambio al asociar item 3 con candidato izquierda.
- `CO_Item_3_Der`: Cambio al asociar item 3 con candidato derecha.
- ... (para los 20 items × 2 direcciones)

**Rango**: -4 a +4
- **Positivo**: Aumentó acuerdo con el item.
- **Negativo**: Disminuyó acuerdo con el item.
- **Cero**: Sin cambio.

#### 2. Cambio de Tiempo (CT)

**Fórmula**: CT = Tiempo_Asociado - Tiempo_Base

Misma estructura que CO:
- `CT_Item_3_Izq`, `CT_Item_3_Der`, etc.

**Interpretación**:
- **Positivo**: Tardó más tiempo (posible conflicto cognitivo).
- **Negativo**: Tardó menos tiempo (mayor fluidez).

#### 3. Variables de Congruencia

**CO_Congruentes_Promedio**: Promedio de cambios congruentes con ideología:
- Participante izquierda + Item progresista + Candidato izquierda.
- Participante derecha + Item conservador + Candidato derecha.

**CO_Incongruentes_Promedio**: Promedio de cambios incongruentes:
- Participante izquierda + Item progresista + Candidato derecha.
- Participante derecha + Item conservador + Candidato izquierda.

### Uso

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

### Salida

Hasta 40 nuevas columnas por DataFrame:
- 20 items × 2 direcciones de CO
- 20 items × 2 direcciones de CT
- 2 variables de congruencia (CO_Congruentes/Incongruentes)

---

## PASO 5: LIMPIEZA Y ELIMINACIÓN DE OUTLIERS

### Módulo

`Codigo/Procesamiento/Limpieza_Datos.py`

### Criterios de Limpieza

#### 1. Filtrado por Categoría Ideológica

**Elimina participantes con categorías inválidas**:
- `'Other'`: Sin categoría ideológica clara.
- `'No apply'`: Sin información ideológica.
- `'No response'`: Sin respuesta a clasificación.
- `'Blank'`: Respuestas en blanco.

**Razón**: Estas categorías distorsionan los análisis comparativos entre grupos ideológicos.

#### 2. Filtrado por Outliers de Tiempo

**Elimina participantes con tiempos de respuesta extremos**:
- Criterio: Media + (3 × Desviación_Estándar).
- Calculado sobre TODOS los tiempos de TODOS los participantes.
- Elimina fila COMPLETA si CUALQUIER tiempo excede el umbral.

**Razón**: Tiempos extremos indican falta de atención, problemas técnicos o respuestas automáticas.

### Funciones Principales

#### `Filtrar_Categorias_Invalidas(Df)`

Elimina participantes con categorías problemáticas.

```python
from Limpieza_Datos import Filtrar_Categorias_Invalidas

Df_Limpio = Filtrar_Categorias_Invalidas(Df)
# Elimina 'Other', 'No apply', 'No response', 'Blank'
```

#### `Filtrar_Outliers_Por_Tiempo(Df)`

Elimina participantes con tiempos extremos (3 desv. estándar).

```python
from Limpieza_Datos import Filtrar_Outliers_Por_Tiempo

Df_Limpio = Filtrar_Outliers_Por_Tiempo(Df)
# Elimina filas con tiempos > Media + 3×Desv
```

#### `Limpiar_Datos_Completo(Df)`

Aplica TODOS los filtros en secuencia.

```python
from Limpieza_Datos import Limpiar_Datos_Completo

Df_Limpio = Limpiar_Datos_Completo(
    Df,
    Filtrar_Categorias=True,
    Filtrar_Tiempos=True,
    Numero_Desviaciones=3
)
```

#### `Limpiar_Diccionario_Dataframes(Dict_Dfs)`

Limpia múltiples DataFrames a la vez.

```python
from Limpieza_Datos import Limpiar_Diccionario_Dataframes

Diccionario_Dfs = {
    'Generales': Df_Generales,
    'Ballotage': Df_Ballotage
}

Diccionario_Limpio = Limpiar_Diccionario_Dataframes(
    Diccionario_Dfs
)

Df_Generales = Diccionario_Limpio['Generales']
Df_Ballotage = Diccionario_Limpio['Ballotage']
```

### Orden de Aplicación

**IMPORTANTE**: Los filtros se aplican en este orden:
1. **Primero categorías**: Elimina grupos problemáticos.
2. **Luego tiempos**: Calcula estadísticos sobre datos ya filtrados.

### Parámetros Configurables

- **NUM_DESVIACIONES_OUTLIERS**: 3 (en `Configuracion.py`).
- **CATEGORIAS_EXCLUIR**: ['Other', 'No apply', 'No response', 'Blank'] (en `Configuracion.py`).

### Impacto Típico

| Filtro | % Eliminado Típico |
|--------|-------------------|
| Categorías | 2-5% |
| Tiempos | 1-3% |
| **TOTAL** | **3-8%** |

### Salida

DataFrame limpio con:
- Solo categorías ideológicas válidas.
- Sin outliers extremos de tiempo.
- Datos de alta calidad para análisis.

---

## PASO 6: TESTS ESTADÍSTICOS MANN-WHITNEY

### Módulo

`Codigo/Test_Estadisticos/Mann_Whitney.py`

### Objetivo

Comparar distribuciones de variables CO/CT entre grupos ideológicos.

### Función Principal

`Ejecutar_Mann_Whitney(Df, Variable, Grupos_A, Grupos_B)`

### Proceso

1. **Filtrar datos**: Extraer observaciones de Grupos_A y Grupos_B.
2. **Test U de Mann-Whitney**: Comparación no paramétrica de distribuciones.
3. **Calcular tamaño del efecto**: r = Z / √N.
4. **Determinar significancia**: p < 0.05.

### Uso

```python
from Mann_Whitney import Ejecutar_Mann_Whitney

Resultado = Ejecutar_Mann_Whitney(
    Df_Generales,
    'CO_Item_3_Izq',
    ['Left_Wing', 'Progressivism'],  # Grupos A
    ['Right_Wing_Libertarian']        # Grupos B
)

print(f"U: {Resultado['U']}")
print(f"P-valor: {Resultado['P_Valor']}")
print(f"Significativo: {Resultado['Significativo']}")
print(f"Tamaño efecto: {Resultado['Tamaño_Efecto']}")
```

### Comparaciones Típicas

1. **Izquierda vs Derecha**: Left_Wing + Progressivism vs Right_Wing_Libertarian.
2. **Progresistas vs Conservadores**: En cada variable CO.
3. **Generales vs Ballotage**: Diferencia de diferencias temporal.

### Salida

Diccionario con:
- `U`: Estadístico U.
- `P_Valor`: Significancia.
- `Significativo`: Boolean.
- `Tamaño_Efecto`: Magnitud del efecto (r).
- `Mediana_Grupo_A`: Mediana del grupo A.
- `Mediana_Grupo_B`: Mediana del grupo B.

---

## PASO 7: MODELOS DE ECUACIONES ESTRUCTURALES

### Módulo

`Codigo/Modelado_Estadistico/Modelos_SEM.py`

### Objetivo

Modelar relaciones causales entre índices ideológicos y variables CO/CT.

### Función Principal

`Ejecutar_Modelo_SEM_Simple(Df, Variable_Predictora, Variable_Outcome)`

### Proceso

1. **Especificación del modelo**: `Outcome ~ Predictor`.
2. **Ajuste del modelo**: Usando librería `semopy`.
3. **Extracción de resultados**: Coeficientes, p-valores, R².

### Uso

```python
from Modelos_SEM import Ejecutar_Modelo_SEM_Simple

Resultado = Ejecutar_Modelo_SEM_Simple(
    Df_Generales,
    'Indice_Progresismo',
    'CO_Item_3_Izq'
)

if Resultado['Exito']:
    print(f"Coeficiente: {Resultado['Coeficiente']}")
    print(f"P-valor: {Resultado['P_Valor']}")
    print(f"R²: {Resultado['R2']}")
```

### Modelos Típicos

1. **Progresismo → CO progresistas izquierda**: ¿Mayor progresismo predice mayor CO hacia izquierda?
2. **Conservadurismo → CO conservadores derecha**: ¿Mayor conservadurismo predice mayor CO hacia derecha?

### Salida

Diccionario con:
- `Exito`: Boolean.
- `N`: Número de observaciones.
- `Coeficiente`: β estimado.
- `P_Valor`: Significancia.
- `R2`: Proporción de varianza explicada.

---

## PASO 8: MODELOS ROBUSTOS DE REGRESIÓN

### Módulo

`Codigo/Modelado_Estadistico/Modelos_Robustos.py`

### Objetivo

Construir modelos de regresión multivariable robustos con selección automática de variables.

### Función Principal

`Modelo_Lineal_Robusto(Variables_X, Variable_Y, Nombre_Variable, ...)`

### Proceso Metodológico

1. **Detección de outliers influyentes**:
   - Distancia de Cook > 4/n.
   - Leverage > 2p/n.
   - Residuos studentizados > 3.

2. **Eliminación de multicolinealidad (VIF)**:
   - Calcular VIF para cada variable.
   - Eliminar variables con VIF > 5.0 iterativamente.

3. **Selección secuencial de variables**:
   - Criterio AIC/BIC/p-valor.
   - Eliminar una variable por iteración.
   - Continuar hasta que todas sean significativas (p < 0.05).

4. **Errores estándar robustos**:
   - Corrección HC3 para heterocedasticidad.

5. **Diagnósticos finales**:
   - Test Jarque-Bera (normalidad).
   - Test Breusch-Pagan (heterocedasticidad).
   - Durbin-Watson (autocorrelación).

### Uso

```python
from Modelos_Robustos import (
    Modelo_Lineal_Robusto,
    Limpiar_Y_Estructurar_Datos_Para_Modelado,
    Codificar_Variables_Booleanas_A_Numericas,
    Codificar_Variables_Categoricas_A_Numericas
)

# Preparar datos.
Variables_Independientes = [
    'Indice_Progresismo',
    'Indice_Conservadurismo',
    'Edad',
    'Genero_Masculino',
    # ... más variables
]

X, y = Limpiar_Y_Estructurar_Datos_Para_Modelado(
    Df_Generales,
    'CO_Item_3_Izq',
    Variables_Independientes
)

X = Codificar_Variables_Booleanas_A_Numericas(X)
X = Codificar_Variables_Categoricas_A_Numericas(X)

# Ejecutar modelo robusto.
Resultado = Modelo_Lineal_Robusto(
    Variables_X=X,
    Variable_Y=y,
    Nombre_Variable='CO_Item_3_Izq',
    Criterio_Eliminacion='aic',
    Umbral_VIF=5.0,
    Alpha_Significancia=0.05,
    Detectar_Outliers=True
)

# Interpretar resultados.
from Modelos_Robustos import Evaluar_Modelo_Robusto

Evaluacion = Evaluar_Modelo_Robusto(
    Resultado,
    Mostrar_Detalles_Tecnicos=True
)
```

### Variables Independientes Típicas

- **Índices**: Indice_Progresismo, Indice_Conservadurismo, Indice_Positividad.
- **Demográficas**: Edad, Genero, Region, Estrato_Social.
- **Políticas**: Categoria_PASO_2023, Voto_2019, Autopercepcion_Izq_Der.
- **Medios**: Influencia_Redes, Medios_Prensa_X.

### Salida

Diccionario con:
- **Métricas de ajuste**: R², R² ajustado, AIC, BIC, F-estadístico.
- **Variables significativas**: Lista de predictores finales.
- **Coeficientes**: β para cada predictor.
- **P-valores**: Significancia de cada predictor.
- **Diagnósticos**: Tests de normalidad, heterocedasticidad, autocorrelación.
- **Proceso**: Historial de eliminación de variables.

---

## PASO 9: VISUALIZACIONES

### Módulos

`Codigo/Visualizacion/Graficos_Cleveland.py`
`Codigo/Visualizacion/` (otros módulos de visualización)

### Tipos de Gráficos

#### 1. Gráficos de Cleveland (Dot Plots)

**Función**: `Crear_Cleveland_Comparativo(Df_Resultados, Titulo, Nombre_Archivo)`

**Uso**:
```python
from Graficos_Cleveland import Crear_Cleveland_Comparativo

Crear_Cleveland_Comparativo(
    Df_Resultados,
    'Comparación CO Congruentes vs Incongruentes',
    'Cleveland_CO_Congruente_vs_Incongruente_Generales'
)
```

**Salida**: Gráfico mostrando diferencias entre grupos con puntos y líneas.

#### 2. Heatmaps de Correlación

Matrices de correlación entre índices ideológicos y variables CO/CT.

#### 3. Gráficos de Violín

Distribuciones de variables CO por categoría ideológica.

#### 4. Gráficos de Barras

Comparaciones de medias entre grupos con barras de error.

### Formatos de Exportación

- **PNG**: 300 DPI para documentos.
- **SVG**: Vectorial para edición.

### Ubicación

```
Tesis_Ordenada/Graficos/
├── Cleveland/
├── Heatmaps/
├── Violin/
└── Barras/
```

---

## PASO 10: EXPORTACIÓN DE RESULTADOS

### Bases Procesadas

**Ubicación**: `Tesis_Ordenada/Tablas/Bases_Procesadas/`

```python
Df_Generales.to_excel(
    'Tablas/Bases_Procesadas/Base_Generales_Procesada.xlsx',
    index=False
)
Df_Ballotage.to_excel(
    'Tablas/Bases_Procesadas/Base_Ballotage_Procesada.xlsx',
    index=False
)
```

### Resultados de Tests

**Ubicación**: `Tesis_Ordenada/Tablas/Resultados_Tests/`

Tablas Excel con resultados de Mann-Whitney para cada comparación.

### Resultados de Modelos

**Ubicación**: `Tesis_Ordenada/Tablas/Resultados_SEM/`

Tablas Excel con:
- Coeficientes β.
- P-valores.
- Métricas de ajuste (R², AIC, BIC).
- Variables significativas por modelo.

**Formato**: Matriz con variables independientes en filas, variables dependientes en columnas, celdas coloreadas por significancia (verde = p < 0.05, gris = no significativo).

---

## RESUMEN DE VARIABLES GENERADAS

### Datos Crudos → Variables Procesadas

| Etapa | Variables de Entrada | Variables de Salida | Cantidad |
|-------|---------------------|---------------------|----------|
| **1. Construcción** | CSV crudos (7 archivos) | Df unificado | 2 DataFrames |
| **2. JSON** | Columna JSON anidada | IP_Item_N_Respuesta/Tiempo/Candidato | 60 columnas |
| **3. Índices** | Respuestas IP items | Indice_Progresismo, Indice_Conservadurismo, etc. | 5 columnas |
| **4. Cambio** | Respuestas base vs asociadas | CO_Item_N_Izq/Der, CT_Item_N_Izq/Der | 80 columnas |
| **4b. Congruencia** | Variables CO + Categoría | CO_Congruentes/Incongruentes_Promedio | 2 columnas |
| **5. Limpieza** | DataFrame completo | DataFrame sin outliers | - |

### Variables por Tipo

#### Variables de Respuesta (60 columnas)

- `IP_Item_3_Respuesta` ... `IP_Item_30_Respuesta` (20 items)
- `IP_Item_3_Tiempo` ... `IP_Item_30_Tiempo` (20 items)
- `IP_Item_3_Candidato` ... `IP_Item_30_Candidato` (20 items)

#### Índices Ideológicos (5 columnas)

- `Indice_Progresismo`
- `Indice_Conservadurismo`
- `Indice_Positividad`
- `Indice_Progresismo_Tiempo`
- `Indice_Conservadurismo_Tiempo`

#### Variables de Cambio de Opinión (40 columnas)

- `CO_Item_3_Izq`, `CO_Item_3_Der`
- `CO_Item_4_Izq`, `CO_Item_4_Der`
- ... (20 items × 2 direcciones)

#### Variables de Cambio de Tiempo (40 columnas)

- `CT_Item_3_Izq`, `CT_Item_3_Der`
- `CT_Item_4_Izq`, `CT_Item_4_Der`
- ... (20 items × 2 direcciones)

#### Variables de Congruencia (2 columnas)

- `CO_Congruentes_Promedio`
- `CO_Incongruentes_Promedio`

### Total

**~150 variables generadas** desde datos crudos hasta análisis final.

---

## FLUJO COMPLETO RESUMIDO

```
DATOS CRUDOS (CSV)
    ↓
[1] Combinar archivos
    ↓
DATAFRAME UNIFICADO
    ↓
[2] Procesar JSON → Expandir columnas
    ↓
DATAFRAME CON IP_ITEMS
    ↓
[3] Calcular índices ideológicos
    ↓
DATAFRAME CON ÍNDICES
    ↓
[4] Crear variables CO y CT
    ↓
DATAFRAME CON CAMBIOS
    ↓
[4b] Calcular CO_Congruentes/Incongruentes
    ↓
DATAFRAME CON CONGRUENCIA
    ↓
[5] Eliminar outliers
    ↓
DATAFRAME LIMPIO
    ↓
[6] Tests Mann-Whitney → Resultados estadísticos
[7] Modelos SEM → Coeficientes y R²
[8] Modelos Robustos → Predictores significativos
    ↓
[9] Generar visualizaciones
    ↓
[10] Exportar tablas y gráficos
    ↓
RESULTADOS FINALES
```

---

## EJECUCIÓN DEL PIPELINE COMPLETO

### Opción 1: Script Automatizado

```bash
cd Tesis_Ordenada/Scripts
python Ejecutar_Pipeline_Completo.py
```

### Opción 2: Notebook Interactivo

```bash
cd Tesis_Ordenada/Notebooks
jupyter notebook Pipeline_Principal.ipynb
```

### Opción 3: Paso a Paso (Python)

```python
# ============================================================
# PIPELINE COMPLETO EN PYTHON
# ============================================================

import sys
from pathlib import Path

# Agregar rutas.
Ruta_Base = Path.cwd().parent
sys.path.append(str(Ruta_Base / "Codigo" / "Utilidades"))
sys.path.append(str(Ruta_Base / "Codigo" / "Procesamiento"))
sys.path.append(str(Ruta_Base / "Codigo" / "Test_Estadisticos"))
sys.path.append(str(Ruta_Base / "Codigo" / "Modelado_Estadistico"))

# Importar módulos.
from Configuracion import Crear_Carpetas_Salida
from Construccion_Bases import (
    Combinar_Archivos_Generales,
    Combinar_Archivos_Ballotage,
    Procesar_Base_Completa
)
from Calculo_Indices import Calcular_Todos_Indices
from Calculo_Variables_Cambio import Calcular_Variables_Cambio
from Funciones_Comunes import (
    Eliminar_Filas_Por_Desviacion_Estandar
)
from Mann_Whitney import Ejecutar_Mann_Whitney
from Modelos_SEM import Ejecutar_Modelo_SEM_Simple
from Modelos_Robustos import Modelo_Lineal_Robusto

# Paso 0: Crear carpetas.
Crear_Carpetas_Salida()

# Paso 1: Construcción.
print("Paso 1: Construcción de bases...")
Df_Generales = Procesar_Base_Completa(
    Combinar_Archivos_Generales()
)
Df_Ballotage = Procesar_Base_Completa(
    Combinar_Archivos_Ballotage()
)

# Paso 3: Índices.
print("Paso 3: Cálculo de índices...")
Df_Generales = Calcular_Todos_Indices(Df_Generales)
Df_Ballotage = Calcular_Todos_Indices(Df_Ballotage)

# Paso 4: Variables de cambio.
print("Paso 4: Variables de cambio...")
Diccionario_Dfs = {
    'Generales': Df_Generales,
    'Ballotage': Df_Ballotage
}
Diccionario_Dfs = Calcular_Variables_Cambio(Diccionario_Dfs)
Df_Generales = Diccionario_Dfs['Generales']
Df_Ballotage = Diccionario_Dfs['Ballotage']

# Paso 5: Limpieza.
print("Paso 5: Eliminación de outliers...")
Columnas_CO = [col for col in Df_Generales.columns
               if col.startswith('CO_')]
Df_Generales = Eliminar_Filas_Por_Desviacion_Estandar(
    Df_Generales, Columnas_CO, 3
)
Df_Ballotage = Eliminar_Filas_Por_Desviacion_Estandar(
    Df_Ballotage, Columnas_CO, 3
)

# Paso 6: Tests Mann-Whitney.
print("Paso 6: Tests estadísticos...")
Resultado_Test = Ejecutar_Mann_Whitney(
    Df_Generales,
    'CO_Item_3_Izq',
    ['Left_Wing', 'Progressivism'],
    ['Right_Wing_Libertarian']
)
print(f"P-valor: {Resultado_Test['P_Valor']:.4f}")

# Paso 7: Modelos SEM.
print("Paso 7: Modelos SEM...")
Resultado_SEM = Ejecutar_Modelo_SEM_Simple(
    Df_Generales,
    'Indice_Progresismo',
    'CO_Item_3_Izq'
)
print(f"Coeficiente: {Resultado_SEM['Coeficiente']:.3f}")

# Paso 10: Exportar.
print("Paso 10: Exportando resultados...")
Df_Generales.to_excel(
    'Tablas/Bases_Procesadas/Base_Generales_Procesada.xlsx',
    index=False
)
Df_Ballotage.to_excel(
    'Tablas/Bases_Procesadas/Base_Ballotage_Procesada.xlsx',
    index=False
)

print("✓ Pipeline completado exitosamente.")
```

---

## DOCUMENTOS GENERADOS

### Tablas

1. **Base_Generales_Procesada.xlsx**: DataFrame completo Generales.
2. **Base_Ballotage_Procesada.xlsx**: DataFrame completo Ballotage.
3. **Resultados_Mann_Whitney.xlsx**: Tabla con todos los tests.
4. **Resultados_SEM.xlsx**: Tabla con coeficientes de modelos SEM.
5. **Resultados_Modelos_Robustos_Generales.xlsx**: Matriz de modelos robustos.
6. **Resultados_Modelos_Robustos_Ballotage.xlsx**: Matriz de modelos robustos.

### Gráficos

1. **Cleveland_CO_Congruente_vs_Incongruente_Generales.png/.svg**
2. **Cleveland_CO_Congruente_vs_Incongruente_Ballotage.png/.svg**
3. **Heatmap_Correlaciones_Indices_CO.png/.svg**
4. **Violin_CO_Por_Categoria.png/.svg**
5. **Barras_Comparacion_Grupos.png/.svg**

---

## PREGUNTAS FRECUENTES

### ¿Se calculan todas las variables CO y CT?

**Sí**. Para cada uno de los 20 items IP, se calculan:
- `CO_Item_N_Izq`: Cambio asociado a candidato izquierda.
- `CO_Item_N_Der`: Cambio asociado a candidato derecha.
- `CT_Item_N_Izq`: Cambio de tiempo con candidato izquierda.
- `CT_Item_N_Der`: Cambio de tiempo con candidato derecha.

**Total**: 40 variables CO + 40 variables CT = **80 variables de cambio**.

### ¿Las variables CO/CT son individuales o promedios?

**Individuales**. Cada `CO_Item_N_Izq` es el cambio para ese item específico.

**Promedios agregados**: Las variables `CO_Congruentes_Promedio` y `CO_Incongruentes_Promedio` SÍ son promedios calculados a partir de las variables individuales.

### ¿Dónde se calculan CO_Congruentes y CO_Incongruentes?

En el archivo `Codigo/Procesamiento/Calculo_Variables_Cambio.py`, función `Calcular_CO_Congruentes_E_Incongruentes()`.

Esta función clasifica cada variable CO individual según:
- **Tipo de item** (progresista o conservador).
- **Dirección política del candidato** (izquierda o derecha).
- **Categoría ideológica del participante** (izquierda o derecha).

Luego promedia las variables congruentes e incongruentes.

### ¿Están incluidos los modelos robustos?

**Sí**. El módulo `Codigo/Modelado_Estadistico/Modelos_Robustos.py` contiene toda la implementación de los modelos robustos con:
- Eliminación secuencial de variables.
- Detección de multicolinealidad (VIF).
- Detección de outliers influyentes.
- Errores estándar robustos (HC3).
- Diagnósticos completos.

Migrado desde los notebooks `6. Modelo robusto.ipynb` y `7. Evaluación del modelo robusto.ipynb`.

### ¿Se hacen TODOS los gráficos y cálculos de los notebooks originales?

Los módulos en `Tesis_Ordenada/Codigo/` contienen TODAS las funciones necesarias para replicar los análisis de los 70+ notebooks originales. Sin embargo, algunos análisis específicos pueden requerir scripts adicionales o personalización de parámetros.

El pipeline actual implementa:
- ✅ Construcción de bases.
- ✅ Cálculo de índices.
- ✅ Variables de cambio (CO/CT).
- ✅ Variables de congruencia.
- ✅ Tests Mann-Whitney.
- ✅ Modelos SEM.
- ✅ Modelos robustos.
- ✅ Gráficos de Cleveland.
- ⚠️ Otros gráficos (heatmaps, violín) requieren implementación adicional.

---

## CONTACTO Y SOPORTE

Para dudas o problemas con el pipeline, consultar:
- **README.md**: Documentación general del proyecto.
- **CLAUDE.md**: Instrucciones para Claude Code.
- **Notebooks/Pipeline_Principal.ipynb**: Ejemplo interactivo.

---

**Última actualización**: 2025-01-04
**Versión del pipeline**: 1.0
