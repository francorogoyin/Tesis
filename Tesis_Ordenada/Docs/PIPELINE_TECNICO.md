# PIPELINE TÉCNICO COMPLETO DE PROCESAMIENTO Y ANÁLISIS

Este documento describe **TODO** el flujo técnico de procesamiento y análisis del experimento de personalidad implícita y política en las elecciones argentinas 2023, desde los datos crudos hasta los resultados finales.

---

## ÍNDICE

1. [Objetivo del Experimento](#objetivo-del-experimento)
2. [Datos de Entrada](#datos-de-entrada)
3. [Fase 1: Preprocesamiento de Datos (Pasos 1-10)](#fase-1-preprocesamiento-de-datos)
4. [Fase 2: Sistema de Control de Calidad](#fase-2-sistema-de-control-de-calidad)
5. [Fase 3: Análisis Estadístico (Pasos 11-14)](#fase-3-análisis-estadístico)
6. [Fase 4: Visualizaciones (Paso 15)](#fase-4-visualizaciones)
7. [Fase 5: Exportación de Resultados (Paso 16)](#fase-5-exportación-de-resultados)
8. [Resumen de Variables Generadas](#resumen-de-variables-generadas)
9. [Preguntas Frecuentes](#preguntas-frecuentes)

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

## FASE 1: PREPROCESAMIENTO DE DATOS

### PASO 1: CONSTRUCCIÓN DE BASES DE DATOS

**Módulo**: `Codigo/Procesamiento/Construccion_Bases.py`

**Funciones**:

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

**Salida**:
- **Df_Generales_Crudo**: DataFrame crudo con datos de Generales.
- **Df_Ballotage_Crudo**: DataFrame crudo con datos de Ballotage.

**Verificación**: Control_01_Construccion_Bases.py

---

### PASO 2: PROCESAMIENTO DE COLUMNA JSON

**Módulo**: `Codigo/Procesamiento/Construccion_Bases.py` (función `Procesar_Base_Completa`)

**Proceso**:

1. **Aplanar diccionario JSON**: Convierte el diccionario anidado en columnas individuales.
2. **Rellenar items faltantes**: Items no presentados se marcan como NaN.
3. **Crear variables de orden**: Para items progresistas/conservadores.

**Funciones Auxiliares** (en `Funciones_Comunes.py`):

#### `Aplanar_Diccionario(Diccionario, Prefijo)`

Convierte diccionario anidado en claves planas:
- `{'IP_Item_3': {'Respuesta': 5}}` → `'IP_Item_3_Respuesta': 5`

#### `Rellenar_IP_Items_Asociados_Faltantes(Df)`

Rellena con NaN los items no presentados (diseño contrabalanceado).

**Uso**:

```python
from Construccion_Bases import Procesar_Base_Completa

Df_Generales = Procesar_Base_Completa(Df_Generales_Crudo)
Df_Ballotage = Procesar_Base_Completa(Df_Ballotage_Crudo)
```

**Salida**: DataFrames con columnas expandidas (60 columnas por 20 items).

---

### PASO 3: CÁLCULO DE ÍNDICES IDEOLÓGICOS

**Módulo**: `Codigo/Procesamiento/Calculo_Indices.py`

**Índices Calculados**:

#### 1. Índice de Progresismo

**Fórmula**: Promedio de respuestas a items progresistas (3, 4, 5, 6, 7, 9, 10, 16, 22, 24).

**Rango**: 1-5 (mayor = más progresista).

#### 2. Índice de Conservadurismo

**Fórmula**: Promedio de respuestas a items conservadores (8, 11, 19, 20, 23, 25, 27, 28, 29, 30).

**Rango**: 1-5 (mayor = más conservador).

#### 3. Índice de Positividad

**Fórmula**: Promedio de TODOS los 20 items IP.

**Interpretación**: Tendencia general a estar de acuerdo.

#### 4. Índices de Tiempo

- `Indice_Progresismo_Tiempo`: Promedio de tiempos en items progresistas.
- `Indice_Conservadurismo_Tiempo`: Promedio de tiempos en items conservadores.

**Función Consolidada**:

```python
from Calculo_Indices import Calcular_Todos_Indices

Df = Calcular_Todos_Indices(Df)
# Agrega 5 columnas de índices
```

**Verificación**: Control_02_Calculo_Indices.py

---

### PASO 4: CREACIÓN DE VARIABLES DE CAMBIO

**Módulo**: `Codigo/Procesamiento/Calculo_Variables_Cambio.py`

**Variables Calculadas**:

#### 1. Cambio de Opinión (CO)

**Fórmula**: CO = Respuesta_Asociada - Respuesta_Base

- `CO_Item_N_Izq`: Cambio con candidato izquierda.
- `CO_Item_N_Der`: Cambio con candidato derecha.

**Rango**: -4 a +4
- **Positivo**: Aumentó acuerdo.
- **Negativo**: Disminuyó acuerdo.
- **Cero**: Sin cambio.

#### 2. Cambio de Tiempo (CT)

**Fórmula**: CT = Tiempo_Asociado - Tiempo_Base

- `CT_Item_N_Izq`, `CT_Item_N_Der`

**Interpretación**:
- **Positivo**: Tardó más (posible conflicto cognitivo).
- **Negativo**: Tardó menos (mayor fluidez).

**Uso**:

```python
from Calculo_Variables_Cambio import Calcular_Variables_Cambio

Diccionario_Dfs = {
    'Generales': Df_Generales,
    'Ballotage': Df_Ballotage
}

Diccionario_Dfs = Calcular_Variables_Cambio(Diccionario_Dfs)
```

**Salida**: 80 columnas (40 CO + 40 CT).

**Verificación**: Control_03_Variables_Cambio.py

---

### PASO 5: LIMPIEZA DE DATOS

**Módulo**: `Codigo/Procesamiento/Limpieza_Datos.py`

**Criterios de Limpieza**:

#### 1. Filtrado por Categoría Ideológica

Elimina participantes con categorías inválidas:
- `'Other'`, `'No apply'`, `'No response'`, `'Blank'`

**Razón**: Distorsionan análisis comparativos.

#### 2. Filtrado por Outliers de Tiempo

Elimina participantes con tiempos extremos:
- Criterio: Media + (3 × Desviación_Estándar)
- Calculado sobre TODOS los tiempos
- Elimina fila COMPLETA si CUALQUIER tiempo excede umbral

**Razón**: Falta de atención o problemas técnicos.

**Funciones**:

```python
from Limpieza_Datos import Limpiar_Datos_Completo

Df_Limpio = Limpiar_Datos_Completo(
    Df,
    Filtrar_Categorias=True,
    Filtrar_Tiempos=True,
    Numero_Desviaciones=3
)
```

**Impacto Típico**: 3-8% de datos eliminados.

**Verificación**: Control_04_Limpieza_Datos.py

---

### PASO 6: RELLENO DE MEDIANAS

**Módulo**: `Codigo/Procesamiento/Relleno_Medianas.py`

**Objetivo**: Rellenar valores faltantes en variables CO/CT con medianas calculadas por categoría ideológica.

**Proceso**:

1. **Identificar NaN**: En variables CO y CT.
2. **Calcular medianas**: Por categoría ideológica para cada variable.
3. **Rellenar NaN**: Con mediana correspondiente.
4. **Backup**: Crear columnas `_Original` con valores pre-relleno.

**Funciones**:

```python
from Relleno_Medianas import Rellenar_Con_Medianas_Por_Categoria

Df = Rellenar_Con_Medianas_Por_Categoria(
    Df,
    Columna_Categoria='Categoria_PASO_2023'
)
```

**Verificación**: Control_05_Relleno_Medianas.py

---

### PASO 7: PROCESAMIENTO DE REDES Y MEDIOS

**Módulo**: `Codigo/Procesamiento/Procesar_Redes_Y_Medios.py`

**Objetivo**: Convertir columnas de texto con múltiples valores en columnas binarias (0/1).

**Redes Sociales Procesadas**:
- Twitter, Facebook, Instagram, Threads, Tiktok, Youtube, Whatsapp, Telegram

**Medios de Prensa Procesados**:
- 13 medios argentinos (Clarín, La Nación, Página/12, etc.)

**Proceso**:

1. **Parsear texto**: Separar por comas.
2. **Crear columnas binarias**: `Red_Social_Twitter`, `Medios_Prensa_Clarin`, etc.
3. **Codificar**: 1 si presente, 0 si ausente.

**Funciones**:

```python
from Procesar_Redes_Y_Medios import (
    Procesar_Redes_Sociales,
    Procesar_Medios_Prensa
)

Df = Procesar_Redes_Sociales(Df)
Df = Procesar_Medios_Prensa(Df)
```

**Verificación**: Control_06_Redes_Y_Medios.py

---

### PASO 8: AGRUPAMIENTO DE VARIABLES

**Módulo**: `Codigo/Procesamiento/Agrupamiento_Variables.py`

**Objetivo**: Crear versiones agrupadas de variables categóricas para reducir dispersión.

**Variables Agrupadas**:

#### 1. Edad_Agrupada

- `18-25`, `26-35`, `36-45`, `46-55`, `56-65`, `66+`

#### 2. Region

- Mapeo de provincias → regiones (NOA, NEA, Centro, Cuyo, Patagonia, AMBA)

#### 3. Nivel_Educativo_Agrupado

- Primario, Secundario, Terciario, Universitario, Posgrado

**Funciones**:

```python
from Agrupamiento_Variables import (
    Agrupar_Edad,
    Mapear_Provincia_A_Region,
    Agrupar_Nivel_Educativo
)

Df['Edad_Agrupada'] = Agrupar_Edad(Df['Edad'])
Df['Region'] = Mapear_Provincia_A_Region(Df['Provincia'])
```

**Verificación**: Control_07_Agrupamientos.py

---

### PASO 9: CREACIÓN DE VARIABLES DUMMY

**Módulo**: `Codigo/Procesamiento/Crear_Variables_Dummy.py`

**Objetivo**: Convertir variables categóricas en dummies para modelado estadístico.

**Variables Dummy Creadas**:

- `Sexo_Masculino`, `Sexo_Femenino`
- `Nivel_Educativo_Primario`, `Nivel_Educativo_Secundario`, etc.
- `Region_NOA`, `Region_NEA`, etc.
- `Edad_Agrupada_18_25`, `Edad_Agrupada_26_35`, etc.

**Criterio**: Se crean n-1 dummies para evitar multicolinealidad.

**Funciones**:

```python
from Crear_Variables_Dummy import Crear_Todas_Variables_Dummy

Df = Crear_Todas_Variables_Dummy(Df)
```

**Verificación**: Control_08_Variables_Dummy.py

---

### PASO 10: ORDENAMIENTO DE COLUMNAS

**Módulo**: `Codigo/Procesamiento/Ordenamiento_Columnas.py`

**Objetivo**: Organizar columnas en orden temático para facilitar navegación.

**Orden Implementado**:

1. **ID** (primera columna)
2. **Demográficas**: Edad, Sexo, Región, etc.
3. **Índices**: Indice_Progresismo, Indice_Conservadurismo, etc.
4. **Variables CO**: Todas juntas
5. **Variables CT**: Todas juntas
6. **Redes sociales**: Todas juntas
7. **Medios de prensa**: Todas juntas
8. **Variables dummy**: Todas juntas

**Funciones**:

```python
from Ordenamiento_Columnas import Ordenar_Columnas_Por_Tematica

Df = Ordenar_Columnas_Por_Tematica(Df)
```

**Verificación**: Control_09_Ordenamiento.py

---

### PASO 11: AGREGACIÓN DE CLUSTERS

**Módulo**: `Codigo/Procesamiento/Agregar_Clusters.py`

**Objetivo**: Incorporar resultados de clustering (Kmeans, Jerárquico, DBSCAN) a la base final.

**Clusters Agregados**:

- `Cluster_Kmeans`: Asignación de K-means
- `Cluster_Jerarquico`: Asignación de clustering jerárquico
- `Cluster_DBSCAN`: Asignación de DBSCAN (incluye outliers como -1)

**Proceso**:

1. **Cargar resultados** de clustering desde archivos separados.
2. **Merge por ID** con base principal.
3. **Validar**: Sin duplicados, sin NaN.

**Funciones**:

```python
from Agregar_Clusters import Agregar_Clusters_A_Base

Df = Agregar_Clusters_A_Base(
    Df,
    Ruta_Clusters='Data/Resultados_Clustering/'
)
```

**Verificación**: Control_10_Clusters.py

---

## FASE 2: SISTEMA DE CONTROL DE CALIDAD

El sistema de control verifica exhaustivamente cada paso del preprocesamiento con **16 scripts de control** que generan reportes PDF detallados.

**Ubicación**: `Codigo/Control/`

**Filosofía**:
- **Zero tolerance**: Cualquier desviación se reporta
- **Verificación exhaustiva**: Fila por fila, columna por columna
- **Trazabilidad completa**: Cada problema reporta ID y columna exacta
- **Reportes PDF**: Todos los controles generan reportes descriptivos

**Controles Implementados**:

| Control | Verificación | Paso Asociado |
|---------|-------------|---------------|
| **01** | IDs únicos, columnas críticas, tipos de datos | Paso 1 |
| **02** | Índices en rangos válidos, sin NaN | Paso 3 |
| **03** | Variables CO/CT en rangos [-4,+4] y [≥0] | Paso 4 |
| **04** | Pérdida de datos <20%, sin duplicados | Paso 5 |
| **05** | Todos los NaN rellenados, backups creados | Paso 6 |
| **06** | Columnas binarias (0/1), coherencia con texto | Paso 7 |
| **07** | Mapeos completos, valores "Otro" <30% | Paso 8 |
| **08** | Suma por fila = 1, coherencia con original | Paso 9 |
| **09** | ID primera, agrupación temática, prefijos | Paso 10 |
| **10** | Merge exitoso, distribución balanceada | Paso 11 |
| **11** | P-values [0,1], tamaños suficientes | Análisis |
| **12** | Clasificación congruente/incongruente | Análisis |
| **13** | Matriz simétrica, diagonal = 1 | Análisis |
| **14** | Coeficientes razonables, R² [0,1] | Análisis |
| **15** | Reproducibilidad 100% vs bases originales | Final |
| **16** | Script maestro - ejecuta todos los controles | Maestro |

**Ejecutar Todos los Controles**:

```bash
cd Codigo/Control
python Control_16_Ejecutar_Todos.py
```

**Reportes Generados**: `Reportes/Control/Control_Consolidado_YYYYMMDD_HHMMSS.pdf`

Ver `Docs/GUIA_CONTROLES.md` para documentación completa del sistema de control.

---

## FASE 3: ANÁLISIS ESTADÍSTICO

### PASO 12: TESTS MANN-WHITNEY

**Módulo**: `Codigo/Test_Estadisticos/Mann_Whitney.py`

**Objetivo**: Comparar distribuciones de variables CO/CT entre grupos ideológicos.

**Función Principal**: `Ejecutar_Mann_Whitney(Df, Variable, Grupos_A, Grupos_B)`

**Proceso**:

1. Filtrar datos de Grupos_A y Grupos_B
2. Test U de Mann-Whitney (comparación no paramétrica)
3. Calcular tamaño del efecto: r = Z / √N
4. Determinar significancia: p < 0.05

**Uso**:

```python
from Mann_Whitney import Ejecutar_Mann_Whitney

Resultado = Ejecutar_Mann_Whitney(
    Df_Generales,
    'CO_Item_3_Izq',
    ['Left_Wing', 'Progressivism'],
    ['Right_Wing_Libertarian']
)
```

**Salida**: Diccionario con U, P_Valor, Significativo, Tamaño_Efecto, Medianas.

**Verificación**: Control_11_Tests_Mann_Whitney.py

---

### PASO 13: ANÁLISIS DE CONGRUENCIA IDEOLÓGICA

**Módulo**: `Codigo/Test_Estadisticos/Congruencia_Ideologica.py`

**Objetivo**: Comparar cambios congruentes vs incongruentes con ideología participante.

**Variables de Congruencia**:

- **CO_Congruentes_Promedio**: Promedio de cambios congruentes
  - Participante izquierda + Item progresista + Candidato izquierda
  - Participante derecha + Item conservador + Candidato derecha

- **CO_Incongruentes_Promedio**: Promedio de cambios incongruentes
  - Participante izquierda + Item progresista + Candidato derecha
  - Participante derecha + Item conservador + Candidato izquierda

**Candidatos**:
- **Izquierda**: Bregman, Solano
- **Derecha**: Milei, Bullrich

**Uso**:

```python
from Congruencia_Ideologica import (
    Analizar_Congruencia_Por_Candidato
)

Resultados = Analizar_Congruencia_Por_Candidato(
    Df_Generales,
    Lista_Candidatos=['Milei', 'Bullrich', 'Bregman']
)
```

**Verificación**: Control_12_Congruencia_Ideologica.py

---

### PASO 14: CORRELACIONES

**Módulo**: `Codigo/Modelado_Estadistico/Correlaciones.py`

**Objetivo**: Calcular correlaciones de Spearman entre índices y variables CO/CT.

**Función Principal**: `Calcular_Matriz_Correlaciones_Spearman(Df, Variables)`

**Proceso**:

1. Seleccionar variables de interés
2. Calcular correlación de Spearman (no paramétrica)
3. Calcular p-valores
4. Generar matriz de correlaciones

**Uso**:

```python
from Correlaciones import Calcular_Matriz_Correlaciones_Spearman

Variables_Analisis = [
    'Indice_Progresismo',
    'Indice_Conservadurismo',
    'CO_Item_3_Izq',
    'CO_Item_3_Der'
]

Matriz, P_Valores = Calcular_Matriz_Correlaciones_Spearman(
    Df_Generales,
    Variables_Analisis
)
```

**Verificación**: Control_13_Correlaciones.py

---

### PASO 15: MODELOS SEM

**Módulo**: `Codigo/Modelado_Estadistico/Modelos_SEM.py`

**Objetivo**: Modelar relaciones causales entre índices ideológicos y variables CO/CT.

**Función Principal**: `Ejecutar_Modelo_SEM_Simple(Df, Variable_Predictora, Variable_Outcome)`

**Proceso**:

1. Especificación del modelo: `Outcome ~ Predictor`
2. Ajuste del modelo usando `semopy`
3. Extracción de resultados: Coeficientes, p-valores, R²

**Uso**:

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

**Modelos Típicos**:
1. Progresismo → CO progresistas izquierda
2. Conservadurismo → CO conservadores derecha

**Verificación**: Control_14_Modelos_SEM.py

---

## FASE 4: VISUALIZACIONES

### PASO 16: GENERACIÓN DE GRÁFICOS

**Ubicación Módulos**: `Codigo/Visualizacion/`

**Tipos de Gráficos**:

#### 1. Gráficos de Cleveland (Dot Plots)

**Módulo**: `Graficos_Cleveland.py`

**Uso**:
```python
from Graficos_Cleveland import Crear_Cleveland_Comparativo

Crear_Cleveland_Comparativo(
    Df_Resultados,
    'Comparación CO Congruentes vs Incongruentes',
    'Cleveland_CO_Congruente_vs_Incongruente_Generales'
)
```

**Salida**: Puntos con líneas mostrando diferencias entre grupos.

#### 2. Heatmaps de Correlación

**Módulo**: `Heatmaps.py`

Matrices de correlación entre índices ideológicos y variables CO/CT.

#### 3. Gráficos de Violín

**Módulo**: `Graficos_Violin.py`

Distribuciones de variables CO por categoría ideológica.

#### 4. Gráficos de Barras

**Módulo**: `Graficos_Barras.py`

Comparaciones de medias entre grupos con barras de error.

#### 5. Boxplots

**Módulo**: `Graficos_Boxplot.py`

Distribuciones con cuartiles y outliers.

**Formatos de Exportación**:
- **PNG**: 300 DPI para documentos
- **SVG**: Vectorial para edición

**Ubicación de Salida**:
```
Tesis_Ordenada/Graficos/
├── Cleveland/
├── Heatmaps/
├── Violin/
├── Barras/
└── Boxplot/
```

---

## FASE 5: EXPORTACIÓN DE RESULTADOS

### Bases Procesadas

**Ubicación**: `Tesis_Ordenada/Data/Bases definitivas/`

```python
Df_Generales.to_excel(
    'Data/Bases definitivas/Bases finalesGenerales.xlsx',
    index=False
)
Df_Ballotage.to_excel(
    'Data/Bases definitivas/Bases finalesBallotage.xlsx',
    index=False
)
```

### Resultados de Tests

**Ubicación**: `Tesis_Ordenada/Tablas/Resultados_Tests/`

Tablas Excel con resultados de Mann-Whitney para cada comparación.

### Resultados de Modelos

**Ubicación**: `Tesis_Ordenada/Tablas/Resultados_SEM/`

Tablas Excel con:
- Coeficientes β
- P-valores
- Métricas de ajuste (R², AIC, BIC)
- Variables significativas por modelo

**Formato**: Matriz con variables independientes en filas, variables dependientes en columnas, celdas coloreadas por significancia (verde = p < 0.05, gris = no significativo).

---

## RESUMEN DE VARIABLES GENERADAS

### Datos Crudos → Variables Procesadas

| Etapa | Variables de Entrada | Variables de Salida | Cantidad |
|-------|---------------------|---------------------|----------|
| **1. Construcción** | CSV crudos (7 archivos) | Df unificado | 2 DataFrames |
| **2. JSON** | Columna JSON anidada | IP_Item_N_Respuesta/Tiempo/Candidato | 60 columnas |
| **3. Índices** | Respuestas IP items | Índices ideológicos | 5 columnas |
| **4. Cambio** | Respuestas base vs asociadas | CO/CT por item y dirección | 80 columnas |
| **5. Limpieza** | DataFrame completo | DataFrame sin outliers | - |
| **6. Medianas** | Variables con NaN | Variables rellenadas | - |
| **7. Redes/Medios** | Texto multi-valor | Columnas binarias | ~20 columnas |
| **8. Agrupamientos** | Variables originales | Variables agrupadas | ~5 columnas |
| **9. Dummies** | Variables categóricas | Variables dummy binarias | ~30 columnas |
| **10. Ordenamiento** | Columnas desordenadas | Columnas ordenadas | - |
| **11. Clusters** | Archivos externos | Columnas de cluster | 3 columnas |

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
[5] Eliminar outliers
    ↓
[6] Rellenar medianas
    ↓
[7] Procesar redes y medios
    ↓
[8] Agrupar variables
    ↓
[9] Crear variables dummy
    ↓
[10] Ordenar columnas
    ↓
[11] Agregar clusters
    ↓
DATAFRAME PREPROCESADO COMPLETO
    ↓
[CONTROL] Verificar con 16 controles
    ↓
[12] Tests Mann-Whitney → Resultados estadísticos
[13] Análisis de congruencia
[14] Correlaciones de Spearman
[15] Modelos SEM → Coeficientes y R²
    ↓
[16] Generar visualizaciones
    ↓
[17] Exportar tablas y gráficos
    ↓
RESULTADOS FINALES
```

---

## EJECUCIÓN DEL PIPELINE COMPLETO

### Opción 1: Script Automatizado (Recomendado)

```bash
cd Tesis_Ordenada
python Ejecutar_Pipeline_Completo.py
```

Este script ejecuta automáticamente:
- Los 11 pasos de preprocesamiento
- Los 16 controles de calidad
- Generación de reportes PDF
- Exportación de bases finales

### Opción 2: Notebook Interactivo

```bash
cd Tesis_Ordenada/Notebooks
jupyter notebook Pipeline_Principal.ipynb
```

### Opción 3: Paso a Paso (Python)

Ver sección completa en README.md principal.

---

## PREGUNTAS FRECUENTES

### ¿Se calculan todas las variables CO y CT?

**Sí**. Para cada uno de los 20 items IP, se calculan:
- `CO_Item_N_Izq`: Cambio asociado a candidato izquierda
- `CO_Item_N_Der`: Cambio asociado a candidato derecha
- `CT_Item_N_Izq`: Cambio de tiempo con candidato izquierda
- `CT_Item_N_Der`: Cambio de tiempo con candidato derecha

**Total**: 40 variables CO + 40 variables CT = **80 variables de cambio**.

### ¿Las variables CO/CT son individuales o promedios?

**Individuales**. Cada `CO_Item_N_Izq` es el cambio para ese item específico.

**Promedios agregados**: Las variables `CO_Congruentes_Promedio` y `CO_Incongruentes_Promedio` SÍ son promedios calculados a partir de las variables individuales.

### ¿Dónde se calculan CO_Congruentes y CO_Incongruentes?

En el archivo `Codigo/Procesamiento/Calculo_Variables_Cambio.py`, función `Calcular_CO_Congruentes_E_Incongruentes()`.

Esta función clasifica cada variable CO individual según:
- **Tipo de item** (progresista o conservador)
- **Dirección política del candidato** (izquierda o derecha)
- **Categoría ideológica del participante** (izquierda o derecha)

Luego promedia las variables congruentes e incongruentes.

### ¿Qué pasa si un control falla?

1. Revisar reporte PDF del control específico en `Reportes/Control/`
2. Identificar ID de sujeto y columna problemática
3. Verificar en el código de procesamiento correspondiente
4. Corregir error
5. Re-ejecutar control o pipeline completo

### ¿Cuánto tiempo tarda el pipeline completo?

**Aproximadamente**:
- Preprocesamiento (Pasos 1-11): 5-10 minutos
- Controles (16 scripts): 3-5 minutos
- Análisis estadístico: 10-20 minutos (depende de número de modelos)
- Visualizaciones: 2-5 minutos

**Total**: 20-40 minutos para ejecución completa.

### ¿Los resultados son reproducibles?

**Sí, 100%**. El Control_15_Identidad_Bases.py verifica que las bases procesadas sean idénticas (hasta tolerancia de 1e-10) a las bases originales del proyecto.

Esto garantiza reproducibilidad completa del pipeline.

---

## CONTACTO Y SOPORTE

Para dudas o problemas con el pipeline, consultar:
- **README.md**: Documentación general del proyecto
- **GUIA_CONTROLES.md**: Sistema de control de calidad
- **API_REFERENCIA.md**: Documentación de funciones
- **CLAUDE.md**: Instrucciones para Claude Code

---

**Última actualización**: 2025-01-10
**Versión del pipeline**: 2.0
