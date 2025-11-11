# ============================================================
# CONTROL_11_TESTS_MANN_WHITNEY.PY
# ============================================================
# Control exhaustivo de tests de Mann-Whitney. Verifica que
# comparaciones sean válidas, p-values en rango correcto,
# tamaños de muestra suficientes y resultados reproducibles.
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
from scipy.stats import mannwhitneyu


# ============================================================
# CONSTANTES
# ============================================================

RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)

TAMAÑO_MINIMO_MUESTRA = 10


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Existencia_Resultados(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que el DataFrame de resultados tenga las columnas
    esperadas y al menos un resultado.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Existencia de resultados',
        'columnas_faltantes': [],
        'aprobado': True
    }

    Columnas_Esperadas = [
        'Item',
        'Categoria_1',
        'Categoria_2',
        'Statistic',
        'P_Value',
        'N_Grupo_1',
        'N_Grupo_2'
    ]

    for Columna in Columnas_Esperadas:
        if Columna not in Df_Resultados.columns:
            Resultado['aprobado'] = False
            Resultado['columnas_faltantes'].append(Columna)

    if len(Df_Resultados) == 0:
        Resultado['aprobado'] = False
        Resultado['error'] = "No hay resultados en el DataFrame"

    return Resultado


def Verificar_P_Values_Validos(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que p-values estén en rango [0, 1] y sean
    numéricos válidos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'P-values válidos [0, 1]',
        'p_values_invalidos': [],
        'aprobado': True
    }

    if 'P_Value' not in Df_Resultados.columns:
        return Resultado

    for Idx in Df_Resultados.index:
        P_Value = Df_Resultados.loc[Idx, 'P_Value']

        # Verificar que sea numérico.
        if not isinstance(P_Value, (int, float, np.number)):
            Resultado['aprobado'] = False
            Resultado['p_values_invalidos'].append({
                'fila': int(Idx),
                'item': str(Df_Resultados.loc[Idx, 'Item']),
                'p_value': str(P_Value),
                'problema': 'No es numérico'
            })
            continue

        # Verificar rango [0, 1].
        if P_Value < 0 or P_Value > 1:
            Resultado['aprobado'] = False
            Resultado['p_values_invalidos'].append({
                'fila': int(Idx),
                'item': str(Df_Resultados.loc[Idx, 'Item']),
                'p_value': float(P_Value),
                'problema': 'Fuera de rango [0, 1]'
            })

        # Verificar que no sea NaN.
        if pd.isna(P_Value):
            Resultado['aprobado'] = False
            Resultado['p_values_invalidos'].append({
                'fila': int(Idx),
                'item': str(Df_Resultados.loc[Idx, 'Item']),
                'p_value': 'NaN',
                'problema': 'Valor faltante'
            })

    return Resultado


def Verificar_Tamaños_Muestra(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que tamaños de muestra sean suficientes (>= 10)
    para ambos grupos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': f'Tamaños de muestra >= {TAMAÑO_MINIMO_MUESTRA}',
        'muestras_pequenas': [],
        'aprobado': True
    }

    if 'N_Grupo_1' not in Df_Resultados.columns or 'N_Grupo_2' not in Df_Resultados.columns:
        return Resultado

    for Idx in Df_Resultados.index:
        N1 = Df_Resultados.loc[Idx, 'N_Grupo_1']
        N2 = Df_Resultados.loc[Idx, 'N_Grupo_2']

        if N1 < TAMAÑO_MINIMO_MUESTRA or N2 < TAMAÑO_MINIMO_MUESTRA:
            Resultado['aprobado'] = False
            Resultado['muestras_pequenas'].append({
                'fila': int(Idx),
                'item': str(Df_Resultados.loc[Idx, 'Item']),
                'categoria_1': str(Df_Resultados.loc[Idx, 'Categoria_1']),
                'categoria_2': str(Df_Resultados.loc[Idx, 'Categoria_2']),
                'n_grupo_1': int(N1),
                'n_grupo_2': int(N2)
            })

    return Resultado


def Verificar_Reproducibilidad(
    Df_Datos: pd.DataFrame,
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que resultados sean reproducibles ejecutando
    nuevamente una muestra de tests (10 primeros).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Reproducibilidad de resultados',
        'tests_no_reproducibles': [],
        'aprobado': True
    }

    if 'P_Value' not in Df_Resultados.columns:
        return Resultado

    # Tomar muestra de 10 resultados.
    Muestra = Df_Resultados.head(10)

    for Idx in Muestra.index:
        Item = Muestra.loc[Idx, 'Item']
        Cat1 = Muestra.loc[Idx, 'Categoria_1']
        Cat2 = Muestra.loc[Idx, 'Categoria_2']
        P_Value_Original = Muestra.loc[Idx, 'P_Value']

        # Verificar que las columnas necesarias existan.
        if Item not in Df_Datos.columns:
            continue

        if 'Categoria_PASO_2023' not in Df_Datos.columns:
            continue

        # Extraer datos.
        Grupo1 = Df_Datos[
            Df_Datos['Categoria_PASO_2023'] == Cat1
        ][Item].dropna()

        Grupo2 = Df_Datos[
            Df_Datos['Categoria_PASO_2023'] == Cat2
        ][Item].dropna()

        if len(Grupo1) < 2 or len(Grupo2) < 2:
            continue

        # Re-calcular test.
        try:
            _, P_Value_Nuevo = mannwhitneyu(
                Grupo1, Grupo2, alternative='two-sided'
            )

            # Comparar con tolerancia.
            if not np.isclose(P_Value_Original, P_Value_Nuevo, rtol=1e-3):
                Resultado['aprobado'] = False
                Resultado['tests_no_reproducibles'].append({
                    'fila': int(Idx),
                    'item': str(Item),
                    'categoria_1': str(Cat1),
                    'categoria_2': str(Cat2),
                    'p_value_original': float(P_Value_Original),
                    'p_value_nuevo': float(P_Value_Nuevo),
                    'diferencia': float(
                        abs(P_Value_Original - P_Value_Nuevo)
                    )
                })

        except Exception as e:
            Resultado['aprobado'] = False
            Resultado['tests_no_reproducibles'].append({
                'fila': int(Idx),
                'item': str(Item),
                'error': str(e)
            })

    return Resultado


