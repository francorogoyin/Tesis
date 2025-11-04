# ============================================================
# EXPORTAR_RESULTADOS.PY
# ============================================================
# Módulo para exportación automática de resultados de análisis
# a diferentes formatos (Excel, HTML, PDF).
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path
import sys
from typing import Dict, List, Optional
from datetime import datetime

sys.path.append(
    str(Path(__file__).parent)
)

from Configuracion import (
    RUTA_TABLAS,
    RUTA_GRAFICOS,
    ALPHA
)


# ============================================================
# EXPORTAR RESULTADOS A EXCEL
# ============================================================

def Exportar_Tests_A_Excel(
    Resultados: Dict[str, pd.DataFrame],
    Nombre_Archivo: str = "Resultados_Tests_Estadisticos"
) -> Path:

    """
    Exporta resultados de tests estadísticos a Excel con
    múltiples hojas.

    Parámetros:
    - Resultados: Diccionario con DataFrames de resultados.
      Formato: {'Nombre_Test': DataFrame, ...}
    - Nombre_Archivo: Nombre base del archivo (sin extensión).

    Retorna:
    - Path del archivo generado.

    """

    # Crear nombre con timestamp.
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    Nombre_Completo = f"{Nombre_Archivo}_{Timestamp}.xlsx"
    Ruta_Salida = RUTA_TABLAS / Nombre_Completo

    # Crear directorio si no existe.
    Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)

    # Exportar a Excel.
    with pd.ExcelWriter(
        Ruta_Salida,
        engine='openpyxl'
    ) as Writer:

        for Nombre_Hoja, Df in Resultados.items():
            # Limitar longitud del nombre de hoja (Excel max 31).
            Nombre_Hoja_Truncado = Nombre_Hoja[:31]

            Df.to_excel(
                Writer,
                sheet_name=Nombre_Hoja_Truncado,
                index=True
            )

    print(f"  ✓ Excel exportado: {Ruta_Salida.name}")

    return Ruta_Salida


# ============================================================
# CREAR RESUMEN DE ANÁLISIS
# ============================================================

def Crear_Resumen_Analisis(
    Resultados_Tests: Dict[str, pd.DataFrame],
    Resultados_Correlaciones: Optional[Dict] = None,
    Nombre_Dataset: str = "Dataset"
) -> pd.DataFrame:

    """
    Crea resumen consolidado de todos los análisis realizados.

    Parámetros:
    - Resultados_Tests: Diccionario con resultados de tests.
    - Resultados_Correlaciones: Diccionario con correlaciones
      (opcional).
    - Nombre_Dataset: Nombre del dataset analizado.

    Retorna:
    - DataFrame con resumen consolidado.

    """

    Resumen = {
        'Dataset': Nombre_Dataset,
        'Fecha_Analisis': datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        'Tests_Realizados': len(Resultados_Tests),
        'Total_Comparaciones': 0,
        'Comparaciones_Significativas': 0,
        'Porcentaje_Significativo': 0.0
    }

    # Contar comparaciones.
    for Nombre_Test, Df_Resultado in Resultados_Tests.items():
        if 'P_Valor' in Df_Resultado.columns:
            N_Comparaciones = len(Df_Resultado)
            N_Significativas = (
                Df_Resultado['P_Valor'] < ALPHA
            ).sum()

            Resumen['Total_Comparaciones'] += N_Comparaciones
            Resumen['Comparaciones_Significativas'] += (
                N_Significativas
            )

    # Calcular porcentaje.
    if Resumen['Total_Comparaciones'] > 0:
        Resumen['Porcentaje_Significativo'] = (
            100 * Resumen['Comparaciones_Significativas'] /
            Resumen['Total_Comparaciones']
        )

    # Agregar información de correlaciones si disponible.
    if Resultados_Correlaciones is not None:
        Resumen['Analisis_Correlacion'] = 'Sí'
    else:
        Resumen['Analisis_Correlacion'] = 'No'

    # Convertir a DataFrame.
    Df_Resumen = pd.DataFrame([Resumen])

    return Df_Resumen


# ============================================================
# GENERAR REPORTE HTML
# ============================================================

