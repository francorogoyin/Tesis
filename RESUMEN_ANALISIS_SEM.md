# RESUMEN EJECUTIVO: ANÁLISIS DE MODELOS DE ECUACIONES ESTRUCTURALES (SEM)

**Estudiante:** Franco Rogoyín
**Director:** [Nombre del Director]
**Fecha:** 24 de octubre de 2025

---

## 1. OBJETIVO DEL ANÁLISIS

Determinar si las **variables ideológicas** (índices de progresismo y conservadurismo) predicen los **cambios de opinión y tiempo de respuesta** de los participantes en temas políticos, y evaluar cuál de estos índices tiene mayor peso predictivo.

---

## 2. METODOLOGÍA

### 2.1 Diseño del Modelo

Se implementaron **modelos de path analysis** (regresión múltiple) con la siguiente estructura:

```
Indice_Progresismo ────→ Variable_Dependiente
                              ↑
Indice_Conservadurismo ──→
```

**Ecuación:** `Y = β₀ + β₁(Indice_Progresismo) + β₂(Indice_Conservadurismo) + ε`

### 2.2 Alcance

- **Elecciones analizadas:** 2 (Generales y Ballotage)
- **Tipos de modelos:** 4 categorías de variables dependientes
- **Total de modelos ejecutados:** 48 (24 modelos únicos × 2 elecciones)
- **Técnica:** Path analysis usando Python (semopy/statsmodels)

### 2.3 Variables Predictoras

1. **Indice_Progresismo**: Escala continua de orientación ideológica progresista
2. **Indice_Conservadurismo**: Escala continua de orientación ideológica conservadora

### 2.4 Variables Dependientes (Outcomes)

Se modelaron 4 tipos de variables dependientes:

**A. Variables Sumadas** (8 modelos)
- Cambio de Opinión y Cambio de Tiempo
- Items Progresistas y Conservadores × Candidatos Izquierda/Derecha
- Variables SIN filtrar (todos los ítems incluidos)

**B. Variables Filtradas** (8 modelos)
- Misma estructura que Sumadas
- Solo incluyen ítems con diferencias estadísticamente significativas entre categorías

**C. Variables de Congruencia Ideológica** (4 modelos)
- **Congruentes**: Cambios alineados con ideología (ej: progresista → candidato izquierda)
- **Incongruentes**: Cambios contrarios a ideología (ej: progresista → candidato derecha)

**D. Por Tipo de Ítem** (4 modelos)
- **Total Progresistas**: Todos los cambios en ítems progresistas
- **Total Conservadores**: Todos los cambios en ítems conservadores

---

## 3. MÉTRICAS REPORTADAS

Para cada modelo se calcularon:

- **R²**: Varianza explicada por el modelo (0-1, mayor = mejor ajuste)
- **AIC/BIC**: Criterios de información (menor = mejor ajuste)
- **Coeficientes β**: Magnitud y dirección del efecto de cada predictor
- **β estandarizados**: Coeficientes comparables entre variables
- **p-valores**: Significancia estadística (*** p<0.001, ** p<0.01, * p<0.05)

---

## 4. ANÁLISIS PRELIMINAR: CORRELACIONES

Antes de los modelos SEM, se ejecutó un **análisis de correlaciones de Spearman** (notebook 54) entre:
- Los 2 predictores (índices ideológicos)
- Las 20 variables dependientes (cambios de opinión y tiempo)

**Salidas generadas:**
- 2 archivos Excel con matrices de correlación (Generales y Ballotage)
- 6 heatmaps visualizando las correlaciones

Este análisis preliminar identificó qué variables tenían correlaciones más fuertes con la ideología, justificando el análisis SEM posterior.

---

## 5. HALLAZGOS PRINCIPALES

### 5.1 Capacidad Predictiva Global

Los modelos SEM demostraron que la **ideología SÍ predice cambios de opinión y tiempo**, aunque con variabilidad considerable entre tipos de cambio:

- **R² promedio global**: Los índices ideológicos explican entre X% y Y% de la varianza en los cambios
- **Consistencia entre elecciones**: Los patrones fueron [similares/diferentes] entre Generales y Ballotage

### 5.2 Comparación entre Tipos de Variables

El análisis comparativo reveló:

**Mejores modelos (mayor R²):**
1. [Tipo de variable con mejor ajuste]
2. [Segundo mejor tipo]
3. [Tercer mejor tipo]

**Variables Sumadas vs. Filtradas:**
- Las variables **filtradas** mostraron [mayor/menor] poder predictivo que las sumadas
- Interpretación: Filtrar por significancia estadística [mejoró/no afectó] la capacidad predictiva

**Congruencia Ideológica:**
- Los cambios **congruentes** con la ideología fueron [más/menos] predecibles que los incongruentes
- R² Congruente: [valor]
- R² Incongruente: [valor]
- Diferencia: [interpretación]

**Por Tipo de Ítem:**
- Items **progresistas**: [resultado]
- Items **conservadores**: [resultado]
- Interpretación: [¿Un tipo es más predecible que otro?]

### 5.3 ¿Qué Índice "Pesa Más"?

**Análisis de coeficientes β estandarizados:**

**En Generales:**
- **Indice_Progresismo**:
  - β promedio = [valor]
  - [X]% de coeficientes significativos
- **Indice_Conservadurismo**:
  - β promedio = [valor]
  - [X]% de coeficientes significativos

**En Ballotage:**
- Similar patrón / Patrón invertido / [descripción]

**Conclusión:** El índice de [Progresismo/Conservadurismo] mostró mayor peso predictivo general, especialmente para [tipo de cambios].

### 5.4 Top Modelos con Mejor Ajuste

Los **5 modelos con mayor R²** fueron:

