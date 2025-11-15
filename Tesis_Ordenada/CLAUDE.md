# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Propósito del Proyecto

**PROYECTO DE MIGRACIÓN**: Este es un proyecto de reorganización y refactorización del proyecto de tesis original ubicado en `../`. El objetivo es emular exactamente los mismos resultados que el proyecto original, pero con código más eficiente, ordenado y modular.

### Contexto del Estudio Original

Proyecto de tesis de investigación en psicología política que analiza cómo la ideología política influye en los cambios de opinión (CO) y tiempos de respuesta (CT) cuando participantes evalúan proposiciones ideológico-políticas asociadas a candidatos políticos versus sin candidatos.

El experimento analiza valoraciones en escala 1-5 para 20 proposiciones (10 progresistas, 10 conservadoras). Luego se presentan las mismas proposiciones asociadas a candidatos que los sujetos consideran de izquierda o derecha. Estudio realizado durante las elecciones argentinas de 2023 (Generales y Ballotage).

## PROTOCOLO DE TRABAJO PARA CADA ETAPA

**IMPORTANTE:** Al abordar cualquier etapa de migración, Claude debe seguir OBLIGATORIAMENTE este procedimiento en orden:

### Paso 1: Lectura de CLAUDE.md
- Leer la sección correspondiente a la etapa actual en este archivo
- Identificar notebooks originales asociados
- Revisar dependencias y resultados esperados
- Verificar estado de checkboxes (qué está hecho, qué falta)

### Paso 2: Lectura de Notebooks Originales
- Leer COMPLETAMENTE los notebooks originales listados para la etapa
- Entender la lógica, funciones, transformaciones y cálculos exactos
- Identificar tests estadísticos específicos usados
- Anotar resultados intermedios y finales

### Paso 3: Verificación y Corrección del CLAUDE.md
- Comparar lo documentado en CLAUDE.md con lo observado en notebooks
- Si hay discordancias, inconsistencias o información faltante:
  - Actualizar CLAUDE.md para reflejar la realidad del código original
  - Documentar hallazgos importantes no mencionados
- Preguntar al usuario sobre ambigüedades antes de proceder

### Paso 4: Evaluación del Código Migrado Existente
- Revisar si ya existe código migrado para esta etapa
- Verificar si es:
  - **Suficiente:** ¿Cubre toda la funcionalidad del notebook original?
  - **Necesario:** ¿Cada parte del código migrado es realmente necesaria?
  - **Satisfactorio:** ¿Sigue las reglas de estilo? ¿Es eficiente? ¿Da los mismos resultados?

### Paso 5: Acción Correctiva
Si el código existente NO es suficiente, necesario o satisfactorio:
- **Corregir:** Ajustar código que tiene errores o no sigue reglas de estilo
- **Completar:** Agregar funcionalidad faltante
- **Eliminar:** Quitar código redundante o innecesario
- **Refactorizar:** Mejorar eficiencia manteniendo exactitud de resultados

### Paso 6: Control Simple y Ejecución Aislada
**CRÍTICO:** Antes de validar contra notebooks, hacer un control simple del paso actual:
- **Control de Integridad:**
  - Verificar que las funciones existen y son importables
  - Verificar que las constantes/configuración están correctas
  - Verificar tipos de datos y estructuras esperadas
- **Ejecución Aislada:**
  - Ejecutar SOLO el código migrado de este paso (no todo el pipeline)
  - Usar datos de prueba o cargar un pequeño subset si es necesario
  - Verificar que no hay errores de ejecución
  - Inspeccionar outputs intermedios (primeras filas, estadísticos básicos)
- **Criterios de Éxito Mínimos:**
  - El código ejecuta sin errores
  - Los tipos de datos de salida son correctos
  - Las dimensiones/shapes son razonables
  - No hay valores absurdos o fuera de rango
- **Documentación del Control:**
  - El control puede estar al final del mismo archivo Python (sección `if __name__ == "__main__"`)
  - Generar un reporte DESCRIPTIVO (TXT) en carpeta `Controles/`
  - NO crear archivos .py separados solo para controles
  - **El reporte debe incluir:**
    - Qué se controló específicamente (no solo "OK")
    - Cómo se controló (método, criterios)
    - Ejemplos concretos de datos verificados
    - Resultados numéricos específicos (antes/después, valores, dimensiones)
    - Criterios de éxito claros y si se cumplieron
    - Cualquier observación o advertencia relevante

### Paso 7: Validación Completa
- Ejecutar código migrado y comparar resultados con notebooks originales
- Verificar que los outputs sean IDÉNTICOS
- Documentar cualquier diferencia encontrada y resolverla

### Paso 8: Actualización de Documentación
- Marcar checkbox de la etapa como completada en CLAUDE.md
- Actualizar sección de "Documentación de Progreso por Sesión"
- Documentar cualquier hallazgo o decisión importante

**NUNCA** saltarse estos pasos. **SIEMPRE** seguir este protocolo en orden.

## ETAPAS DEL PROYECTO

### ETAPA 1: ARMADO DE LA BASE DESDE JSON

#### 1.1. Construcción Inicial de Databases
- [x] **1.1.1. Lectura de archivos JSON crudos** (Notebooks 1-2)
  - Cargar datos de Generales y Ballotage
  - Procesar estructura JSON anidada
  - Aplanar diccionarios
  - **Migrado a:** `Codigo/Procesamiento/Construccion_Bases.py`

#### 1.2. Limpieza y Control de Calidad (ANTES de calcular índices)
- [x] **1.2.1. Detección y eliminación de outliers** (Notebooks 15-17)
  - Por desviación estándar
  - Por criterios específicos de cada variable
  - **Migrado a:** `Codigo/Procesamiento/Limpieza_Datos.py`

- [x] **1.2.2. Imputación de valores faltantes** (Notebooks 15-17)
  - Relleno con medianas por categoría
  - **IMPORTANTE:** Esto debe hacerse ANTES de calcular los índices
  - **Migrado a:** `Codigo/Procesamiento/Limpieza_Datos.py`