def Verificar_Comparaciones_Validas(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que comparaciones sean entre categorías
    diferentes (no compara categoría consigo misma).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Comparaciones entre categorías diferentes',
        'comparaciones_invalidas': [],
        'aprobado': True
    }

    if 'Categoria_1' not in Df_Resultados.columns or 'Categoria_2' not in Df_Resultados.columns:
        return Resultado

    for Idx in Df_Resultados.index:
        Cat1 = Df_Resultados.loc[Idx, 'Categoria_1']
        Cat2 = Df_Resultados.loc[Idx, 'Categoria_2']

        if Cat1 == Cat2:
            Resultado['aprobado'] = False
            Resultado['comparaciones_invalidas'].append({
                'fila': int(Idx),
                'item': str(Df_Resultados.loc[Idx, 'Item']),
                'categoria': str(Cat1)
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
    Genera reporte PDF de tests Mann-Whitney.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_11_Tests_Mann_Whitney_{Nombre_Base}_"
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
        f"Control 11: Tests Mann-Whitney - {Nombre_Base}",
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

        if 'columnas_faltantes' in Resultado and Resultado['columnas_faltantes']:
            Story.append(Paragraph(
                f"<b>Columnas faltantes: "
                f"{len(Resultado['columnas_faltantes'])}</b>",
                Estilos['Normal']
            ))

            for Col in Resultado['columnas_faltantes']:
                Story.append(Paragraph(
                    f"- {Col}",
                    Estilos['Normal']
                ))

        if 'p_values_invalidos' in Resultado and Resultado['p_values_invalidos']:
            Story.append(Paragraph(
                f"<b>P-values inválidos: "
                f"{len(Resultado['p_values_invalidos'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['Fila', 'Item', 'P-value', 'Problema']]
            for Caso in Resultado['p_values_invalidos'][:30]:
                Datos_Tabla.append([
                    str(Caso['fila']),
                    Caso['item'],
                    str(Caso['p_value']),
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

        if 'muestras_pequenas' in Resultado and Resultado['muestras_pequenas']:
            Story.append(Paragraph(
                f"<b>Muestras pequeñas (< {TAMAÑO_MINIMO_MUESTRA}): "
                f"{len(Resultado['muestras_pequenas'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['Item', 'Cat 1', 'Cat 2', 'N1', 'N2']]
            for Caso in Resultado['muestras_pequenas'][:30]:
                Datos_Tabla.append([
                    Caso['item'],
                    Caso['categoria_1'],
                    Caso['categoria_2'],
                    str(Caso['n_grupo_1']),
                    str(Caso['n_grupo_2'])
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

        if 'tests_no_reproducibles' in Resultado and Resultado['tests_no_reproducibles']:
            Story.append(Paragraph(
                f"<b>Tests no reproducibles: "
                f"{len(Resultado['tests_no_reproducibles'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['Item', 'P original', 'P nuevo', 'Diferencia']]
            for Caso in Resultado['tests_no_reproducibles'][:20]:
                if 'error' in Caso:
                    continue

                Datos_Tabla.append([
                    Caso['item'],
                    f"{Caso['p_value_original']:.6f}",
                    f"{Caso['p_value_nuevo']:.6f}",
                    f"{Caso['diferencia']:.6f}"
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

        Story.append(Spacer(1, 20))

    Doc.build(Story)
    print(f"\n✓ Reporte PDF generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Control_Tests_Mann_Whitney(
    Nombre_Base: str,
    Df_Resultados: pd.DataFrame,
    Df_Datos: pd.DataFrame = None
) -> bool:

    """
    Ejecuta control completo de tests Mann-Whitney.

    Parámetros:
    - Nombre_Base: 'Generales' o 'Ballotage'.
    - Df_Resultados: DataFrame con resultados de tests.
    - Df_Datos: DataFrame original (opcional, para reproducibilidad).

    """

    print("\n" + "="*70)
    print(f"CONTROL 11: TESTS MANN-WHITNEY - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando existencia de resultados...")
    R1 = Verificar_Existencia_Resultados(Df_Resultados, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando p-values válidos...")
    R2 = Verificar_P_Values_Validos(Df_Resultados, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando tamaños de muestra...")
    R3 = Verificar_Tamaños_Muestra(Df_Resultados, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando comparaciones válidas...")
    R4 = Verificar_Comparaciones_Validas(Df_Resultados, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    if Df_Datos is not None:
        print("\n5. Verificando reproducibilidad...")
        R5 = Verificar_Reproducibilidad(
            Df_Datos, Df_Resultados, Nombre_Base
        )
        Resultados.append(R5)
        print(f"   {'✓' if R5['aprobado'] else '✗'} "
              f"{R5['verificacion']}")

    print(f"\n{5 if Df_Datos is None else 6}. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Tests correctos")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 11 debe ejecutarse importando la función")
    print("Ejecutar_Control_Tests_Mann_Whitney()")
