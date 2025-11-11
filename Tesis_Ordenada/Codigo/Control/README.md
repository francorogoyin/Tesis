# Control - Sistema de Verificación Exhaustiva

Este directorio contiene **16 scripts de control** que verifican exhaustivamente cada paso del procesamiento de datos de la tesis, desde las bases crudas hasta los resultados finales de análisis estadísticos.

## Filosofía de los Controles

- **Zero tolerance**: Cualquier desviación se reporta, sin umbrales de aceptación
- **Verificación exhaustiva**: Fila por fila, columna por columna
- **Trazabilidad completa**: Cada problema reporta ID de sujeto y columna exacta
- **Reportes PDF**: Todos los controles generan reportes descriptivos en PDF
- **Automatización**: Retorno booleano permite integración en pipelines
- **Reproducibilidad**: Verifica que inputs idénticos produzcan outputs idénticos

## Estructura de Controles

### Controles de Preprocesamiento (01-10)

#### Control_01_Construccion_Bases.py
**Verificaciones:**
- IDs únicos sin duplicados
- Existencia de columnas críticas
- Tipos de datos correctos
- Sin NaN en columnas críticas
- Rangos de edad válidos [18-100]

#### Control_02_Calculo_Indices.py
**Verificaciones:**
- Existencia de índices de progresismo y conservadurismo
- Rangos de respuesta [1-5] y tiempo [≥0]
- Coherencia entre índices (no ambos extremos simultáneamente)
- Sin NaN en índices
- Detección de valores extremos (>3 SD)

#### Control_03_Variables_Cambio.py
**Verificaciones:**
- Rangos CO en [-4, +4]
- CT no negativos
- Coherencia CO = Respuesta_Asociada - Respuesta_Base
- Distribución simétrica de CO (media ≈ 0)
- Existencia de todas las variables CO/CT esperadas

#### Control_04_Limpieza_Datos.py
**Verificaciones:**
- Pérdida de datos aceptable (<20%)
- Outliers de edad eliminados
- Sin duplicados post-limpieza
- Columnas mantenidas

**Nota:** Requiere DataFrame antes y después de limpieza.

#### Control_05_Relleno_Medianas.py
**Verificaciones:**
- Todos los NaN rellenados
- Columnas _Original creadas como backup
- Valores rellenados en rangos razonables
- Medianas por categoría ideológica diferentes

**Nota:** Requiere DataFrame antes y después de relleno.

#### Control_06_Redes_Y_Medios.py
**Verificaciones:**
- Columnas binarias (solo 0 y 1)
- Coherencia con texto original (Red_Social, Medios_Prensa)
- Al menos una red social por sujeto
- Existencia de todas las columnas esperadas

**Redes verificadas:** Twitter, Facebook, Instagram, Threads, Tiktok, Youtube, Whatsapp, Telegram

**Medios verificados:** 13 medios de prensa argentinos

#### Control_07_Agrupamientos.py
**Verificaciones:**
- Existencia de variables agrupadas
- Mapeo Provincia → Región completo
- Coherencia Edad ↔ Edad_Agrupada
- Valores "Otro" no excesivos (<30%)
- Autopercepciones solo A/B/C

#### Control_08_Variables_Dummy.py
**Verificaciones:**
- Existencia de dummies para todas las categóricas
- Columnas dummy binarias (0/1)
- Suma por fila = 1 (solo una categoría activa)
- Coherencia con columna original
- Sin multicolinealidad (n-1 dummies)

**Variables verificadas:** Sexo, Nivel_Educativo, Region, Edad_Agrupada, Categoria_PASO_2023

#### Control_09_Ordenamiento.py
**Verificaciones:**
- ID como primera columna
- Agrupación temática (IP juntas, índices juntos, etc.)
- Prefijos aplicados (Medios_Prensa_, etc.)
- Nombres consistentes (Pascal_Snake_Case, sin espacios/guiones)

#### Control_10_Clusters.py
**Verificaciones:**
- Existencia de columnas de cluster
- Merge por ID exitoso sin duplicados
- Sin NaN en clusters
- Distribución balanceada (ningún cluster <5%)
- Valores válidos (enteros ≥ -1 o etiquetas)

**Clusters verificados:** Kmeans, Jerárquico, DBSCAN

---

### Controles de Análisis Estadístico (11-14)

#### Control_11_Tests_Mann_Whitney.py
**Verificaciones:**
- Existencia de columnas de resultados
- P-values en [0, 1]
- Tamaños de muestra suficientes (≥10)
- Comparaciones entre categorías diferentes
- Reproducibilidad (re-cálculo de muestra de tests)

#### Control_12_Congruencia_Ideologica.py
**Verificaciones:**
- Clasificación correcta de ítems congruentes/incongruentes
- P-values válidos [0, 1]
- Comparaciones completas (todos los candidatos)
- Medianas coherentes (CO en [-4,+4], CT ≥0)

**Candidatos izquierda:** Bregman, Solano
**Candidatos derecha:** Milei, Bullrich

#### Control_13_Correlaciones.py
**Verificaciones:**
- Coeficientes Spearman en [-1, 1]
- P-values en [0, 1]
- Matriz de correlación simétrica
- Diagonal = 1 (correlación consigo misma)
- Reproducibilidad (re-cálculo de muestra)