#### 1.3. Creación de Índices Ideológicos (DESPUÉS de imputación)
- [x] **1.3.1. Índice de Positividad** (Notebooks 3-8)
  - Cálculo basado en valoraciones de ítems
  - **Migrado a:** `Codigo/Procesamiento/Calculo_Indices.py`

- [x] **1.3.2. Índice de Progresismo** (Notebooks 3-8)
  - Suma ponderada de ítems progresistas
  - **Migrado a:** `Codigo/Procesamiento/Calculo_Indices.py`

- [x] **1.3.3. Índice de Conservadurismo** (Notebooks 3-8)
  - Suma ponderada de ítems conservadores
  - **Migrado a:** `Codigo/Procesamiento/Calculo_Indices.py`

- [x] **1.3.4. Índices de Tiempo** (Notebooks 3-8)
  - Índice de Progresismo por tiempo de respuesta
  - Índice de Conservadurismo por tiempo de respuesta
  - **Migrado a:** `Codigo/Procesamiento/Calculo_Indices.py`

#### 1.4. Variables Categóricas y Dummy
- [x] **1.4.1. Variables dummy demográficas** (Notebooks 12-13)
  - Género, Región, Nivel educativo, Estrato social
  - **Migrado a:** `Codigo/Procesamiento/Construccion_Bases.py`

- [x] **1.4.2. Agrupamiento de candidatos en categorías ideológicas** (Notebooks 12-13)
  - Left_Wing, Progressivism, Centre, Moderate_Right_A/B, Right_Wing_Libertarian
  - **Migrado a:** `Codigo/Procesamiento/Construccion_Bases.py`

#### 1.5. Variables de Cambio Básicas
- [x] **1.5.1. Variables CO básicas por ítem** (Notebooks 18-19)
  - CO_Item_X_Izq / CO_Item_X_Der para cada ítem
  - Diferencia entre valoración base y con candidato
  - **Migrado a:** `Codigo/Procesamiento/Variables_Cambio.py`

- [x] **1.5.2. Variables CT básicas por ítem** (Notebooks 18-19)
  - CT_Item_X_Izq / CT_Item_X_Der para cada ítem
  - Diferencia entre tiempo base y con candidato
  - **Migrado a:** `Codigo/Procesamiento/Variables_Cambio.py`

- [x] **1.5.3. Variables CO agregadas básicas** (Notebooks 18-19)
  - CO_Pro, CO_Con (todos los ítems progresistas/conservadores)
  - CO_Pro_Izq, CO_Pro_Der, CO_Con_Izq, CO_Con_Der
  - **Migrado a:** `Codigo/Procesamiento/Variables_Cambio.py`

- [x] **1.5.4. Variables CT agregadas básicas** (Notebooks 18-19)
  - CT_Pro, CT_Con
  - CT_Pro_Izq, CT_Pro_Der, CT_Con_Izq, CT_Con_Der
  - **Migrado a:** `Codigo/Procesamiento/Variables_Cambio.py`

#### 1.6. Variables de Cambio Sumadas
- [ ] **1.6.1. Variables CO sumadas** (Notebook 27)
  - `Cambio_Op_Sum_Pro_Izq`: Suma CO ítems progresistas → izquierda
  - `Cambio_Op_Sum_Pro_Der`: Suma CO ítems progresistas → derecha
  - `Cambio_Op_Sum_Con_Izq`: Suma CO ítems conservadores → izquierda
  - `Cambio_Op_Sum_Con_Der`: Suma CO ítems conservadores → derecha
  - **Migrar a:** `Codigo/Procesamiento/Variables_Cambio_Agregadas.py`

- [ ] **1.6.2. Variables CT sumadas** (Notebook 27)
  - `Cambio_Tiempo_Sum_Pro_Izq`
  - `Cambio_Tiempo_Sum_Pro_Der`
  - `Cambio_Tiempo_Sum_Con_Izq`
  - `Cambio_Tiempo_Sum_Con_Der`
  - **Migrar a:** `Codigo/Procesamiento/Variables_Cambio_Agregadas.py`

#### 1.7. Variables de Cambio Filtradas (solo ítems significativos)
- [ ] **1.7.1. Variables CO filtradas** (Notebook 28)
  - `Cambio_Op_Filt_Pro_Izq`: Suma solo ítems significativos
  - `Cambio_Op_Filt_Pro_Der`
  - `Cambio_Op_Filt_Con_Izq`
  - `Cambio_Op_Filt_Con_Der`
  - **Dependencia:** Requiere tests Kruskal-Wallis (Etapa 2.2)
  - **Migrar a:** `Codigo/Procesamiento/Variables_Cambio_Filtradas.py`

- [ ] **1.7.2. Variables CT filtradas** (Notebook 37)
  - `Cambio_Tiempo_Filt_Pro_Izq`
  - `Cambio_Tiempo_Filt_Pro_Der`
  - `Cambio_Tiempo_Filt_Con_Izq`
  - `Cambio_Tiempo_Filt_Con_Der`
  - **Dependencia:** Requiere tests Kruskal-Wallis para CT
  - **Migrar a:** `Codigo/Procesamiento/Variables_Cambio_Filtradas.py`

#### 1.8. Variables de Congruencia Ideológica
- [ ] **1.8.1. Variables de congruencia CO** (Modelos/20)
  - `CO_Congruente`: Progresista→Izquierda + Conservador→Derecha
  - `CO_Incongruente`: Progresista→Derecha + Conservador→Izquierda
  - **Migrar a:** `Codigo/Procesamiento/Variables_Congruencia.py`

- [ ] **1.8.2. Variables de congruencia CT** (Modelos/20)
  - `CT_Congruente`
  - `CT_Incongruente`
  - **Migrar a:** `Codigo/Procesamiento/Variables_Congruencia.py`

