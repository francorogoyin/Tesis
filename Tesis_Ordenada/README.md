# Tesis: Personalidad Implícita y Cambio de Opinión Política

**Análisis experimental del efecto de candidatos políticos en cambios de opinión y tiempos de respuesta durante las elecciones argentinas 2023**

---

## 🎯 ¿Qué es este proyecto?

Este repositorio contiene el **pipeline completo** de procesamiento, análisis estadístico y visualización de datos de un experimento de psicología política realizado durante las elecciones argentinas de 2023 (Generales y Ballotage).

### Pregunta de Investigación

**¿Cómo influye la ideología política en los cambios de opinión (CO) y tiempos de respuesta (CT) cuando se asocian proposiciones ideológicas con candidatos políticos específicos?**

### Diseño Experimental

1. **Fase Base**: Participantes evalúan 20 proposiciones ideológicas (10 progresistas, 10 conservadoras) en escala 1-5
2. **Fase Asociada**: Mismas proposiciones presentadas asociadas a candidatos políticos (izquierda o derecha)
3. **Medición de Cambios**:
   - **CO** (Cambio de Opinión) = Respuesta_Asociada - Respuesta_Base
   - **CT** (Cambio de Tiempo) = Tiempo_Asociado - Tiempo_Base

### Hipótesis Principal

Los participantes mostrarán **mayor cambio de opinión hacia candidatos congruentes** con su ideología:
- Progresistas → Candidatos de izquierda en ítems progresistas
- Conservadores → Candidatos de derecha en ítems conservadores

---

## 📊 Datos del Estudio

- **Participantes Generales**: ~2786 casos
- **Participantes Ballotage**: ~1254 casos
- **Proposiciones evaluadas**: 20 ítems IP (10 progresistas + 10 conservadores)
- **Candidatos analizados**: 8 candidatos de espectro izquierda-derecha
- **Variables generadas**: ~150 variables desde datos crudos hasta análisis final

### Categorías Ideológicas

- Left_Wing (Bregman, Solano)
- Progressivism (Massa, Grabois)
- Centre (Schiaretti)
- Moderate_Right_A (Rodríguez Larreta)
- Moderate_Right_B (Bullrich)
- Right_Wing_Libertarian (Milei)

---

## 🏗️ Estructura del Proyecto

