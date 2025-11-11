# ============================================================
# CONTROL_13_CORRELACIONES.PY
# ============================================================
# Control exhaustivo de análisis de correlaciones Spearman.
# Verifica que coeficientes estén en [-1, 1], p-values
# válidos y matrices simétricas.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors
from scipy.stats import spearmanr


# ============================================================
# CONSTANTES
# ============================================================

RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Coeficientes_Validos(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que coeficientes de correlación estén en rango
    [-1, 1] y sean numéricos válidos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Coeficientes en rango [-1, 1]',
        'coeficientes_invalidos': [],
        'aprobado': True
    }

    if 'Correlacion' not in Df_Resultados.columns:
        return Resultado

    for Idx in Df_Resultados.index:
        Coef = Df_Resultados.loc[Idx, 'Correlacion']

        if pd.isna(Coef):
            Resultado['aprobado'] = False
            Resultado['coeficientes_invalidos'].append({
                'fila': int(Idx),
                'variable_1': str(
                    Df_Resultados.loc[Idx, 'Variable_1']
                    if 'Variable_1' in Df_Resultados.columns
                    else 'N/A'
                ),
                'variable_2': str(
                    Df_Resultados.loc[Idx, 'Variable_2']
                    if 'Variable_2' in Df_Resultados.columns
                    else 'N/A'
                ),
                'coeficiente': 'NaN',
                'problema': 'Valor faltante'
            })
            continue

        if not isinstance(Coef, (int, float, np.number)):
            Resultado['aprobado'] = False
            Resultado['coeficientes_invalidos'].append({
                'fila': int(Idx),
                'variable_1': str(
                    Df_Resultados.loc[Idx, 'Variable_1']
                    if 'Variable_1' in Df_Resultados.columns
                    else 'N/A'
                ),
                'variable_2': str(
                    Df_Resultados.loc[Idx, 'Variable_2']
                    if 'Variable_2' in Df_Resultados.columns
                    else 'N/A'
                ),
                'coeficiente': str(Coef),
                'problema': 'No es numérico'
            })
            continue

        if Coef < -1 or Coef > 1:
            Resultado['aprobado'] = False
            Resultado['coeficientes_invalidos'].append({
                'fila': int(Idx),
                'variable_1': str(
                    Df_Resultados.loc[Idx, 'Variable_1']
                    if 'Variable_1' in Df_Resultados.columns
                    else 'N/A'
                ),
                'variable_2': str(
                    Df_Resultados.loc[Idx, 'Variable_2']
                    if 'Variable_2' in Df_Resultados.columns
                    else 'N/A'
                ),
                'coeficiente': float(Coef),
                'problema': 'Fuera de rango [-1, 1]'
            })

    return Resultado


def Verificar_P_Values_Validos(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que p-values estén en rango [0, 1].

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'P-values en rango [0, 1]',
        'p_values_invalidos': [],
        'aprobado': True
    }

    if 'P_Value' not in Df_Resultados.columns:
        return Resultado

    for Idx in Df_Resultados.index:
        P_Value = Df_Resultados.loc[Idx, 'P_Value']

        if pd.isna(P_Value):
            Resultado['aprobado'] = False
            Resultado['p_values_invalidos'].append({
                'fila': int(Idx),
                'p_value': 'NaN',
                'problema': 'Valor faltante'
            })
            continue

        if not isinstance(P_Value, (int, float, np.number)):
            Resultado['aprobado'] = False
            Resultado['p_values_invalidos'].append({
                'fila': int(Idx),
                'p_value': str(P_Value),
                'problema': 'No es numérico'
            })
            continue

        if P_Value < 0 or P_Value > 1:
            Resultado['aprobado'] = False
            Resultado['p_values_invalidos'].append({
                'fila': int(Idx),
                'p_value': float(P_Value),
                'problema': 'Fuera de rango [0, 1]'
            })

    return Resultado


def Verificar_Matriz_Simetrica(
    Matriz_Correlacion: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que matriz de correlación sea simétrica.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Matriz de correlación simétrica',
        'diferencias': [],
        'aprobado': True
    }

    if Matriz_Correlacion is None:
        return Resultado

    # Verificar que sea cuadrada.
    if Matriz_Correlacion.shape[0] != Matriz_Correlacion.shape[1]:
        Resultado['aprobado'] = False
        Resultado['error'] = "Matriz no es cuadrada"
        return Resultado

    # Verificar simetría.
    Diferencias = (
        Matriz_Correlacion - Matriz_Correlacion.T
    )

    # Encontrar diferencias significativas (> 1e-6).
    Mask = np.abs(Diferencias) > 1e-6

    if Mask.sum().sum() > 0:
        Resultado['aprobado'] = False

        # Reportar primeras 20 diferencias.
        Indices = np.where(Mask)
        for i in range(min(20, len(Indices[0]))):
            Fila = Indices[0][i]
            Columna = Indices[1][i]

            Resultado['diferencias'].append({
                'fila': int(Fila),
                'columna': int(Columna),
                'variable_fila': str(Matriz_Correlacion.index[Fila]),
                'variable_columna': str(
                    Matriz_Correlacion.columns[Columna]
                ),
                'valor_ij': float(
                    Matriz_Correlacion.iloc[Fila, Columna]
                ),
                'valor_ji': float(
                    Matriz_Correlacion.iloc[Columna, Fila]
                ),
                'diferencia': float(Diferencias.iloc[Fila, Columna])
            })

    return Resultado