#### 1.9. Incorporación de Variables de Clustering
- [ ] **1.9.1. Incorporar variables de clustering externas** (Notebook 42)
  - `Conservative_Cluster`: Pertenencia a cluster conservador (calculado externamente)
  - `Progressive_Cluster`: Pertenencia a cluster progresista (calculado externamente)
  - **IMPORTANTE:** Estas variables fueron calculadas por otra persona. Solo se incorporan a la base final.
  - **Migrar a:** `Codigo/Procesamiento/Variables_Cluster.py`

#### 1.10. Variables de Diferencia de Diferencias
- [ ] **1.10.1. Variables DifDif** (Notebook 48)
  - Cálculo de diferencias entre Generales y Ballotage
  - Por ítem y por categoría
  - **Migrar a:** `Codigo/Procesamiento/Variables_Diferencia_Diferencias.py`

#### 1.11. Exportación de Bases Finales
- [ ] **1.11.1. Guardar bases procesadas** (Notebooks 14, 43)
  - `Data/Bases definitivas/Generales.xlsx`
  - `Data/Bases definitivas/Ballotage.xlsx`
  - **Migrar a:** `Codigo/Procesamiento/Pipeline_Completo.py`

---

### ETAPA 2: ANÁLISIS ESTADÍSTICO

**IMPORTANTE:** Usar exactamente los mismos tests que en los notebooks originales. No cambiar tests aunque sean del mismo tipo de comparación.

#### 2.1. Tests de Cambios Promedios (Variables Agregadas)

- [ ] **2.1.1. Kruskal-Wallis para cambios promedios** (Notebook 21)
  - **Test:** Kruskal-Wallis H
  - **Variables:** `CO_Pro_Izq`, `CO_Con_Izq`, `CO_Pro_Der`, `CO_Con_Der`
  - **Comparaciones:** Entre 6 categorías ideológicas
  - **Propósito:** Identificar si hay diferencias significativas entre categorías
  - **Migrar a:** `Codigo/Test_Estadisticos/Kruskal_Wallis_Promedios.py`

- [ ] **2.1.2. Post-hoc Dunn para cambios promedios** (Notebook 22)
  - **Test:** Prueba de Dunn con corrección de Holm
  - **Variables:** Solo variables significativas del Notebook 21
  - **Propósito:** Identificar qué pares de categorías difieren
  - **Migrar a:** `Codigo/Test_Estadisticos/Dunn_Post_Hoc_Promedios.py`

#### 2.2. Tests de Cambios por Ítem Individual (CO)

- [ ] **2.2.1. Kruskal-Wallis para ítems CO** (Notebook 23)
  - **Test:** Kruskal-Wallis H
  - **Variables:** 40 ítems CO individuales (20 ítems × 2 candidatos)
  - **Comparaciones:** Entre 6 categorías ideológicas
  - **Resultados esperados:**
    - Generales: 11 ítems significativos
    - Ballotage: 9 ítems significativos
  - **Migrar a:** `Codigo/Test_Estadisticos/Kruskal_Wallis_Items.py`

- [ ] **2.2.2. Post-hoc Dunn para ítems CO** (Notebook 24)
  - **Test:** Prueba de Dunn con corrección de Holm
  - **Variables:** Solo ítems significativos del Notebook 23
  - **Migrar a:** `Codigo/Test_Estadisticos/Dunn_Post_Hoc_Items.py`

#### 2.3. Tests de Cambios de Tiempo (CT)

- [ ] **2.3.1. Kruskal-Wallis para cambios promedios CT** (Notebooks 29-30)
  - **Test:** Kruskal-Wallis H
  - **Variables:** `CT_Pro_Izq`, `CT_Con_Izq`, `CT_Pro_Der`, `CT_Con_Der`
  - **Migrar a:** `Codigo/Test_Estadisticos/Kruskal_Wallis_Promedios.py` (mismo archivo, función parametrizada)

- [ ] **2.3.2. Post-hoc Dunn para cambios promedios CT** (Notebooks 29-30)
  - **Test:** Prueba de Dunn con corrección de Holm
  - **Migrar a:** `Codigo/Test_Estadisticos/Dunn_Post_Hoc_Promedios.py` (función parametrizada)

- [ ] **2.3.3. Kruskal-Wallis para ítems CT** (Notebooks 35-36, 38-39)
  - **Test:** Kruskal-Wallis H
  - **Variables:** 40 ítems CT individuales
  - **Migrar a:** `Codigo/Test_Estadisticos/Kruskal_Wallis_Items.py` (función parametrizada)

- [ ] **2.3.4. Post-hoc Dunn para ítems CT** (Notebooks 35-36, 38-39)
  - **Test:** Prueba de Dunn con corrección de Holm
  - **Migrar a:** `Codigo/Test_Estadisticos/Dunn_Post_Hoc_Items.py` (función parametrizada)

#### 2.4. Análisis de Congruencia Ideológica

- [ ] **2.4.1. Wilcoxon pareado - Población general** (Notebook 52)
  - **Test:** Wilcoxon signed-rank test (pareado)
  - **Comparaciones:** Congruente vs Incongruente (todas las poblaciones juntas)
  - **Variables:** `CO_Congruente` vs `CO_Incongruente`, `CT_Congruente` vs `CT_Incongruente`
  - **Resultados esperados:**
    - Generales: 4 de 4 significativas
    - Ballotage: 4 de 4 significativas
  - **Migrar a:** `Codigo/Test_Estadisticos/Congruencia_Ideologica.py`

- [ ] **2.4.2. Wilcoxon pareado - Por categoría** (Notebook 52)
  - **Test:** Wilcoxon signed-rank test (pareado)
  - **Comparaciones:** Congruente vs Incongruente para cada una de las 6 categorías
  - **Resultados esperados:**
    - Generales: 8 de 12 significativas
    - Ballotage: 3 de 12 significativas
  - **Migrar a:** `Codigo/Test_Estadisticos/Congruencia_Ideologica.py`

