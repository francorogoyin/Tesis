# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Propósito del Proyecto

Proyecto de tesis de investigación en psicología política que analiza cómo la ideología política influye en los cambios de opinión (CO) y tiempos de respuesta (CT) cuando participantes evalúan cambios de valoración en proposiciones ideológico-políticas cuando estas están asociadas a candidatos políticos a cuando no lo están. El experimento analiza las valoraciones de los sujetos en una escala del 1-5 para distintas proposiciones (20, concretamente: 10 de índole progresista y 10 de índole conservadora). Luego, se les vuelve a proponer las mismas oraciones y a que las valoren, pero esta vez asociadas a candidatos que los sujetos consideran de izquierda o de derecha. Es decir, termina habiendo "ítems" (así se llaman las proposiciones u oraciones presentadas) de índole progresista o conservador asociadas a candidatos de izquierda o derecha, según el caso. Estudio realizado durante las elecciones argentinas de 2023 (Generales y Ballotage).

## Arquitectura del Proyecto

### Estructura de Directorios

- **Código/**: 70 notebooks numerados secuencialmente + `Funciones.py` con utilidades reutilizables
- **Data/**: Contiene subdirectorios para datos crudos, procesados y resultados
  - `Bases definitivas/`: Datasets consolidados finales
  - `Procesados/`: Datos con variables de congruencia ideológica calculadas
  - `Resultados_SEM/`: Outputs de modelos de ecuaciones estructurales
  - `Resultados_Cleveland/`, `Resultados_Barras/`, etc.: Resultados de visualizaciones
- **Modelos/**: Notebooks de modelado predictivo y clustering
- **Gráficos/**: Visualizaciones generadas (SVG/PNG)

### Flujo de Trabajo de Notebooks

Los notebooks están numerados para ejecución secuencial:

**Fase 1 (1-19): Preparación de Datos**
- Notebooks 1-2: Construcción de databases desde CSVs crudos
- Notebooks 3-8: Creación de índices (Positividad, Progresismo, Conservadurismo)
- Notebooks 12-13: Variables dummy y agrupamiento categórico
- Notebooks 15-17: Limpieza de datos y eliminación de outliers
- Notebooks 18-19: Cálculo de variables CO (Cambio de Opinión) y CT (Cambio de Tiempo)

**Fase 2 (20-47): Análisis Estadístico**
- Notebooks 21-24, 29-30, 35-36, 38-39: Tests de significancia estadística
- Notebooks 27-28, 37: Agregación de ítems significativos
- Notebooks 26, 41-47: Generación de tablas de resultados en Excel

**Fase 3 (48-70): Análisis Avanzados**
- Notebooks 48-50, 60-61: Análisis de Diferencia de Diferencias
- Notebook 52: Análisis de congruencia ideológica (congruente vs incongruente)
- Notebook 53: Validación cruzada de ítems significativos
- Notebook 54: Matrices de correlación (Spearman)
- Notebooks 55-59: Modelos SEM (ecuaciones estructurales) - 48 modelos totales
- Notebooks 60-64, 70: Gráficos de Cleveland para visualización de diferencias
- Notebooks 68-69: Heatmaps de correlaciones

### Variables Clave del Estudio

**Variables Dependientes:**
- `CO` (Cambio de Opinión): Diferencia en respuesta base vs con candidato asociado
- `CT` (Cambio de Tiempo): Diferencia en tiempo de respuesta base vs con candidato

**Predictores Principales:**
- `Indice_Progresismo`: Caracterización operativa de orientación progresista
- `Indice_Conservadurismo`: Caracterización operativa de orientación conservadora

**Categorías Ideológicas:**
- `Left_Wing`: Bregman, Solano
- `Progressivism`: Massa, Grabois
- `Centre`: Schiaretti
- `Moderate_Right_A`: Rodríguez Larreta
- `Moderate_Right_B`: Bullrich
- `Right_Wing_Libertarian`: Milei

**Variables de Congruencia:**
- Congruente: Progresista→Izquierda, Conservador→Derecha
- Incongruente: Progresista→Derecha, Conservador→Izquierda

### Funciones Reutilizables (Funciones.py)

El archivo `Funciones.py` contiene utilidades para:
- Procesamiento de estructuras JSON anidadas
- Creación automatizada de variables CO y CT
- Generación de boxplots por categoría ideológica
- Relleno de valores faltantes con medianas por categoría
- Eliminación de outliers por desviación estándar
- Aplanamiento de diccionarios anidados

## Comandos Comunes

### Ejecutar Notebooks

Los notebooks deben ejecutarse en orden numérico. Muchos incluyen:
```python
%%capture
%run "X. Notebook Anterior.ipynb"
```

### Ejecutar Análisis Específico

Para re-ejecutar un análisis específico sin dependencias:
```python
# En Jupyter
%run "Código/Funciones.py"
```

### Generar Bases Finales

Los notebooks 14 y 43 exportan las bases procesadas:
- `Data/Bases definitivas/Bases finalesGenerales.xlsx`
- `Data/Bases definitivas/Bases finalesBallotage.xlsx`

### Ejecutar Modelos SEM

Los notebooks 55-59 generan modelos. Cada uno exporta resultados a:
- `Data/Resultados_SEM/Modelos_[Tipo]_[Eleccion].xlsx`

## Consideraciones Técnicas

### REGLAS DE ESTILO DE CÓDIGO (OBLIGATORIAS)

**CRITICAL: Estas reglas son OBLIGATORIAS y no pueden ser olvidadas bajo ninguna circunstancia.**

#### Nomenclatura Pascal_Snake_Case

Todo el código debe usar exclusivamente **Pascal_Snake_Case** para:
- Variables, funciones, clases
- Nombres de archivos (.py, .pyw, .ipynb)
- Nombres de carpetas y directorios
- Claves de diccionarios
- Bucles, condicionales, manejo de archivos
- Funciones lambda, nombres de módulos, constantes
- Cualquier otro identificador en el código

Ejemplos correctos:
- `Variable_Descriptiva`, `Lista_De_Numeros`, `Funcion_De_Calculo`
- `Procesamiento_Datos.py`, `Modelos_SEM.py`
- `Test_Estadisticos/`, `Modelado_Estadistico/`

#### Nombres Descriptivos

- **PROHIBIDO** usar abreviaciones o nombres genéricos (Var, Dec, Tmp)
- Usar nombres claros y completos (Variable_Configuracion, Diccionario_Usuarios)
- Las funciones deben comenzar con verbos de acción:
  - ✅ Correcto: `Calcular_Total()`, `Obtener_Datos_Usuario()`, `Generar_Reporte()`
  - ❌ Incorrecto: `Datos_Usuario()`, `Reporte()`, `Total()`

#### Idioma

- **TODO** el código debe estar en español: variables, funciones, clases, comentarios y docstrings

#### Comentarios

- Deben ser siempre descriptivos, como para otra persona o para ti en el futuro lejano
- Siempre finalizar con un punto
- ✅ Correcto: `# El IMC se calcula como el peso en kilogramos dividido por la altura en metros al cuadrado.`
- ❌ Incorrecto: `# Cálculo.`

#### Espaciado y Sintaxis

- El signo `=` siempre debe tener un espacio antes y después: `variable = valor`
- Las líneas no deben exceder **70 caracteres** de longitud
- Si una línea excede 70 caracteres, dividirla en varias líneas con indentación clara

#### Docstrings

Cada función y clase debe tener un docstring exhaustivo:
- Descripción detallada de su propósito
- Type hinting en parámetros y retorno
- **NO** incluir ejemplos de uso salvo especificación explícita

Formato obligatorio:
```python
def Funcion_Ejemplo(Parametro_Uno: str,
                    Parametro_Dos: int) -> bool:

    """
    Descripción detallada de qué hace esta función.
    Puede incluir múltiples líneas explicativas.

    """

    return True
```

Notar las líneas vacías:
1. Entre parámetros y comillas de apertura del docstring
2. Entre última línea del docstring y comillas de cierre
3. Entre comillas de cierre y cuerpo de la función

#### Organización de Archivos .py

Los archivos .py deben estar organizados con **comentarios separadores** para facilitar navegación:

```python
# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np


# ============================================================
# CONSTANTES Y CONFIGURACIÓN
# ============================================================

RUTA_DATOS = "Data/Bases definitivas/"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def Funcion_Helper():
    """Descripción."""
    pass


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def Funcion_Principal():
    """Descripción."""
    pass


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    pass
```

#### Principio de Responsabilidad Única

- Las funciones deben hacer **solo una cosa** siempre que sea posible
- Si una función tiene múltiples responsabilidades, dividirla en funciones más pequeñas

### Dependencias Principales

```python
pandas          # Manipulación de datos
numpy           # Cálculos numéricos
matplotlib      # Visualizaciones base
seaborn         # Gráficos estadísticos
scipy           # Tests estadísticos (mannwhitneyu, spearmanr)
semopy          # Modelos de ecuaciones estructurales
statsmodels     # Análisis estadístico complementario
openpyxl        # Exportación a Excel
```

### Análisis Estadísticos Implementados

1. **Tests no paramétricos**: Mann-Whitney U para comparaciones entre grupos
2. **Modelos SEM**: Regresiones estructurales con semopy
3. **Diferencia de Diferencias**: Cuantificación de cambios entre elecciones
4. **Correlaciones de Spearman**: Entre predictores y outcomes
5. **Validación Cruzada**: Filtrado cruzado entre Generales y Ballotage

### Formatos de Salida

- **Excel (.xlsx)**: Tablas de resultados, bases procesadas
- **SVG**: Gráficos de alta calidad (Cleveland, heatmaps)
- **PNG**: Visualizaciones complementarias
- **CSV**: Exportaciones específicas de subconjuntos

## Resultados Principales

### Congruencia Ideológica (Notebook 52)
- **Generales**: 11 de 12 comparaciones significativas (p < 0.05)
- **Ballotage**: 3 de 12 comparaciones significativas
- Efecto robusto en primera vuelta, atenuado en segunda

### Modelos SEM (Notebooks 55-59)
- **48 modelos** evaluando predicción de ideología sobre cambios
- R² promedio: 2-4% (efectos pequeños pero significativos)
- Mejor predictor en Generales: Índice de Conservadurismo (β = -1.019)
- En Ballotage: ambos índices con efectos similares (~50% modelos significativos)

### Validación Cruzada (Notebook 53)
- **Generales**: 14 ítems CT robustos (35%)
- **Ballotage**: 5 ítems CT robustos (12.5%)
- Mayor consistencia en primera vuelta electoral

## Documentación Adicional

- `RESUMEN_ANALISIS_SEM.md`: Plantilla de resumen ejecutivo de modelos
- `Resumen_Analisis_Estadisticos.docx`: Documento Word con resultados consolidados
- `Instrucciones Tesis.txt`: Notas del investigador
- `Guía para el paper de IP.odt`: Guía metodológica del estudio

## Datos del Estudio

- **Participantes**: ~2786 en Generales, ~1254 en Ballotage
- **Items IP**: 20 ítems de personalidad implícita evaluados con/sin candidatos
- **Variables de control**: Demográficas, electorales, consumo de medios, variables situacionales (sueño, sustancias, estrés)

## Proyecto Reorganizado: Tesis_Ordenada

A partir de 2025, el proyecto está siendo reorganizado en una estructura modular bajo el directorio `Tesis_Ordenada/`. El proyecto original se mantiene intacto como backup.

### Nueva Estructura de Directorios

```
Tesis_Ordenada/
├── Codigo/
│   ├── Procesamiento/
│   │   ├── Construccion_Bases.py
│   │   ├── Calculo_Indices.py
│   │   ├── Variables_Cambio.py
│   │   └── Limpieza_Datos.py
│   ├── Test_Estadisticos/
│   │   ├── Mann_Whitney.py
│   │   ├── Congruencia_Ideologica.py
│   │   ├── Validacion_Cruzada.py
│   │   └── Diferencia_Diferencias.py
│   ├── Modelado_Estadistico/
│   │   ├── Modelos_SEM.py
│   │   ├── Correlaciones.py
│   │   └── Clusters.py
│   ├── Visualizacion/
│   │   ├── Graficos_Cleveland.py
│   │   ├── Heatmaps.py
│   │   ├── Graficos_Violin.py
│   │   └── Graficos_Barras.py
│   └── Utilidades/
│       ├── Funciones_Comunes.py
│       └── Configuracion.py
├── Graficos/
│   ├── Cleveland/
│   ├── Heatmaps/
│   ├── Violin/
│   └── Barras/
├── Tablas/
│   ├── Resultados_Tests/
│   ├── Resultados_SEM/
│   └── Bases_Procesadas/
├── Data/
│   └── (enlaces simbólicos a ../Data/)
└── Notebooks/
    ├── Exploracion/
    ├── Pipeline_Principal.ipynb
    └── Analisis_Final/
```

### Principios de la Reorganización

1. **Modularidad**: Código reutilizable en archivos .py organizados por función
2. **Separación de Responsabilidades**: Procesamiento, análisis, modelado y visualización separados
3. **Backup Completo**: El proyecto original permanece intacto
4. **Comentarios Separadores**: Todos los archivos .py usan comentarios `# ====...====` para delimitar secciones
5. **Pipeline Ejecutable**: Scripts que permiten ejecutar el análisis completo desde línea de comandos

### Carpetas Principales

#### Codigo/

Contiene todo el código Python organizado por tipo de operación:

- **Procesamiento/**: Construcción de bases, índices, variables de cambio, limpieza
- **Test_Estadisticos/**: Tests Mann-Whitney, análisis de congruencia, validación cruzada
- **Modelado_Estadistico/**: Modelos SEM, correlaciones, clustering
- **Visualizacion/**: Todos los tipos de gráficos
- **Utilidades/**: Funciones compartidas, configuración global

#### Graficos/

Almacena todas las visualizaciones generadas, organizadas por tipo:
- Cleveland plots comparativos
- Heatmaps de correlaciones
- Gráficos de violín
- Gráficos de barras

#### Tablas/

Contiene todos los resultados tabulares exportados:
- Resultados de tests estadísticos (Excel/CSV)
- Outputs de modelos SEM
- Bases de datos procesadas

### Migración desde Proyecto Original

Para migrar funcionalidad de los notebooks originales a la nueva estructura:

1. Identificar el código reutilizable en el notebook
2. Extraer a función con nombre descriptivo
3. Agregar docstring completo
4. Colocar en el módulo apropiado bajo `Codigo/`
5. Usar comentarios separadores para organizar el archivo
6. Mantener el notebook original sin cambios

### Comandos para Ejecutar Pipeline

```bash
# Ejecutar procesamiento completo
python Codigo/Procesamiento/Pipeline_Completo.py

# Ejecutar solo análisis específico
python Codigo/Test_Estadisticos/Congruencia_Ideologica.py

# Generar todas las visualizaciones
python Codigo/Visualizacion/Generar_Todos_Graficos.py
```