#### Control_14_Modelos_SEM.py
**Verificaciones:**
- Coeficientes razonables (alerta si |β| > 10)
- P-values válidos [0, 1]
- R² en [0, 1]
- Proporción de modelos convergentes
- Coherencia de signos con teoría

---

### Control Final

#### Control_15_Identidad_Bases.py
**Verificación de reproducibilidad 100%:**
- Dimensiones idénticas (filas y columnas)
- Columnas idénticas (nombres y orden)
- Tipos de datos idénticos
- Valores idénticos celda por celda (tolerancia 1e-10)

Compara bases procesadas en `Tesis_Ordenada/` contra bases definitivas del proyecto original.

---

### Script Maestro

#### Control_16_Ejecutar_Todos.py
**Ejecuta todos los controles secuencialmente:**
1. Carga bases de Generales y Ballotage
2. Ejecuta controles 01-10, 15 para cada base
3. Genera reporte consolidado PDF
4. Muestra resumen con:
   - Controles ejecutados/aprobados/fallidos
   - Duración total
   - Detalles de controles fallidos

**Uso:**
```bash
python Control_16_Ejecutar_Todos.py
```

## Formato de Reportes PDF

Todos los controles generan reportes PDF en `Reportes/Control/` con:

- **Encabezado**: Nombre del control, base y fecha/hora
- **Resumen**: X/Y verificaciones aprobadas
- **Detalles por verificación**:
  - Estado (✓ APROBADO / ✗ FALLÓ)
  - Tablas con casos problemáticos
  - ID de sujeto, fila, columna y valores específicos
- **Código de colores**: Verde (aprobado), Rojo (falló)

## Convenciones de Código

Todos los controles siguen estas convenciones:

- **Nomenclatura**: Pascal_Snake_Case consistente
- **Estructura**:
  - Importaciones
  - Constantes
  - Funciones de verificación (4-6 por control)
  - Generación de reporte PDF
  - Función principal `Ejecutar_Control_XXX()`
- **Docstrings**: Completos en todas las funciones
- **Comentarios separadores**: `# ====...====` para delimitar secciones
- **Return**: `bool` indicando aprobación total

## Cómo Usar los Controles

### Uso Individual

```python
from Control.Control_01_Construccion_Bases import (
    Ejecutar_Control_Construccion_Bases
)

Df = pd.read_excel("base.xlsx")
Aprobado = Ejecutar_Control_Construccion_Bases("Generales", Df)

if Aprobado:
    print("✓ Control aprobado")
else:
    print("✗ Revisar reporte PDF")
```

### Controles que Requieren Datos Adicionales

**Control_04 y Control_05** (antes/después):
```python
Df_Antes = pd.read_excel("base_antes.xlsx")
Df_Despues = pd.read_excel("base_despues.xlsx")

Aprobado = Ejecutar_Control_Limpieza_Datos(
    "Generales", Df_Antes, Df_Despues
)
```

**Control_11** (reproducibilidad):
```python
Df_Resultados = pd.read_excel("resultados_tests.xlsx")
Df_Datos = pd.read_excel("base.xlsx")

Aprobado = Ejecutar_Control_Tests_Mann_Whitney(
    "Generales", Df_Resultados, Df_Datos
)
```

**Control_13** (con matriz):
```python
Df_Resultados = pd.read_excel("correlaciones.xlsx")
Matriz = pd.read_excel("matriz_correlacion.xlsx", index_col=0)
Df_Datos = pd.read_excel("base.xlsx")

Aprobado = Ejecutar_Control_Correlaciones(
    "Generales", Df_Resultados, Matriz, Df_Datos
)
```

### Uso del Script Maestro

```bash
# Ejecutar todos los controles
python Control_16_Ejecutar_Todos.py

# Revisar reporte consolidado
# Reportes/Control/Control_Consolidado_YYYYMMDD_HHMMSS.pdf
```

## Interpretación de Resultados

### ✓ Todos los controles aprobados
- Pipeline reproduce exactamente resultados originales
- Datos procesados correctamente en todos los pasos
- Listo para análisis y publicación

### ✗ Algún control falló
1. Revisar reporte PDF del control específico
2. Identificar ID de sujeto y columna problemática
3. Verificar en el código de procesamiento correspondiente
4. Corregir error
5. Re-ejecutar control

## Mantenimiento

### Agregar Nuevo Control

1. Seguir patrón de controles existentes
2. Implementar 4-6 funciones de verificación
3. Generar reporte PDF con reportlab
4. Return booleano
5. Agregar a `Control_16_Ejecutar_Todos.py`

### Modificar Control Existente

1. Mantener firma de función principal
2. Mantener estructura de reporte PDF
3. Documentar cambios en docstrings
4. Re-ejecutar script maestro para verificar integración

## Dependencias

```python
pandas          # Manipulación de DataFrames
numpy           # Operaciones numéricas
reportlab       # Generación de PDFs
scipy           # Tests estadísticos (mannwhitneyu, spearmanr)
pathlib         # Manejo de rutas
```

## Autores y Contacto

Desarrollado como parte del proyecto de tesis de Patricio sobre psicología política y cambio de opinión en elecciones argentinas 2023.

---

**Última actualización**: 2025-01-10