#### 2.5. Validación Cruzada y Diferencia de Diferencias

- [ ] **2.5.1. Filtrado cruzado entre elecciones** (Notebook 53)
  - Identificar ítems robustos (significativos en ambas elecciones)
  - **Resultados esperados:**
    - Generales: 14 ítems CT robustos (35%)
    - Ballotage: 5 ítems CT robustos (12.5%)
  - **Migrar a:** `Codigo/Test_Estadisticos/Validacion_Cruzada.py`

- [ ] **2.5.2. Análisis de diferencia de diferencias** (Notebooks 49-50)
  - Cuantificación de cambios entre Generales y Ballotage
  - Análisis general y segmentado por población
  - **Migrar a:** `Codigo/Test_Estadisticos/Diferencia_Diferencias.py`

#### 2.6. Correlaciones

- [ ] **2.6.1. Matrices de correlación de Spearman** (Notebook 54)
  - **Test:** Correlación de Spearman
  - Entre predictores y outcomes
  - **Migrar a:** `Codigo/Modelado_Estadistico/Correlaciones.py`

#### 2.7. Exportación de Resultados Estadísticos

- [ ] **2.7.1. Tablas de resultados en Excel** (Notebooks 26, 41-47)
  - Exportar todos los resultados de tests a Excel
  - Tablas formateadas y organizadas
  - **Migrar a:** `Codigo/Utilidades/Exportar_Resultados.py`

---

### ETAPA 3: MODELADO ESTADÍSTICO

#### 3.1. Preparación para Modelado

- [ ] **3.1.1. Funciones de carga de datos** (Modelos/1)
  - Cargar bases finales de Generales y Ballotage
  - **Migrar a:** `Codigo/Utilidades/Preparacion_Modelado.py`

- [ ] **3.1.2. Definición de variables** (Modelos/2)
  - Listas de variables dependientes e independientes
  - **Migrar a:** `Codigo/Utilidades/Preparacion_Modelado.py`

- [ ] **3.1.3. Análisis exploratorio** (Modelos/3)
  - Distribuciones de variables dependientes
  - **Migrar a:** `Codigo/Utilidades/Preparacion_Modelado.py`

- [ ] **3.1.4. Limpieza y estructuración** (Modelos/4)
  - Preparar datos para ajuste de modelos
  - **Migrar a:** `Codigo/Utilidades/Preparacion_Modelado.py`

- [ ] **3.1.5. Conversión de variables** (Modelos/5)
  - Codificación de categóricas a numéricas
  - Conversión de booleanas
  - **Migrar a:** `Codigo/Utilidades/Preparacion_Modelado.py`

#### 3.2. Modelos GLM de Variables Ideológicas

- [ ] **3.2.1. GLM Índice de Progresismo** (Modelos/10)
  - **Variable dependiente:** `Indice_Progresismo`
  - **Familia:** Gaussiana con link identity
  - **Proceso:** Ajuste recursivo hasta convergencia
  - **Resultados esperados:** R² ~61-64%
  - **Migrar a:** `Codigo/Modelado_Estadistico/GLM_Progresismo.py`

- [ ] **3.2.2. GLM Índice de Conservadurismo** (Modelos/11)
  - **Variable dependiente:** `Indice_Conservadurismo`
  - **Familia:** Gamma con link log
  - **Resultados esperados:** R² ~62-65%
  - **Migrar a:** `Codigo/Modelado_Estadistico/GLM_Conservadurismo.py`

- [ ] **3.2.3. GLM Autopercepción Izq-Der** (Modelos/12)
  - **Variable dependiente:** `Autopercepcion_Izq_Der`
  - **Migrar a:** `Codigo/Modelado_Estadistico/GLM_Autopercepcion.py`

- [ ] **3.2.4. GLM Autopercepción Con-Pro** (Modelos/13)
  - **Variable dependiente:** `Autopercepcion_Con_Pro`
  - **Migrar a:** `Codigo/Modelado_Estadistico/GLM_Autopercepcion.py`

- [ ] **3.2.5. GLM Autopercepción Per-Antiper** (Modelos/14)
  - **Variable dependiente:** `Autopercepcion_Per_Antiper`
  - **Migrar a:** `Codigo/Modelado_Estadistico/GLM_Autopercepcion.py`

#### 3.3. Modelos de Regresión Logística Binaria

- [ ] **3.3.1. Regresión Logística Cercanía a Massa** (Modelos/15)
  - **Variable:** `Cercano_Massa` (binarizada: ≥4 = 1, ≤3 = 0)
  - **Familia:** Binomial
  - **Outputs:** OR, IC 95%, Pseudo R² McFadden
  - **Resultados esperados:** Pseudo R² ~26-31%
  - **Migrar a:** `Codigo/Modelado_Estadistico/Regresion_Logistica_Cercania.py`

- [ ] **3.3.2. Regresión Logística Cercanía a Milei** (Modelos/16)
  - **Variable:** `Cercano_Milei`
  - **Migrar a:** `Codigo/Modelado_Estadistico/Regresion_Logistica_Cercania.py`

- [ ] **3.3.3. Regresión Logística Cercanía a Schiaretti** (Modelos/17)
  - **Variable:** `Cercano_Schiaretti`
  - **Migrar a:** `Codigo/Modelado_Estadistico/Regresion_Logistica_Cercania.py`

- [ ] **3.3.4. Regresión Logística Cercanía a Bullrich** (Modelos/18)
  - **Variable:** `Cercano_Bullrich`
  - **Migrar a:** `Codigo/Modelado_Estadistico/Regresion_Logistica_Cercania.py`

- [ ] **3.3.5. Regresión Logística Cercanía a Bregman** (Modelos/19)
  - **Variable:** `Cercano_Bregman`
  - **Migrar a:** `Codigo/Modelado_Estadistico/Regresion_Logistica_Cercania.py`

#### 3.4. Modelos Robustos