def Verificar_Diagonal_Igual_Uno(
    Matriz_Correlacion: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que diagonal de matriz de correlación sea 1
    (correlación de variable consigo misma).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Diagonal = 1',
        'valores_incorrectos': [],
        'aprobado': True
    }

    if Matriz_Correlacion is None:
        return Resultado

    # Obtener diagonal.
    Diagonal = np.diag(Matriz_Correlacion)

    # Verificar que todos sean ≈ 1.
    for i, Valor in enumerate(Diagonal):
        if not np.isclose(Valor, 1.0, rtol=1e-6):
            Resultado['aprobado'] = False
            Resultado['valores_incorrectos'].append({
                'indice': int(i),
                'variable': str(Matriz_Correlacion.index[i]),
                'valor': float(Valor)
            })

    return Resultado


def Verificar_Reproducibilidad(
    Df_Datos: pd.DataFrame,
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que correlaciones sean reproducibles
    (muestra de 10 correlaciones).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Reproducibilidad de correlaciones',
        'correlaciones_no_reproducibles': [],
        'aprobado': True
    }

    if 'Correlacion' not in Df_Resultados.columns:
        return Resultado

    # Tomar muestra de 10.
    Muestra = Df_Resultados.head(10)

    for Idx in Muestra.index:
        if 'Variable_1' not in Df_Resultados.columns or 'Variable_2' not in Df_Resultados.columns:
            continue

        Var1 = Muestra.loc[Idx, 'Variable_1']
        Var2 = Muestra.loc[Idx, 'Variable_2']
        Corr_Original = Muestra.loc[Idx, 'Correlacion']

        # Verificar que variables existan.
        if Var1 not in Df_Datos.columns or Var2 not in Df_Datos.columns:
            continue

        # Extraer datos.
        Datos1 = Df_Datos[Var1].dropna()
        Datos2 = Df_Datos[Var2].dropna()

        # Alinear índices.
        Indices_Comunes = Datos1.index.intersection(Datos2.index)
        Datos1 = Datos1.loc[Indices_Comunes]
        Datos2 = Datos2.loc[Indices_Comunes]

        if len(Datos1) < 3:
            continue

        # Re-calcular correlación.
        try:
            Corr_Nueva, _ = spearmanr(Datos1, Datos2)

            # Comparar con tolerancia.
            if not np.isclose(Corr_Original, Corr_Nueva, rtol=1e-3):
                Resultado['aprobado'] = False
                Resultado['correlaciones_no_reproducibles'].append({
                    'fila': int(Idx),
                    'variable_1': str(Var1),
                    'variable_2': str(Var2),
                    'corr_original': float(Corr_Original),
                    'corr_nueva': float(Corr_Nueva),
                    'diferencia': float(
                        abs(Corr_Original - Corr_Nueva)
                    )
                })

        except Exception as e:
            Resultado['aprobado'] = False
            Resultado['correlaciones_no_reproducibles'].append({
                'fila': int(Idx),
                'variable_1': str(Var1),
                'variable_2': str(Var2),
                'error': str(e)
            })

    return Resultado


# ============================================================
# GENERACIÓN DE REPORTE PDF
# ============================================================

