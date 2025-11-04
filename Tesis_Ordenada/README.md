# Tesis_Ordenada

Proyecto reorganizado de tesis sobre psicología política: análisis de cómo la ideología influye en cambios de opinión y tiempos de respuesta durante las elecciones argentinas 2023.

## Estructura del Proyecto

```
Tesis_Ordenada/
├── Codigo/
│   ├── Procesamiento/           # Construcción y preparación de datos
│   ├── Test_Estadisticos/       # Tests Mann-Whitney y análisis
│   ├── Modelado_Estadistico/    # Modelos SEM y correlaciones
│   ├── Visualizacion/           # Generación de gráficos
│   └── Utilidades/              # Configuración y funciones comunes
├── Data/
│   ├── Datos_Crudos/           # CSVs originales del experimento
│   └── Datos_Procesados/       # Bases procesadas
├── Graficos/                    # Visualizaciones generadas
│   ├── Cleveland/
│   ├── Heatmaps/
│   ├── Violin/
│   └── Barras/
├── Tablas/                      # Resultados exportados
│   ├── Resultados_Tests/
│   ├── Resultados_SEM/
│   └── Bases_Procesadas/
├── Notebooks/                   # Notebooks de análisis
│   ├── Exploracion/
│   └── Analisis_Final/
└── Scripts/                     # Scripts ejecutables
```

## Inicio Rápido

### Ejecutar Pipeline Completo

```bash
cd Scripts
python Ejecutar_Pipeline_Completo.py
```

### Usar Módulos Individuales

```python
# Construcción de bases.
from Codigo.Procesamiento.Construccion_Bases import (
    Ejecutar_Construccion_Bases
)
Ejecutar_Construccion_Bases()

# Cálculo de índices.
from Codigo.Procesamiento.Calculo_Indices import (
    Calcular_Todos_Indices
)
Df_Con_Indices = Calcular_Todos_Indices(Df)

# Tests estadísticos.
from Codigo.Test_Estadisticos.Mann_Whitney import (
    Ejecutar_Mann_Whitney
)
Resultado = Ejecutar_Mann_Whitney(Df, 'CO_Item_3_Izq', [...], [...])
```

## Configuración

Todas las constantes y rutas están centralizadas en:
```
Codigo/Utilidades/Configuracion.py
```

### Parámetros Principales

- **ALPHA**: 0.05 (nivel de significancia)
- **NUM_DESVIACIONES_OUTLIERS**: 3
- **ITEMS_PROGRESISTAS**: [3, 4, 5, 6, 7, 9, 10, 16, 22, 24]
- **ITEMS_CONSERVADORES**: [8, 11, 19, 20, 23, 25, 27, 28, 29, 30]

## Variables del Estudio

### Variables Dependientes

- **CO (Cambio de Opinión)**: Diferencia en respuesta base vs con candidato
- **CT (Cambio de Tiempo)**: Diferencia en tiempo de respuesta

### Predictores

- **Índice de Progresismo**: Promedio de respuestas a items progresistas
- **Índice de Conservadurismo**: Promedio de respuestas a items conservadores

### Categorías Ideológicas

- Left_Wing
- Progressivism
- Centre
- Moderate_Right_A
- Moderate_Right_B
- Right_Wing_Libertarian

## Análisis Principales

1. **Tests Mann-Whitney**: Comparaciones entre grupos ideológicos
2. **Modelos SEM**: Predicción de CO y CT desde índices ideológicos
3. **Análisis de Congruencia**: Cambios congruentes vs incongruentes
4. **Diferencia de Diferencias**: Cambios entre Generales y Ballotage

## Convenciones de Código

- **Nomenclatura**: Pascal_Snake_Case para TODO
- **Idioma**: Español en código y documentación
- **Límite de línea**: 70 caracteres
- **Docstrings**: Obligatorios con descripción detallada

Ejemplo:
```python
def Calcular_Total(Lista_Valores: list) -> float:

    """
    Calcula el total sumando todos los valores de una lista.

    Parámetros:
    - Lista_Valores: Lista de números a sumar.

    Retorna:
    - Suma total de los valores.

    """

    return sum(Lista_Valores)
```

## Dependencias

```
pandas
numpy
matplotlib
seaborn
scipy
semopy
openpyxl
```

Instalar con:
```bash
pip install pandas numpy matplotlib seaborn scipy semopy openpyxl
```

## Datos

- **Participantes Generales**: ~2786
- **Participantes Ballotage**: ~1254
- **Items IP evaluados**: 20 (10 progresistas, 10 conservadores)

## Contacto

Para más información, consultar el CLAUDE.md en la raíz del proyecto.