- [ ] **3.4.1. Función de modelo robusto** (Modelos/6)
  - Regresión lineal con errores estándar robustos HC3
  - Detección de outliers (Cook, leverage, residuos studentizados)
  - Eliminación por multicolinealidad (VIF > 5.0)
  - Selección de variables (AIC, BIC, p-valor)
  - Diagnósticos (Jarque-Bera, Breusch-Pagan, Durbin-Watson)
  - **Migrar a:** `Codigo/Modelado_Estadistico/Modelo_Robusto.py`

- [ ] **3.4.2. Función de evaluación de modelo robusto** (Modelos/7)
  - Evaluación de calidad de ajuste
  - **Migrar a:** `Codigo/Modelado_Estadistico/Modelo_Robusto.py`

- [ ] **3.4.3. Pipeline de modelos robustos** (Modelos/8)
  - Ejecutar modelos para TODAS las variables dependientes:
    - **Generales:** CO_Congruente, CO_Incongruente, CT_Congruente, CT_Incongruente, CO_Pro, CO_Con, CO_Pro_Der, CO_Con_Der, CO_Pro_Izq, CO_Con_Izq, + 11 ítems CO significativos
    - **Ballotage:** CO_Congruente, CO_Incongruente, CT_Congruente, CT_Incongruente, CO_Pro, CO_Con, CO_Pro_Der, CO_Con_Der, CO_Pro_Izq, CO_Con_Izq, + 9 ítems CO significativos
  - **Migrar a:** `Codigo/Modelado_Estadistico/Pipeline_Modelos_Robustos.py`

- [ ] **3.4.4. Generación de tablas de resultados** (Modelos/9)
  - Tablas resumen de todos los modelos robustos
  - **Migrar a:** `Codigo/Modelado_Estadistico/Pipeline_Modelos_Robustos.py`

---

### ETAPA 4: VISUALIZACIONES

#### 4.1. Gráficos de Cleveland

- [ ] **4.1.1. Cleveland plots de diferencias CO** (Notebooks 60-64, 70)
  - Visualización de diferencias entre categorías para CO
  - **Migrar a:** `Codigo/Visualizacion/Graficos_Cleveland.py`

- [ ] **4.1.2. Cleveland plots de diferencias CT** (Notebooks 60-64, 70)
  - Visualización de diferencias entre categorías para CT
  - **Migrar a:** `Codigo/Visualizacion/Graficos_Cleveland.py`

#### 4.2. Heatmaps

- [ ] **4.2.1. Heatmaps de correlaciones** (Notebooks 68-69)
  - Matrices de correlación de Spearman visualizadas
  - **Migrar a:** `Codigo/Visualizacion/Heatmaps.py`

#### 4.3. Gráficos de Barras

- [ ] **4.3.1. Gráficos de barras comparativos**
  - Comparaciones por categoría ideológica
  - **Migrar a:** `Codigo/Visualizacion/Graficos_Barras.py`

#### 4.4. Gráficos de Violín

- [ ] **4.4.1. Violin plots de distribuciones**
  - Distribuciones por grupo ideológico
  - **Migrar a:** `Codigo/Visualizacion/Graficos_Violin.py`

#### 4.5. Exportación de Gráficos

- [ ] **4.5.1. Guardado en formatos de alta calidad**
  - SVG para gráficos principales
  - PNG para visualizaciones complementarias
  - Organizados en carpetas por tipo

---

### ETAPA 5: REPORTES Y EXPORTACIÓN DE RESULTADOS

#### 5.1. Tablas de Resultados de Tests Estadísticos

- [ ] **5.1.1. Tablas de Kruskal-Wallis** (Notebooks 21, 23, 29-30, 35-36, 38-39)
  - Resultados de comparaciones entre grupos
  - Estadísticos H, p-valores, significancia
  - Formato Excel con formato condicional
  - **Migrar a:** `Codigo/Utilidades/Exportar_Resultados.py`

- [ ] **5.1.2. Tablas de post-hoc Dunn** (Notebooks 22, 24)
  - Matrices de comparaciones pareadas
  - P-valores ajustados por Holm
  - Identificación de pares significativos
  - **Migrar a:** `Codigo/Utilidades/Exportar_Resultados.py`

- [ ] **5.1.3. Tablas de congruencia ideológica** (Notebook 52)
  - Resultados Wilcoxon población general y por categoría
  - Estadísticos W, p-valores, medias por grupo
  - **Migrar a:** `Codigo/Utilidades/Exportar_Resultados.py`

- [ ] **5.1.4. Tablas de validación cruzada** (Notebook 53)
  - Ítems robustos (significativos en ambas elecciones)
  - Comparación de resultados entre Generales y Ballotage
  - **Migrar a:** `Codigo/Utilidades/Exportar_Resultados.py`

#### 5.2. Tablas de Resultados de Modelos

- [ ] **5.2.1. Resumen de modelos GLM** (Modelos/10-14)
  - Tabla consolidada con R², AIC, BIC, F-estadístico
  - Variables significativas por modelo
  - Coeficientes e intervalos de confianza
  - **Migrar a:** `Codigo/Modelado_Estadistico/Pipeline_GLM.py`

- [ ] **5.2.2. Resumen de modelos logísticos** (Modelos/15-19)
  - Tabla consolidada con Pseudo R², AIC, BIC, χ²
  - Odds Ratios e intervalos de confianza
  - Variables significativas por candidato
  - **Migrar a:** `Codigo/Modelado_Estadistico/Pipeline_Regresion_Logistica.py`

- [ ] **5.2.3. Resumen de modelos robustos** (Modelos/9)
  - Tabla consolidada de todos los modelos robustos
  - R² ajustado, AIC, BIC, diagnósticos
  - Variables significativas por variable dependiente
  - Comparación entre Generales y Ballotage
  - **Migrar a:** `Codigo/Modelado_Estadistico/Pipeline_Modelos_Robustos.py`

#### 5.3. Tablas de Matrices de Correlación