def Generar_Reporte_PDF(
    Resultados: List[Dict],
    Nombre_Base: str,
    Ruta_Salida: Path
) -> None:

    """
    Genera reporte PDF de correlaciones.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_13_Correlaciones_{Nombre_Base}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    Doc = SimpleDocTemplate(
        str(Archivo_PDF),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    Estilos = getSampleStyleSheet()
    Estilo_Titulo = ParagraphStyle(
        'CustomTitle',
        parent=Estilos['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30
    )
    Estilo_Subtitulo = ParagraphStyle(
        'CustomHeading',
        parent=Estilos['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12
    )

    Story = []

    Story.append(Paragraph(
        f"Control 13: Correlaciones Spearman - {Nombre_Base}",
        Estilo_Titulo
    ))
    Story.append(Paragraph(
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        Estilos['Normal']
    ))
    Story.append(Spacer(1, 20))

    Aprobados = sum(1 for R in Resultados if R['aprobado'])
    Total = len(Resultados)

    Story.append(Paragraph(
        f"<b>Resumen: {Aprobados}/{Total} verificaciones "
        f"aprobadas</b>",
        Estilo_Subtitulo
    ))
    Story.append(Spacer(1, 12))

    for Resultado in Resultados:
        Story.append(Paragraph(
            f"<b>{Resultado['verificacion']}</b>",
            Estilo_Subtitulo
        ))

        Estado = "✓ APROBADO" if Resultado['aprobado'] else "✗ FALLÓ"
        Color = colors.green if Resultado['aprobado'] else colors.red

        Story.append(Paragraph(
            f"Estado: <font color='{Color}'><b>{Estado}</b></font>",
            Estilos['Normal']
        ))
        Story.append(Spacer(1, 8))

        if 'coeficientes_invalidos' in Resultado and Resultado['coeficientes_invalidos']:
            Story.append(Paragraph(
                f"<b>Coeficientes inválidos: "
                f"{len(Resultado['coeficientes_invalidos'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['Var1', 'Var2', 'Coef.', 'Problema']]
            for Caso in Resultado['coeficientes_invalidos'][:20]:
                Datos_Tabla.append([
                    Caso['variable_1'],
                    Caso['variable_2'],
                    str(Caso['coeficiente']),
                    Caso['problema']
                ])

            Tabla = Table(Datos_Tabla)
            Tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            Story.append(Tabla)

        if 'diferencias' in Resultado and Resultado['diferencias']:
            Story.append(Paragraph(
                f"<b>Matriz no simétrica: "
                f"{len(Resultado['diferencias'])} diferencias</b>",
                Estilos['Normal']
            ))

            for Diff in Resultado['diferencias'][:10]:
                Story.append(Paragraph(
                    f"- ({Diff['variable_fila']}, "
                    f"{Diff['variable_columna']}): "
                    f"{Diff['valor_ij']:.6f} vs {Diff['valor_ji']:.6f}",
                    Estilos['Normal']
                ))

        if 'valores_incorrectos' in Resultado and Resultado['valores_incorrectos']:
            Story.append(Paragraph(
                f"<b>Diagonal ≠ 1: "
                f"{len(Resultado['valores_incorrectos'])}</b>",
                Estilos['Normal']
            ))

            for Val in Resultado['valores_incorrectos'][:20]:
                Story.append(Paragraph(
                    f"- {Val['variable']}: {Val['valor']:.6f}",
                    Estilos['Normal']
                ))

        Story.append(Spacer(1, 20))

    Doc.build(Story)
    print(f"\n✓ Reporte PDF generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Control_Correlaciones(
    Nombre_Base: str,
    Df_Resultados: pd.DataFrame,
    Matriz_Correlacion: pd.DataFrame = None,
    Df_Datos: pd.DataFrame = None
) -> bool:

    """
    Ejecuta control completo de correlaciones.

    Parámetros:
    - Nombre_Base: 'Generales' o 'Ballotage'.
    - Df_Resultados: DataFrame con correlaciones.
    - Matriz_Correlacion: Matriz cuadrada (opcional).
    - Df_Datos: DataFrame original (opcional, para reproducibilidad).

    """

    print("\n" + "="*70)
    print(f"CONTROL 13: CORRELACIONES SPEARMAN - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando coeficientes válidos...")
    R1 = Verificar_Coeficientes_Validos(Df_Resultados, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando p-values válidos...")
    R2 = Verificar_P_Values_Validos(Df_Resultados, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    if Matriz_Correlacion is not None:
        print("\n3. Verificando matriz simétrica...")
        R3 = Verificar_Matriz_Simetrica(
            Matriz_Correlacion, Nombre_Base
        )
        Resultados.append(R3)
        print(f"   {'✓' if R3['aprobado'] else '✗'} "
              f"{R3['verificacion']}")

        print("\n4. Verificando diagonal = 1...")
        R4 = Verificar_Diagonal_Igual_Uno(
            Matriz_Correlacion, Nombre_Base
        )
        Resultados.append(R4)
        print(f"   {'✓' if R4['aprobado'] else '✗'} "
              f"{R4['verificacion']}")

    if Df_Datos is not None:
        Num_Paso = 3 if Matriz_Correlacion is None else 5
        print(f"\n{Num_Paso}. Verificando reproducibilidad...")
        R_Repro = Verificar_Reproducibilidad(
            Df_Datos, Df_Resultados, Nombre_Base
        )
        Resultados.append(R_Repro)
        print(f"   {'✓' if R_Repro['aprobado'] else '✗'} "
              f"{R_Repro['verificacion']}")

    Num_Final = len(Resultados) + 1
    print(f"\n{Num_Final}. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Correlaciones correctas")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 13 debe ejecutarse importando la función")
    print("Ejecutar_Control_Correlaciones()")