```
Tesis_Ordenada/
├── README.md                          # Este archivo - Guía principal
├── Ejecutar_Pipeline_Completo.py     # Script maestro - ejecuta todo el pipeline
├── CLAUDE.md                          # Instrucciones para Claude Code
│
├── Docs/                              # Documentación técnica detallada
│   ├── PIPELINE_TECNICO.md           # Especificación técnica completa del pipeline
│   ├── GUIA_CONTROLES.md             # Documentación del sistema de control de calidad
│   └── API_REFERENCIA.md             # Referencia de funciones y módulos
│
├── Codigo/                            # Todo el código fuente organizado por función
│   ├── Utilidades/                   # Funciones compartidas y configuración
│   │   ├── Configuracion.py         # Constantes y rutas globales
│   │   ├── Funciones_Comunes.py     # Utilidades reutilizables
│   │   └── Exportar_Resultados.py   # Funciones de exportación
│   │
│   ├── Procesamiento/                # Pipeline de transformación de datos
│   │   ├── Construccion_Bases.py    # Paso 1: Construcción desde CSVs
│   │   ├── Calculo_Indices.py       # Paso 2: Índices ideológicos
│   │   ├── Calculo_Variables_Cambio.py  # Paso 3: Variables CO y CT
│   │   ├── Limpieza_Datos.py        # Paso 4: Outliers y filtros
│   │   ├── Relleno_Medianas.py      # Paso 5: Imputación de NaN
│   │   ├── Procesar_Redes_Y_Medios.py   # Paso 6: Binarización
│   │   ├── Agrupamiento_Variables.py    # Paso 7: Categorización
│   │   ├── Crear_Variables_Dummy.py     # Paso 8: One-hot encoding
│   │   ├── Ordenamiento_Columnas.py     # Paso 9: Organización
│   │   └── Agregar_Clusters.py          # Paso 10: Clustering
│   │
│   ├── Test_Estadisticos/            # Análisis estadísticos
│   │   ├── Mann_Whitney.py           # Tests no paramétricos
│   │   ├── Tests_Adicionales.py      # Tests complementarios
│   │   └── Analisis_Correlacion.py   # Correlaciones Spearman
│   │
│   ├── Modelado_Estadistico/         # Modelos predictivos
│   │   ├── Modelos_SEM.py            # Ecuaciones estructurales
│   │   └── Modelos_Robustos.py       # Regresiones robustas con VIF
│   │
│   ├── Visualizacion/                # Generación de gráficos
│   │   ├── Graficos_Cleveland.py     # Dot plots comparativos
│   │   ├── Graficos_Barras.py        # Gráficos de barras
│   │   ├── Graficos_Boxplot.py       # Boxplots por categoría
│   │   ├── Graficos_Violin.py        # Distribuciones de violín
│   │   └── Graficos_Heatmap.py       # Matrices de correlación
│   │
│   └── Control/                       # Sistema de control de calidad (16 controles)
│       ├── Control_01_Construccion_Bases.py
│       ├── Control_02_Calculo_Indices.py
│       ├── Control_03_Variables_Cambio.py
│       ├── Control_04_Limpieza_Datos.py
│       ├── Control_05_Relleno_Medianas.py
│       ├── Control_06_Redes_Y_Medios.py
│       ├── Control_07_Agrupamientos.py
│       ├── Control_08_Variables_Dummy.py
│       ├── Control_09_Ordenamiento.py
│       ├── Control_10_Clusters.py
│       ├── Control_11_Tests_Mann_Whitney.py
│       ├── Control_12_Congruencia_Ideologica.py
│       ├── Control_13_Correlaciones.py
│       ├── Control_14_Modelos_SEM.py
│       ├── Control_15_Identidad_Bases.py
│       ├── Control_16_Ejecutar_Todos.py
│       └── README.md                 # Documentación de controles
│
├── Data/                              # Datos de entrada y procesados
│   ├── Datos_Crudos/                 # CSVs originales (7 archivos)
│   └── Bases_Definitivas/            # Bases finales procesadas
│
├── Tablas/                            # Resultados tabulares exportados
│   ├── Bases_Procesadas/             # DataFrames finales en Excel
│   ├── Resultados_Tests/             # Tablas de tests estadísticos
│   └── Resultados_SEM/               # Resultados de modelos SEM
│
├── Graficos/                          # Visualizaciones generadas
│   ├── Cleveland/                     # Dot plots comparativos
│   ├── Heatmaps/                     # Matrices de correlación
│   ├── Violin/                       # Gráficos de violín
│   └── Barras/                       # Gráficos de barras
│
├── Reportes/                          # Reportes de control de calidad
│   └── Control/                      # PDFs de verificación exhaustiva
│
└── Notebooks/                         # Notebooks interactivos Jupyter
    ├── Pipeline_Principal.ipynb      # Ejecución interactiva del pipeline
    └── Graficos/                     # Notebooks de experimentación gráfica
```

---

## 🚀 Inicio Rápido

### Requisitos Previos

```bash
# Python 3.9+
pip install pandas numpy scipy matplotlib seaborn openpyxl reportlab semopy statsmodels
```

### Ejecución del Pipeline Completo

**Opción 1: Script automatizado (recomendado)**

```bash
cd Tesis_Ordenada
python Ejecutar_Pipeline_Completo.py
```

Este script ejecuta **10 pasos** de procesamiento:
1. Construcción de bases desde CSVs
2. Cálculo de índices ideológicos
3. Creación de variables CO y CT
4. Limpieza de datos y outliers
5. Relleno de medianas por categoría
6. Procesamiento de redes sociales y medios
7. Agrupamiento de variables
8. Creación de variables dummy
9. Ordenamiento de columnas
10. Agregación de clusters

**Opción 2: Control de calidad exhaustivo**

```bash
cd Codigo/Control
python Control_16_Ejecutar_Todos.py
```

Ejecuta **16 controles exhaustivos** que verifican:
- ✅ Cada paso del procesamiento
- ✅ Cada fila y columna de datos
- ✅ Reproducibilidad 100%
- ✅ Genera reportes PDF detallados

**Opción 3: Notebook interactivo**

```bash
jupyter notebook Notebooks/Pipeline_Principal.ipynb
```

---