- [ ] **5.3.1. Matrices de Spearman** (Notebook 54)
  - Correlaciones entre todas las variables
  - P-valores y significancia
  - Exportación a Excel con formato condicional
  - **Migrar a:** `Codigo/Modelado_Estadistico/Correlaciones.py`

#### 5.4. Documentos de Resultados Consolidados

- [ ] **5.4.1. Resumen ejecutivo de análisis** (Notebooks 26, 41-47)
  - Documento Word/Excel con todos los hallazgos principales
  - Tablas de resultados significativos
  - Interpretaciones estadísticas
  - **Migrar a:** `Codigo/Utilidades/Generar_Resumen_Ejecutivo.py`

- [ ] **5.4.2. Bases de datos finales exportadas** (Notebooks 14, 43)
  - Excel con todas las variables calculadas
  - Documentación de variables (diccionario de datos)
  - Metadatos (fecha, N observaciones, variables incluidas)
  - **Migrar a:** `Codigo/Procesamiento/Pipeline_Completo.py`

---

### ETAPA 6: CONTROLES DE CALIDAD Y VALIDACIÓN

**PRINCIPIO FUNDAMENTAL:** Todos los controles deben verificar que el código migrado funciona correctamente Y que produce exactamente los mismos resultados que los notebooks originales.

#### 6.1. Controles de Integridad de Datos (Después de cada sub-etapa de Etapa 1)

- [ ] **6.1.1. Control tras construcción inicial**
  - **Verificar funcionamiento:**
    - N observaciones coincide con esperado (2786 Generales, 1254 Ballotage)
    - Estructura de columnas esperadas existe
    - Ausencia de duplicados por ID
    - Tipos de datos correctos
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks 1-2 y comparar shapes de DataFrames
    - Verificar que columnas son idénticas
    - Comparar primeras/últimas filas de datos
    - Verificar que IDs coinciden exactamente
  - **Implementar en:** `Codigo/Utilidades/Controles_Calidad.py`

- [ ] **6.1.2. Control tras limpieza y eliminación de outliers**
  - **Verificar funcionamiento:**
    - Cantidad de outliers detectados y eliminados por variable
    - Rangos válidos de variables tras limpieza
    - Estadísticos descriptivos razonables
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks 15-17 y comparar N observaciones tras limpieza
    - Verificar que outliers eliminados son los mismos (mismos IDs)
    - Comparar estadísticos descriptivos (media, mediana, DE) con tolerancia ±0.001
  - **Implementar en:** `Codigo/Utilidades/Controles_Calidad.py`

- [ ] **6.1.3. Control tras imputación**
  - **Verificar funcionamiento:**
    - No quedan valores faltantes en variables críticas
    - Medianas usadas son correctas por categoría
    - Cantidad de valores imputados documentada por variable
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks 15-17 y comparar conteo de NaN antes/después
    - Verificar que medianas calculadas son idénticas
    - Comparar valores imputados (mismas filas, mismos valores)
  - **Implementar en:** `Codigo/Utilidades/Controles_Calidad.py`

- [ ] **6.1.4. Control tras cálculo de índices**
  - **Verificar funcionamiento:**
    - Rangos válidos de índices (mín, máx esperados)
    - Distribuciones coherentes (media, mediana, DE)
    - No hay valores NaN inesperados
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks 3-8 y comparar índices calculados fila por fila
    - Verificar estadísticos descriptivos idénticos (tolerancia ±0.0001)
    - Comparar histogramas de distribuciones
  - **Implementar en:** `Codigo/Utilidades/Controles_Calidad.py`

- [ ] **6.1.5. Control tras variables de cambio**
  - **Verificar funcionamiento:**
    - Todas las variables CO/CT esperadas existen
    - Coherencia matemática (CO_Pro = suma de CO_Items progresistas)
    - Ausencia de valores imposibles
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks 18-19 y comparar todas las variables CO/CT fila por fila
    - Verificar que agregaciones dan exactamente los mismos valores
    - Comparar estadísticos descriptivos de cada variable
  - **Implementar en:** `Codigo/Utilidades/Controles_Calidad.py`

#### 6.2. Controles de Resultados Estadísticos (Etapa 2)

- [ ] **6.2.1. Validación de tests Kruskal-Wallis**
  - **Verificar funcionamiento:**
    - Tests ejecutados sin errores
    - P-valores en rango válido [0, 1]
    - Variables significativas identificadas correctamente
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks 21, 23, 29-30, 35-36, 38-39
    - Comparar estadísticos H (deben ser idénticos hasta 6 decimales)
    - Comparar p-valores (deben ser idénticos hasta 6 decimales)
    - Verificar mismas variables identificadas como significativas
  - **Resultados esperados:**
    - Generales: 11 ítems CO significativos
    - Ballotage: 9 ítems CO significativos
  - **Implementar en:** `Codigo/Test_Estadisticos/Validar_Resultados.py`

- [ ] **6.2.2. Validación de tests post-hoc Dunn**
  - **Verificar funcionamiento:**
    - Matrices de p-valores completas
    - Corrección de Holm aplicada
    - Pares significativos identificados
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks 22, 24
    - Comparar matrices de p-valores elemento por elemento
    - Verificar mismos pares significativos identificados
    - Comparar conteo de comparaciones significativas
  - **Implementar en:** `Codigo/Test_Estadisticos/Validar_Resultados.py`

- [ ] **6.2.3. Validación de congruencia ideológica**
  - **Verificar funcionamiento:**
    - Tests Wilcoxon ejecutados correctamente
    - Estadísticos W calculados
    - Significancia identificada
  - **Comparar con notebooks originales:**
    - Ejecutar notebook 52
    - Comparar estadísticos W de Wilcoxon (idénticos hasta 6 decimales)
    - Comparar p-valores (idénticos hasta 6 decimales)
    - Verificar conteo correcto de comparaciones significativas
  - **Resultados esperados:**
    - Generales general: 4/4 significativas
    - Generales categoría: 8/12 significativas
    - Ballotage general: 4/4 significativas
    - Ballotage categoría: 3/12 significativas
  - **Implementar en:** `Codigo/Test_Estadisticos/Validar_Resultados.py`