def Generar_Reporte_HTML(
    Resultados_Tests: Dict[str, pd.DataFrame],
    Df_Resumen: pd.DataFrame,
    Nombre_Archivo: str = "Reporte_Analisis",
    Incluir_Tablas_Completas: bool = False
) -> Path:

    """
    Genera reporte HTML con resumen de resultados.

    Parámetros:
    - Resultados_Tests: Diccionario con resultados de tests.
    - Df_Resumen: DataFrame con resumen del análisis.
    - Nombre_Archivo: Nombre base del archivo HTML.
    - Incluir_Tablas_Completas: Si incluir tablas completas
      en reporte.

    Retorna:
    - Path del archivo generado.

    """

    # Crear nombre con timestamp.
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    Nombre_Completo = f"{Nombre_Archivo}_{Timestamp}.html"
    Ruta_Salida = RUTA_TABLAS / Nombre_Completo

    # Crear directorio si no existe.
    Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)

    # Construir HTML.
    Html = []

    # Encabezado.
    Html.append("<!DOCTYPE html>")
    Html.append("<html lang='es'>")
    Html.append("<head>")
    Html.append("<meta charset='UTF-8'>")
    Html.append(
        "<meta name='viewport' "
        "content='width=device-width, initial-scale=1.0'>"
    )
    Html.append(
        "<title>Reporte de Análisis Estadístico</title>"
    )

    # CSS.
    Html.append("<style>")
    Html.append("body { font-family: Arial, sans-serif; "
                "margin: 20px; }")
    Html.append("h1 { color: #2c3e50; }")
    Html.append("h2 { color: #34495e; border-bottom: "
                "2px solid #3498db; padding-bottom: 5px; }")
    Html.append("table { border-collapse: collapse; "
                "width: 100%; margin: 20px 0; }")
    Html.append("th { background-color: #3498db; "
                "color: white; padding: 10px; text-align: left; }")
    Html.append("td { padding: 8px; border-bottom: "
                "1px solid #ddd; }")
    Html.append("tr:hover { background-color: #f5f5f5; }")
    Html.append(".significativo { color: #27ae60; "
                "font-weight: bold; }")
    Html.append(".no-significativo { color: #95a5a6; }")
    Html.append(".resumen { background-color: #ecf0f1; "
                "padding: 15px; border-radius: 5px; "
                "margin: 20px 0; }")
    Html.append("</style>")
    Html.append("</head>")

    Html.append("<body>")

    # Título.
    Html.append("<h1>Reporte de Análisis Estadístico</h1>")

    # Resumen.
    Html.append("<div class='resumen'>")
    Html.append("<h2>Resumen del Análisis</h2>")
    Html.append(Df_Resumen.to_html(index=False, escape=False))
    Html.append("</div>")

    # Tests realizados.
    Html.append("<h2>Tests Estadísticos Realizados</h2>")

    for Nombre_Test, Df_Resultado in Resultados_Tests.items():
        Html.append(f"<h3>{Nombre_Test}</h3>")

        if 'P_Valor' in Df_Resultado.columns:
            # Contar significativos.
            N_Sig = (Df_Resultado['P_Valor'] < ALPHA).sum()
            N_Total = len(Df_Resultado)

            Html.append(
                f"<p>Comparaciones significativas: "
                f"<strong>{N_Sig}/{N_Total}</strong> "
                f"({100*N_Sig/N_Total:.1f}%)</p>"
            )

            if Incluir_Tablas_Completas:
                # Tabla completa.
                Html.append(
                    Df_Resultado.head(20).to_html(
                        index=True,
                        escape=False
                    )
                )
                if len(Df_Resultado) > 20:
                    Html.append(
                        "<p><em>Mostrando primeras 20 filas "
                        "de {len(Df_Resultado)}.</em></p>"
                    )
            else:
                # Solo resultados significativos.
                Df_Sig = Df_Resultado[
                    Df_Resultado['P_Valor'] < ALPHA
                ].head(10)

                if len(Df_Sig) > 0:
                    Html.append(
                        "<p><strong>Primeras 10 comparaciones "
                        "significativas:</strong></p>"
                    )
                    Html.append(
                        Df_Sig.to_html(index=True, escape=False)
                    )
                else:
                    Html.append(
                        "<p><em>No hay resultados "
                        "significativos.</em></p>"
                    )

    # Pie de página.
    Html.append("<hr>")
    Html.append(
        f"<p><small>Reporte generado: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        f"</small></p>"
    )
    Html.append(
        f"<p><small>Nivel de significancia: "
        f"α = {ALPHA}</small></p>"
    )

    Html.append("</body>")
    Html.append("</html>")

    # Guardar archivo.
    with open(Ruta_Salida, 'w', encoding='utf-8') as F:
        F.write('\n'.join(Html))

    print(f"  ✓ Reporte HTML generado: {Ruta_Salida.name}")

    return Ruta_Salida


# ============================================================
# EXPORTAR ESTADÍSTICAS DESCRIPTIVAS
# ============================================================