## 📝 Pipeline Completo de Procesamiento

### Fase 1: Preprocesamiento (Pasos 1-10)

```
DATOS CRUDOS (7 CSVs)
    ↓
[1] Construcción de bases → Combina archivos, procesa JSON anidado
    ↓
[2] Cálculo de índices → Progresismo, Conservadurismo, Positividad
    ↓
[3] Variables de cambio → CO (Cambio Opinión), CT (Cambio Tiempo)
    ↓
[4] Limpieza de datos → Elimina outliers (3 SD), categorías inválidas
    ↓
[5] Relleno de medianas → Imputa NaN por categoría ideológica
    ↓
[6] Redes y medios → Binariza redes sociales y medios de prensa
    ↓
[7] Agrupamientos → Provincia→Región, Edad→Grupos, etc.
    ↓
[8] Variables dummy → One-hot encoding de categóricas
    ↓
[9] Ordenamiento → Organiza columnas temáticamente
    ↓
[10] Clusters → Agrega variables de clustering K-means, Jerárquico, DBSCAN
    ↓
BASES PROCESADAS FINALES (Excel)
```

### Fase 2: Análisis Estadístico

```python
# Tests Mann-Whitney U
from Test_Estadisticos.Mann_Whitney import Ejecutar_Mann_Whitney

Resultado = Ejecutar_Mann_Whitney(
    Df_Generales,
    'CO_Item_3_Izq',
    ['Left_Wing', 'Progressivism'],
    ['Right_Wing_Libertarian']
)
# → P-valor, U-statistic, tamaño del efecto

# Modelos SEM
from Modelado_Estadistico.Modelos_SEM import Ejecutar_Modelo_SEM_Simple

Resultado = Ejecutar_Modelo_SEM_Simple(
    Df_Generales,
    'Indice_Progresismo',
    'CO_Item_3_Izq'
)
# → Coeficiente β, P-valor, R²

# Correlaciones Spearman
from Test_Estadisticos.Analisis_Correlacion import Calcular_Correlaciones

Matriz = Calcular_Correlaciones(Df_Generales, Variables_Interes)
# → Matriz de correlación con p-valores
```

### Fase 3: Visualizaciones

```python
# Gráficos de Cleveland
from Visualizacion.Graficos_Cleveland import Crear_Cleveland_Comparativo

Crear_Cleveland_Comparativo(
    Df_Resultados,
    'Comparación Congruente vs Incongruente',
    'Cleveland_Congruencia_Generales'
)

# Heatmaps de correlación
from Visualizacion.Graficos_Heatmap import Crear_Heatmap_Correlaciones

Crear_Heatmap_Correlaciones(
    Matriz_Correlaciones,
    'Heatmap_Indices_vs_CO'
)
```

---

## 🔬 Sistema de Control de Calidad

El sistema de control verifica **exhaustivamente** cada paso del procesamiento:

### Controles de Preprocesamiento (01-10)

| Control | Verificación | Crítico |
|---------|-------------|---------|
| **01** | IDs únicos, columnas críticas, tipos de datos | ✅ |
| **02** | Índices en rangos válidos, sin NaN, coherencia | ✅ |
| **03** | CO en [-4, +4], CT ≥ 0, coherencia con base | ✅ |
| **04** | Pérdida de datos < 20%, outliers eliminados | ✅ |
| **05** | NaN rellenados, valores razonables, medianas coherentes | ✅ |
| **06** | Redes binarias, coherencia con texto original | ✅ |
| **07** | Mapeos completos, valores "Otro" < 30% | ✅ |
| **08** | Dummies binarios, suma=1, sin multicolinealidad | ✅ |
| **09** | ID primera columna, agrupación temática | ✅ |
| **10** | Clusters completos, distribución balanceada | ✅ |

### Controles de Análisis (11-14)

| Control | Verificación | Crítico |
|---------|-------------|---------|
| **11** | P-values válidos, muestras suficientes, reproducibilidad | ✅ |
| **12** | Clasificación congruente/incongruente correcta | ✅ |
| **13** | Coeficientes [-1,1], matriz simétrica, diagonal=1 | ✅ |
| **14** | Coeficientes razonables, R² [0,1], modelos convergentes | ✅ |

### Control Final (15)