- [ ] **6.2.4. Validación de validación cruzada**
  - **Verificar funcionamiento:**
    - Ítems robustos identificados correctamente
    - Coherencia entre elecciones
  - **Comparar con notebooks originales:**
    - Ejecutar notebook 53
    - Comparar listas de ítems robustos (deben ser idénticas)
    - Verificar conteos esperados (14 ítems Generales, 5 ítems Ballotage)
  - **Implementar en:** `Codigo/Test_Estadisticos/Validar_Resultados.py`

#### 6.3. Controles de Modelos (Etapa 3)

- [ ] **6.3.1. Validación de modelos GLM**
  - **Verificar funcionamiento:**
    - Convergencia de todos los modelos
    - Variables significativas identificadas
    - Diagnósticos calculados
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks Modelos/10-14
    - Comparar R² ajustado (tolerancia ±0.0001)
    - Comparar AIC, BIC (tolerancia ±0.01)
    - Verificar mismas variables significativas
    - Comparar coeficientes (tolerancia ±0.0001)
    - Comparar errores estándar (tolerancia ±0.0001)
  - **Resultados esperados:**
    - Progresismo: R² 61-64%
    - Conservadurismo: R² 62-65%
  - **Implementar en:** `Codigo/Modelado_Estadistico/Validar_Modelos.py`

- [ ] **6.3.2. Validación de modelos logísticos**
  - **Verificar funcionamiento:**
    - Convergencia de modelos binarios
    - Odds Ratios calculados correctamente
    - IC 95% razonables
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks Modelos/15-19
    - Comparar Pseudo R² McFadden (tolerancia ±0.0001)
    - Comparar AIC, BIC, χ² (tolerancia ±0.01)
    - Comparar Odds Ratios e IC 95% (tolerancia ±0.001)
    - Verificar mismas variables significativas
  - **Resultados esperados:**
    - Massa: Pseudo R² 26-31%
  - **Implementar en:** `Codigo/Modelado_Estadistico/Validar_Modelos.py`

- [ ] **6.3.3. Validación de modelos robustos**
  - **Verificar funcionamiento:**
    - Pipeline ejecutado para todas las variables dependientes
    - Detección de outliers funcional
    - Eliminación por VIF aplicada
    - Diagnósticos completos
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks Modelos/6-9
    - Comparar R² ajustado para cada variable dependiente (tolerancia ±0.0001)
    - Verificar mismos outliers detectados (mismos índices)
    - Verificar mismas variables eliminadas por VIF
    - Comparar diagnósticos: Jarque-Bera, Breusch-Pagan, Durbin-Watson (tolerancia ±0.01)
    - Comparar variables significativas en cada modelo
  - **Implementar en:** `Codigo/Modelado_Estadistico/Validar_Modelos.py`

#### 6.4. Controles de Visualizaciones (Etapa 4)

- [ ] **6.4.1. Validación de gráficos**
  - **Verificar funcionamiento:**
    - Todos los gráficos se generan sin errores
    - Exportación correcta en formatos SVG y PNG
    - Organización en carpetas correcta
  - **Comparar con notebooks originales:**
    - Ejecutar notebooks 60-64, 68-70
    - Comparar visualmente gráficos generados con originales
    - Verificar que datos graficados son idénticos (extraer valores de gráficos)
    - Comparar títulos, etiquetas, leyendas
  - **Implementar en:** `Codigo/Visualizacion/Validar_Graficos.py`

#### 6.5. Control Final de Pipeline Completo

- [ ] **6.5.1. Ejecución end-to-end**
  - **Verificar funcionamiento:**
    - Pipeline completo ejecuta desde JSON hasta reportes finales
    - Todos los outputs se generan correctamente
    - Sin errores ni warnings críticos
    - Tiempo de ejecución razonable por etapa
  - **Comparar con notebooks originales:**
    - Ejecutar TODOS los notebooks en orden
    - Comparar bases de datos finales fila por fila, columna por columna
    - Comparar todos los archivos Excel generados
    - Comparar todos los resultados estadísticos
    - Comparar todos los resultados de modelos
  - **Implementar en:** `Pipeline_Completo_Con_Validacion.py`

- [ ] **6.5.2. Reporte de validación final**
  - **Generar documento consolidado:**
    - Checklist de todos los controles ejecutados y pasados
    - Tabla comparativa de todos los resultados clave
    - Documentación de cualquier diferencia encontrada (debe ser CERO)
    - Si hay diferencias, justificación técnica y decisión tomada
    - Firma de aprobación: "Migración validada exitosamente"
  - **Generar en:** `Reportes/Validacion_Migracion_Completa.xlsx`

---

## Variables Clave del Estudio

**Variables Dependientes:**
- `CO` (Cambio de Opinión): Diferencia en respuesta base vs con candidato asociado
- `CT` (Cambio de Tiempo): Diferencia en tiempo de respuesta base vs con candidato
- `CO_Congruente` / `CO_Incongruente`: Cambios de opinión según congruencia ideológica
- `CT_Congruente` / `CT_Incongruente`: Cambios de tiempo según congruencia ideológica
- `CO_Pro` / `CO_Con`: Cambios de opinión por tipo de ítem (progresista/conservador)
- `CO_Pro_Izq` / `CO_Pro_Der` / `CO_Con_Izq` / `CO_Con_Der`: Cambios de opinión por tipo de ítem y candidato

**Predictores Principales:**
- `Indice_Progresismo`: Caracterización operativa de orientación progresista
- `Indice_Conservadurismo`: Caracterización operativa de orientación conservadora
- `Autopercepcion_Izq_Der`: Autopercepción ideológica Izquierda-Derecha
- `Autopercepcion_Con_Pro`: Autopercepción Conservador-Progresista
- `Autopercepcion_Per_Antiper`: Autopercepción Peronista-Antiperonista
- `Cercania_[Candidato]`: Cercanía percibida a cada candidato (Massa, Milei, Bullrich, Schiaretti, Bregman)