def Exportar_Estadisticas_Descriptivas(
    Df: pd.DataFrame,
    Variables: List[str],
    Columna_Categoria: str = 'Categoria_PASO_2023',
    Nombre_Archivo: str = "Estadisticas_Descriptivas"
) -> Path:

    """
    Calcula y exporta estadísticas descriptivas por categoría.

    Parámetros:
    - Df: DataFrame con los datos.
    - Variables: Lista de variables a analizar.
    - Columna_Categoria: Columna con categorías.
    - Nombre_Archivo: Nombre base del archivo.

    Retorna:
    - Path del archivo generado.

    """

    # Crear diccionario para almacenar resultados.
    Resultados = {}

    for Variable in Variables:
        if Variable not in Df.columns:
            continue

        # Calcular estadísticas por categoría.
        Stats = Df.groupby(Columna_Categoria)[Variable].agg([
            'count',
            'mean',
            'std',
            'min',
            'median',
            'max',
            ('q25', lambda x: x.quantile(0.25)),
            ('q75', lambda x: x.quantile(0.75))
        ]).round(3)

        # Renombrar columnas.
        Stats.columns = [
            'N',
            'Media',
            'DE',
            'Min',
            'Mediana',
            'Max',
            'Q25',
            'Q75'
        ]

        Resultados[Variable] = Stats.reset_index()

    # Exportar.
    Timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    Nombre_Completo = f"{Nombre_Archivo}_{Timestamp}.xlsx"
    Ruta_Salida = RUTA_TABLAS / Nombre_Completo

    Ruta_Salida.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(
        Ruta_Salida,
        engine='openpyxl'
    ) as Writer:
        for Variable, Stats in Resultados.items():
            Nombre_Hoja = Variable[:31]
            Stats.to_excel(
                Writer,
                sheet_name=Nombre_Hoja,
                index=False
            )

    print(
        f"  ✓ Estadísticas descriptivas exportadas: "
        f"{Ruta_Salida.name}"
    )

    return Ruta_Salida


# ============================================================
# EXPORTACIÓN INTEGRADA
# ============================================================

def Exportar_Analisis_Completo(
    Resultados_Tests: Dict[str, pd.DataFrame],
    Resultados_Correlaciones: Optional[Dict] = None,
    Estadisticas_Descriptivas: Optional[Dict] = None,
    Nombre_Dataset: str = "Dataset",
    Generar_HTML: bool = True,
    Generar_Excel: bool = True
) -> Dict[str, Path]:

    """
    Exporta todos los resultados de análisis en formatos
    múltiples.

    Parámetros:
    - Resultados_Tests: Diccionario con tests estadísticos.
    - Resultados_Correlaciones: Diccionario con correlaciones.
    - Estadisticas_Descriptivas: Diccionario con estadísticas
      descriptivas.
    - Nombre_Dataset: Nombre del dataset.
    - Generar_HTML: Si generar reporte HTML.
    - Generar_Excel: Si generar archivo Excel.

    Retorna:
    - Diccionario con rutas de archivos generados.

    """

    print("\n" + "="*70)
    print(f"EXPORTANDO RESULTADOS: {Nombre_Dataset}")
    print("="*70)

    Archivos_Generados = {}

    # Crear resumen.
    Df_Resumen = Crear_Resumen_Analisis(
        Resultados_Tests,
        Resultados_Correlaciones,
        Nombre_Dataset
    )

    # Exportar a Excel.
    if Generar_Excel:
        print("\n📊 Exportando a Excel...")

        # Combinar todos los resultados.
        Todos_Resultados = {
            'Resumen': Df_Resumen,
            **Resultados_Tests
        }

        if Resultados_Correlaciones is not None:
            for Nombre, Datos in Resultados_Correlaciones.items():
                if isinstance(Datos, dict):
                    for Sub_Nombre, Sub_Datos in Datos.items():
                        if isinstance(Sub_Datos, pd.DataFrame):
                            Todos_Resultados[
                                f"Corr_{Nombre}_{Sub_Nombre}"
                            ] = Sub_Datos
                elif isinstance(Datos, pd.DataFrame):
                    Todos_Resultados[f"Corr_{Nombre}"] = Datos

        if Estadisticas_Descriptivas is not None:
            for Nombre, Datos in (
                Estadisticas_Descriptivas.items()
            ):
                if isinstance(Datos, pd.DataFrame):
                    Todos_Resultados[f"Desc_{Nombre}"] = Datos

        Ruta_Excel = Exportar_Tests_A_Excel(
            Todos_Resultados,
            f"Analisis_Completo_{Nombre_Dataset}"
        )
        Archivos_Generados['Excel'] = Ruta_Excel

    # Generar reporte HTML.
    if Generar_HTML:
        print("\n📄 Generando reporte HTML...")
        Ruta_HTML = Generar_Reporte_HTML(
            Resultados_Tests,
            Df_Resumen,
            f"Reporte_{Nombre_Dataset}"
        )
        Archivos_Generados['HTML'] = Ruta_HTML

    print("\n" + "="*70)
    print("✅ EXPORTACIÓN COMPLETADA")
    print("="*70)
    print("\nArchivos generados:")
    for Tipo, Ruta in Archivos_Generados.items():
        print(f"  - {Tipo}: {Ruta.name}")
    print()

    return Archivos_Generados


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Módulo de exportación de resultados cargado.")