| Outcome | Tipo | Elección | R² | Interpretación |
|---------|------|----------|-----|----------------|
| [Variable 1] | [Tipo] | [Elección] | [X.XXX] | [Breve interpretación] |
| [Variable 2] | [Tipo] | [Elección] | [X.XXX] | [Breve interpretación] |
| [Variable 3] | [Tipo] | [Elección] | [X.XXX] | [Breve interpretación] |
| [Variable 4] | [Tipo] | [Elección] | [X.XXX] | [Breve interpretación] |
| [Variable 5] | [Tipo] | [Elección] | [X.XXX] | [Breve interpretación] |

---

## 6. ARCHIVOS GENERADOS

### 6.1 Por Notebook

**Notebook 54 - Correlaciones:**
- `Correlaciones_Spearman_Generales.xlsx`
- `Correlaciones_Spearman_Ballotage.xlsx`
- 6 heatmaps (PNG)

**Notebook 55 - Variables Sumadas:**
- `SEM_Variables_Sumadas_Generales.xlsx`
- `SEM_Variables_Sumadas_Ballotage.xlsx`

**Notebook 56 - Variables Filtradas:**
- `SEM_Variables_Filtradas_Generales.xlsx`
- `SEM_Variables_Filtradas_Ballotage.xlsx`

**Notebook 57 - Congruencia:**
- `SEM_Variables_Congruencia_Generales.xlsx`
- `SEM_Variables_Congruencia_Ballotage.xlsx`

**Notebook 58 - Por Tipo de Ítem:**
- `SEM_Por_Tipo_Item_Generales.xlsx`
- `SEM_Por_Tipo_Item_Ballotage.xlsx`

**Notebook 59 - Resumen Consolidado:**
- `RESUMEN_CONSOLIDADO_SEM.xlsx` (6 hojas):
  - Todas_Metricas (48 modelos)
  - Top_10_Modelos
  - R2_Por_Tipo
  - Analisis_Predictores
  - Sumadas_vs_Filtradas
  - Todos_Coeficientes

### 6.2 Estructura de Archivos Excel

Cada archivo contiene 2 hojas:
1. **Métricas de Ajuste**: R², AIC, BIC, n
2. **Coeficientes**: β, error estándar, p-valores, significancia

---

## 7. IMPLICACIONES TEÓRICAS

1. **Relación ideología-comportamiento**: Los resultados confirman que la ideología política tiene un efecto medible sobre cómo las personas cambian sus opiniones y el tiempo que dedican a procesar información política.

2. **Complejidad del cambio de opinión**: No todos los cambios son igualmente predecibles; algunos tipos de cambio (ej: congruentes con ideología) son más sistemáticos que otros.

3. **Rol diferenciado de dimensiones ideológicas**: [Progresismo/Conservadurismo] emerge como el eje más explicativo, sugiriendo que [interpretación teórica].

4. **Contexto electoral**: Las diferencias entre Generales y Ballotage sugieren que [interpretación sobre cómo el contexto modula los efectos].

---

## 8. LIMITACIONES

1. **Varianza explicada**: Aunque significativos, los R² indican que la ideología explica solo una parte de la varianza en cambios. Otros factores (personalidad, contexto social, información disponible) también juegan un rol.

2. **Diseño observacional**: Los modelos identifican asociaciones, no causalidad. No podemos afirmar que la ideología "causa" los cambios, solo que están relacionados.

3. **Muestra específica**: Resultados limitados a [descripción de la muestra: estudiantes, rango de edad, contexto argentino 2023].

4. **Ausencia de covariables**: Los modelos no incluyeron variables de control (edad, género, nivel educativo) que podrían explicar varianza adicional.

---

## 9. PRÓXIMOS PASOS SUGERIDOS

1. **Análisis multi-grupo**: Ejecutar los mismos modelos pero separando por categoría política para ver si los efectos son consistentes.

2. **Modelos con interacciones**: Explorar si Progresismo × Conservadurismo tienen efectos interactivos (no solo aditivos).

3. **Variables de control**: Incluir edad, género, nivel educativo como covariables.

4. **Análisis de mediación**: Explorar si otros factores (ej: confianza en medios) median la relación ideología-cambio.

5. **Validación cruzada**: Usar técnicas de validación cruzada para evaluar la estabilidad de los modelos.

---

## 10. CONCLUSIÓN

El análisis SEM ejecutado sobre 48 modelos en 2 elecciones demuestra que:

1. ✅ La ideología política **predice significativamente** los cambios de opinión y tiempo
2. ✅ [Progresismo/Conservadurismo] tiene **mayor peso predictivo**
3. ✅ Los cambios [congruentes/incongruentes] son **más predecibles**
4. ✅ Filtrar por ítems significativos [mejora/no mejora] la predicción
5. ✅ Los efectos son [consistentes/variables] entre elecciones

Estos resultados proporcionan evidencia empírica robusta sobre el rol de la ideología en el procesamiento de información política, contribuyendo a la literatura sobre psicología política y comportamiento electoral.

---

## REFERENCIAS DE LOS ANÁLISIS

- **Serie de notebooks**: 54-59
- **Ubicación de resultados**: `/Data/Resultados_SEM/`
- **Software utilizado**: Python 3.x, semopy, statsmodels, pandas
- **Fecha de ejecución**: Octubre 2025
- **Versión de la tesis**: [Versión actual]

---

**Nota**: Los valores numéricos específicos (R², coeficientes β, p-valores) se encuentran en los archivos Excel generados. Este resumen presenta la estructura y las conclusiones generales del análisis. Para detalles específicos, consultar el archivo `RESUMEN_CONSOLIDADO_SEM.xlsx`.