**Clusters:**
- `Conservative_Cluster`: Pertenencia a cluster conservador (calculado externamente)
- `Progressive_Cluster`: Pertenencia a cluster progresista (calculado externamente)

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

**Variables de Control:**
- Demográficas: Edad, Género, Región, Nivel educativo, Estrato social
- Electorales: Voto 2019, Categoría PASO 2023
- Consumo de medios: Redes sociales, Medios de prensa, Influencia

## Principios de Migración

### REGLA DE ORO: EXACTITUD DE RESULTADOS

**CRÍTICO**: Cada paso migrado debe producir EXACTAMENTE los mismos resultados que los notebooks originales. No se permite ninguna desviación.

### Metodología de Migración

1. **Leer notebook original completo**
2. **Identificar código reutilizable**
3. **Extraer a función con nombre descriptivo en Pascal_Snake_Case**
4. **Agregar docstring exhaustivo**
5. **Colocar en módulo apropiado bajo `Codigo/`**
6. **Usar comentarios separadores `# ====...====`**
7. **Mantener notebook original sin cambios**
8. **Validar que resultados sean idénticos**

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
- `Procesamiento_Datos.py`, `Modelos_GLM.py`
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

    """
    Descripción.

    """

    pass


# ============================================================
# FUNCIONES PRINCIPALES
# ============================================================

def Funcion_Principal():

    """
    Descripción.

    """

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

## Dependencias Principales

```python
pandas           # Manipulación de datos
numpy            # Cálculos numéricos
matplotlib       # Visualizaciones base
seaborn          # Gráficos estadísticos
scipy            # Tests estadísticos (kruskal, wilcoxon, spearmanr)
scikit_posthocs  # Prueba de Dunn post-hoc
statsmodels      # GLM, regresión logística, modelos robustos
sklearn          # Preprocessing
openpyxl         # Exportación a Excel
```

## Tests Estadísticos Utilizados

**IMPORTANTE:** Usar EXACTAMENTE los mismos tests que en los notebooks originales. Los tests documentados aquí son los que se usan en el proyecto original:

- **Kruskal-Wallis H test** (`scipy.stats.kruskal`): Para comparaciones entre múltiples grupos (>2)
- **Prueba de Dunn post-hoc** (`scikit_posthocs.posthoc_dunn`) con corrección de Holm: Tras Kruskal-Wallis significativo
- **Wilcoxon signed-rank test** (`scipy.stats.wilcoxon`): Para comparaciones pareadas (congruente vs incongruente)
- **Correlación de Spearman** (`scipy.stats.spearmanr`): Para correlaciones no paramétricas

## Formatos de Salida

- **Excel (.xlsx)**: Tablas de resultados, bases procesadas
- **SVG**: Gráficos de alta calidad (Cleveland, heatmaps)
- **PNG**: Visualizaciones complementarias
- **CSV**: Exportaciones específicas de subconjuntos

## Resultados Esperados (Validación)

Para verificar que la migración es correcta, los resultados deben coincidir con:

### Congruencia Ideológica
- **Generales población general**: 4 de 4 comparaciones significativas (CO y CT)
- **Generales por categoría**: 8 de 12 comparaciones significativas (CO y CT)
- **Ballotage población general**: 4 de 4 comparaciones significativas
- **Ballotage por categoría**: 3 de 12 comparaciones significativas

### Modelos GLM
- **Progresismo**: R² ~61-64% en ambas elecciones
- **Conservadurismo**: R² ~62-65% en ambas elecciones

### Modelos de Cercanía (Regresión Logística)
- **Massa**: Pseudo R² ~26-31%

### Tests de Ítems Individuales (Kruskal-Wallis)
- **Generales**: 11 ítems CO significativos
- **Ballotage**: 9 ítems CO significativos

### Validación Cruzada
- **Generales**: 14 ítems CT robustos (35%)
- **Ballotage**: 5 ítems CT robustos (12.5%)

## Datos del Estudio

- **Participantes**: ~2786 en Generales, ~1254 en Ballotage
- **Items IP**: 20 ítems de personalidad implícita evaluados con/sin candidatos
- **Variables de control**: Demográficas, electorales, consumo de medios, variables situacionales

## Comandos para Ejecutar Pipeline

```bash
# Ejecutar procesamiento completo
python Codigo/Procesamiento/Pipeline_Completo.py

# Ejecutar tests estadísticos
python Codigo/Test_Estadisticos/Pipeline_Tests.py

# Ejecutar modelos GLM
python Codigo/Modelado_Estadistico/Pipeline_GLM.py

# Ejecutar modelos robustos
python Codigo/Modelado_Estadistico/Pipeline_Modelos_Robustos.py

# Generar todas las visualizaciones
python Codigo/Visualizacion/Generar_Todos_Graficos.py
```

## Documentación de Progreso por Sesión

### Sesión 2025-01-15
- **Actividad:** Creación de CLAUDE.md para Tesis_Ordenada con estructura jerárquica de etapas
- **Estado:** Documentación completa con checkboxes de progreso
- **Estructura:** 4 etapas principales desglosadas en sub-etapas detalladas
- **Correcciones:**
  - Orden corregido: Imputación de medianas ANTES de cálculo de índices
  - Clustering: Solo incorporación de variables calculadas externamente (no cálculo)
- **Tests documentados:** Kruskal-Wallis, Dunn post-hoc, Wilcoxon pareado, Spearman
- **Modelos documentados:** 23 notebooks en Modelos/ (GLM, Logísticos, Robustos)
- **Variables:** Todas las variables dependientes e independientes catalogadas
- **Próximos pasos:** Migrar Etapa 1.6 en adelante (variables agregadas y filtradas)