| Control | Verificación | Crítico |
|---------|-------------|---------|
| **15** | Identidad 100% con bases originales (reproducibilidad) | ✅ |

### Ejecución de Controles

```bash
# Ejecutar TODOS los controles (genera reportes PDF)
python Codigo/Control/Control_16_Ejecutar_Todos.py

# Ejecutar control específico
python Codigo/Control/Control_02_Calculo_Indices.py
```

**Reportes generados**: `Reportes/Control/*.pdf`

Cada reporte incluye:
- ✅ Estado de cada verificación (APROBADO/FALLÓ)
- 📋 Tablas con casos problemáticos (ID, fila, columna, valores)
- 📊 Estadísticas descriptivas
- 🔍 Detalles para debugging

---

## 📂 Archivos Importantes

### Scripts de Ejecución

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `Ejecutar_Pipeline_Completo.py` | Pipeline maestro de 10 pasos | `python Ejecutar_Pipeline_Completo.py` |
| `Control/Control_16_Ejecutar_Todos.py` | Ejecuta todos los controles | `python Control_16_Ejecutar_Todos.py` |
| `Notebooks/Pipeline_Principal.ipynb` | Notebook interactivo | `jupyter notebook` |

### Módulos Clave de Procesamiento

| Módulo | Función Principal | Descripción |
|--------|------------------|-------------|
| `Construccion_Bases.py` | `Procesar_Base_Completa()` | Combina CSVs, aplana JSON |
| `Calculo_Indices.py` | `Calcular_Todos_Indices()` | Progresismo, Conservadurismo |
| `Calculo_Variables_Cambio.py` | `Calcular_Variables_Cambio()` | CO y CT por ítem |
| `Limpieza_Datos.py` | `Limpiar_Datos_Completo()` | Filtros y outliers |

### Módulos de Análisis

| Módulo | Función Principal | Descripción |
|--------|------------------|-------------|
| `Mann_Whitney.py` | `Ejecutar_Mann_Whitney()` | Tests no paramétricos |
| `Modelos_SEM.py` | `Ejecutar_Modelo_SEM_Simple()` | Ecuaciones estructurales |
| `Modelos_Robustos.py` | `Modelo_Lineal_Robusto()` | Regresión con VIF |
| `Analisis_Correlacion.py` | `Calcular_Correlaciones()` | Spearman con p-valores |

---

## 🛠️ Uso Avanzado

### Personalizar el Pipeline

```python
# Ejecutar solo pasos específicos
from Procesamiento.Construccion_Bases import Procesar_Base_Completa
from Procesamiento.Calculo_Indices import Calcular_Todos_Indices

Df = Procesar_Base_Completa(Df_Crudo)
Df = Calcular_Todos_Indices(Df)
# ... continuar según necesidad
```

### Modificar Parámetros

Editar `Codigo/Utilidades/Configuracion.py`:

```python
# Cambiar número de desviaciones para outliers
NUM_DESVIACIONES_OUTLIERS = 3  # Cambiar a 2 o 4

# Modificar ítems de índices
ITEMS_PROGRESISTAS = [3, 4, 5, 6, 7, 9, 10, 16, 22, 24]
ITEMS_CONSERVADORES = [8, 11, 19, 20, 23, 25, 27, 28, 29, 30]
```

### Ejecutar Análisis Específico

```python
# Solo análisis de congruencia ideológica
from Test_Estadisticos.Tests_Adicionales import (
    Analizar_Congruencia_Ideologica
)

Resultados = Analizar_Congruencia_Ideologica(
    Df_Generales,
    Guardar_Excel=True,
    Guardar_Graficos=True
)
```

---

## 📈 Resultados y Visualizaciones

### Ubicación de Outputs

```
Tablas/
├── Bases_Procesadas/
│   ├── Base_Final_Generales.xlsx      # ~2786 casos, ~150 columnas
│   └── Base_Final_Ballotage.xlsx      # ~1254 casos, ~150 columnas
│
├── Resultados_Tests/
│   ├── Mann_Whitney_Generales.xlsx
│   └── Mann_Whitney_Ballotage.xlsx
│
└── Resultados_SEM/
    ├── Modelos_SEM_Generales.xlsx
    └── Modelos_SEM_Ballotage.xlsx

Graficos/
├── Cleveland/
│   ├── Congruencia_Generales.svg
│   └── Congruencia_Ballotage.svg
│
├── Heatmaps/
│   ├── Correlaciones_Indices_CO.svg
│   └── Correlaciones_Indices_CT.svg
│
└── Violin/
    └── Distribucion_CO_Por_Categoria.svg

Reportes/
└── Control/
    ├── Control_01_Construccion_Bases_Generales_YYYYMMDD_HHMMSS.pdf
    ├── Control_02_Calculo_Indices_Generales_YYYYMMDD_HHMMSS.pdf
    └── Control_Consolidado_YYYYMMDD_HHMMSS.pdf  # Reporte maestro
```

---

## 📚 Documentación Adicional

- **[Docs/PIPELINE_TECNICO.md](Docs/PIPELINE_TECNICO.md)**: Especificación técnica completa del pipeline (funciones, parámetros, formatos)
- **[Docs/GUIA_CONTROLES.md](Docs/GUIA_CONTROLES.md)**: Documentación exhaustiva del sistema de control de calidad
- **[Docs/API_REFERENCIA.md](Docs/API_REFERENCIA.md)**: Referencia completa de funciones y módulos
- **[CLAUDE.md](CLAUDE.md)**: Instrucciones para Claude Code (asistente de desarrollo)

---

## 🔧 Solución de Problemas

### Error: "No module named 'X'"

```bash
# Verificar instalación de dependencias
pip install pandas numpy scipy matplotlib seaborn openpyxl reportlab semopy statsmodels
```

### Error: "Archivo no encontrado"

Verificar que las rutas en `Configuracion.py` apunten correctamente a:
- `Data/Datos_Crudos/` (CSVs originales)
- Crear carpetas de salida si no existen

### Control falla con "Diferencias encontradas"

1. Revisar el PDF generado en `Reportes/Control/`
2. Identificar ID, fila y columna problemática
3. Verificar el código de procesamiento correspondiente
4. Corregir y re-ejecutar control específico

---

## 🤝 Contribución y Contacto

### Estructura de Código

**Todos los scripts siguen estas convenciones**:
- **Nomenclatura**: Pascal_Snake_Case exclusivamente
- **Idioma**: Código y comentarios en español
- **Líneas**: Máximo 70 caracteres
- **Docstrings**: Exhaustivos con type hints
- **Organización**: Comentarios separadores `# ====...====`

### Agregar Nuevo Análisis

1. Crear módulo en carpeta apropiada (`Test_Estadisticos/`, `Modelado_Estadistico/`, etc.)
2. Seguir patrón de módulos existentes
3. Agregar docstrings completos
4. Crear control correspondiente en `Control/` si aplica
5. Actualizar documentación

---

## 📖 Resumen de Variables Generadas

| Tipo | Cantidad | Descripción |
|------|----------|-------------|
| **IP Items Respuesta** | 20 | Respuestas base 1-5 a proposiciones |
| **IP Items Tiempo** | 20 | Tiempos de respuesta en ms |
| **IP Items Candidato** | 20 | Candidato asociado en fase 2 |
| **Índices** | 5 | Progresismo, Conservadurismo, Positividad, Tiempos |
| **Variables CO** | 40 | Cambio opinión (20 items × 2 direcciones) |
| **Variables CT** | 40 | Cambio tiempo (20 items × 2 direcciones) |
| **Congruencia** | 2 | CO_Congruentes_Promedio, CO_Incongruentes_Promedio |
| **Demográficas** | ~15 | Edad, Género, Región, Educación, etc. |
| **Redes/Medios** | ~21 | 8 redes sociales + 13 medios binarios |
| **Agrupadas** | ~10 | Edad_Agrupada, Autopercepcion, etc. |
| **Dummies** | ~30 | One-hot encoding de categóricas |
| **Clusters** | 3 | K-means, Jerárquico, DBSCAN |
| **TOTAL** | **~150** | Variables en bases finales |

---

## 📜 Licencia y Citación

Este proyecto es parte de una tesis de investigación en psicología política sobre el efecto de candidatos políticos en cambios de opinión durante las elecciones argentinas 2023.

**Para citar este trabajo**:
```
[Pendiente de publicación]
```

---

**Última actualización**: 2025-01-10
**Versión**: 2.0 (Proyecto reorganizado y modularizado)
