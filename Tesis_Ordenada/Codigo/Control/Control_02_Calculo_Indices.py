# ============================================================
# CONTROL_02_CALCULO_INDICES.PY
# ============================================================
# Control exhaustivo de cálculo de índices ideológicos.
# Verifica rangos válidos, coherencia entre índices y
# detección de valores atípicos extremos fila por fila.
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
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak
)
from reportlab.lib import colors
import sys

# Agregar ruta de Utilidades.
Ruta_Actual = Path(__file__).parent
Ruta_Utilidades = Ruta_Actual.parent / "Utilidades"
sys.path.append(str(Ruta_Utilidades))

from Configuracion import (
    ITEMS_PROGRESISTAS,
    ITEMS_CONSERVADORES
)


# ============================================================
# CONSTANTES
# ============================================================

# Índices a verificar.
INDICES_A_VERIFICAR = [
    'Indice_Positividad',
    'Indice_Progresismo',
    'Indice_Progresismo_Tiempo',
    'Indice_Conservadurismo',
    'Indice_Conservadurismo_Tiempo'
]

# Rangos esperados para índices de respuesta (escala 1-5).
RANGO_INDICE_RESPUESTA = (1.0, 5.0)

# Rango esperado para índices de tiempo (positivos).
RANGO_INDICE_TIEMPO = (0.0, np.inf)

# Ruta de reportes.
RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Existencia_Indices(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todos los índices esperados existan.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con resultados.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Existencia de índices',
        'indices_esperados': len(INDICES_A_VERIFICAR),
        'indices_presentes': 0,
        'indices_faltantes': [],
        'aprobado': True
    }

    for Indice in INDICES_A_VERIFICAR:
        if Indice in Df.columns:
            Resultado['indices_presentes'] += 1
        else:
            Resultado['indices_faltantes'].append(Indice)
            Resultado['aprobado'] = False

    return Resultado


def Verificar_Rangos_Indices_Respuesta(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que índices de respuesta estén en rango [1, 5].
    Reporta cada sujeto fuera de rango.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos fuera de rango.

    """

    Indices_Respuesta = [
        'Indice_Positividad',
        'Indice_Progresismo',
        'Indice_Conservadurismo'
    ]

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Rangos de índices de respuesta [1-5]',
        'casos_fuera_de_rango': [],
        'aprobado': True
    }

    for Indice in Indices_Respuesta:
        if Indice not in Df.columns:
            continue

        # Verificar rango.
        Min_Val, Max_Val = RANGO_INDICE_RESPUESTA
        Mask_Invalido = (
            (Df[Indice] < Min_Val) |
            (Df[Indice] > Max_Val)
        )

        # Excluir NaN de la verificación.
        Mask_Invalido = Mask_Invalido & Df[Indice].notna()

        Indices_Invalidos = Df[Mask_Invalido].index.tolist()

        if Indices_Invalidos:
            Resultado['aprobado'] = False

            for Idx in Indices_Invalidos:
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Resultado['casos_fuera_de_rango'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'indice': Indice,
                    'valor': float(Df.loc[Idx, Indice])
                })

    return Resultado


def Verificar_Rangos_Indices_Tiempo(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que índices de tiempo sean no negativos.
    Reporta cada caso con tiempo negativo.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos inválidos.

    """

    Indices_Tiempo = [
        'Indice_Progresismo_Tiempo',
        'Indice_Conservadurismo_Tiempo'
    ]

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Índices de tiempo no negativos',
        'casos_negativos': [],
        'aprobado': True
    }

    for Indice in Indices_Tiempo:
        if Indice not in Df.columns:
            continue

        # Verificar no negativos.
        Mask_Negativo = Df[Indice] < 0
        Mask_Negativo = Mask_Negativo & Df[Indice].notna()

        Indices_Negativos = Df[Mask_Negativo].index.tolist()

        if Indices_Negativos:
            Resultado['aprobado'] = False

            for Idx in Indices_Negativos:
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Resultado['casos_negativos'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'indice': Indice,
                    'valor': float(Df.loc[Idx, Indice])
                })

    return Resultado


def Verificar_Coherencia_Progresismo_Conservadurismo(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica coherencia entre índices de progresismo y
    conservadurismo. No deberían ser ambos muy altos
    simultáneamente (contradicción ideológica).

    Detecta casos donde ambos índices > 4.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos incoherentes.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Coherencia Progresismo-Conservadurismo',
        'casos_incoherentes': [],
        'aprobado': True
    }

    if ('Indice_Progresismo' not in Df.columns or
        'Indice_Conservadurismo' not in Df.columns):
        Resultado['error'] = "Índices no encontrados"
        Resultado['aprobado'] = False
        return Resultado

    # Detectar ambos muy altos (contradicción).
    Mask_Incoherente = (
        (Df['Indice_Progresismo'] > 4.0) &
        (Df['Indice_Conservadurismo'] > 4.0)
    )

    Indices_Incoherentes = Df[Mask_Incoherente].index.tolist()

    if Indices_Incoherentes:
        Resultado['aprobado'] = False

        for Idx in Indices_Incoherentes:
            ID_Sujeto = (
                Df.loc[Idx, 'ID']
                if 'ID' in Df.columns
                else f"Fila_{Idx}"
            )

            Resultado['casos_incoherentes'].append({
                'id': ID_Sujeto,
                'fila': int(Idx),
                'indice_progresismo': float(
                    Df.loc[Idx, 'Indice_Progresismo']
                ),
                'indice_conservadurismo': float(
                    Df.loc[Idx, 'Indice_Conservadurismo']
                )
            })

    return Resultado


def Verificar_NaN_En_Indices(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica presencia de NaN en índices calculados.
    Reporta cada caso con NaN.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos con NaN.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Valores NaN en índices',
        'casos_con_nan': [],
        'aprobado': True
    }

    for Indice in INDICES_A_VERIFICAR:
        if Indice not in Df.columns:
            continue

        Mask_NaN = Df[Indice].isna()
        Indices_NaN = Df[Mask_NaN].index.tolist()

        if Indices_NaN:
            Resultado['aprobado'] = False

            for Idx in Indices_NaN:
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Resultado['casos_con_nan'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'indice': Indice
                })

    return Resultado


def Verificar_Valores_Extremos(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica valores estadísticamente extremos (outliers)
    en índices usando criterio de 3 desviaciones estándar.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos extremos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Valores extremos (>3 SD)',
        'casos_extremos': [],
        'aprobado': True
    }

    for Indice in INDICES_A_VERIFICAR:
        if Indice not in Df.columns:
            continue

        # Calcular media y SD.
        Media = Df[Indice].mean()
        SD = Df[Indice].std()

        if pd.isna(Media) or pd.isna(SD) or SD == 0:
            continue

        # Detectar outliers (>3 SD).
        Mask_Extremo = np.abs(Df[Indice] - Media) > (3 * SD)
        Mask_Extremo = Mask_Extremo & Df[Indice].notna()

        Indices_Extremos = Df[Mask_Extremo].index.tolist()

        if Indices_Extremos:
            # No falla automáticamente, solo reporta.
            for Idx in Indices_Extremos:
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Valor = float(Df.loc[Idx, Indice])
                Z_Score = (Valor - Media) / SD

                Resultado['casos_extremos'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'indice': Indice,
                    'valor': Valor,
                    'z_score': float(Z_Score)
                })

    # Solo falla si hay muchos extremos (>5% de casos).
    if len(Resultado['casos_extremos']) > len(Df) * 0.05:
        Resultado['aprobado'] = False

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
    Genera reporte PDF detallado de verificaciones de
    índices.

    Parámetros:
    - Resultados: Lista de diccionarios con resultados.
    - Nombre_Base: Nombre de la base verificada.
    - Ruta_Salida: Path donde guardar PDF.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_02_Indices_{Nombre_Base}_"
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

    # Título.
    Story.append(Paragraph(
        f"Control 02: Cálculo de Índices - {Nombre_Base}",
        Estilo_Titulo
    ))
    Story.append(Paragraph(
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        Estilos['Normal']
    ))
    Story.append(Spacer(1, 20))

    # Resumen.
    Aprobados = sum(1 for R in Resultados if R['aprobado'])
    Total = len(Resultados)

    Story.append(Paragraph(
        f"<b>Resumen: {Aprobados}/{Total} verificaciones "
        f"aprobadas</b>",
        Estilo_Subtitulo
    ))
    Story.append(Spacer(1, 12))

    # Detalle de cada verificación.
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

        # Detalles específicos.
        if 'casos_fuera_de_rango' in Resultado and Resultado['casos_fuera_de_rango']:
            Story.append(Paragraph(
                f"<b>Casos fuera de rango: "
                f"{len(Resultado['casos_fuera_de_rango'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Índice', 'Valor']]
            for Caso in Resultado['casos_fuera_de_rango'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['indice'],
                    f"{Caso['valor']:.3f}"
                ])

            Tabla = Table(Datos_Tabla)
            Tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            Story.append(Tabla)

            if len(Resultado['casos_fuera_de_rango']) > 30:
                Story.append(Paragraph(
                    f"... y {len(Resultado['casos_fuera_de_rango']) - 30} más",
                    Estilos['Italic']
                ))

        elif 'casos_negativos' in Resultado and Resultado['casos_negativos']:
            Story.append(Paragraph(
                f"<b>Casos con tiempo negativo: "
                f"{len(Resultado['casos_negativos'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Índice', 'Valor']]
            for Caso in Resultado['casos_negativos'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['indice'],
                    f"{Caso['valor']:.3f}"
                ])

            Tabla = Table(Datos_Tabla)
            Tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            Story.append(Tabla)

        elif 'casos_incoherentes' in Resultado and Resultado['casos_incoherentes']:
            Story.append(Paragraph(
                f"<b>Casos con índices contradictorios: "
                f"{len(Resultado['casos_incoherentes'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Prog.', 'Cons.']]
            for Caso in Resultado['casos_incoherentes'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    f"{Caso['indice_progresismo']:.2f}",
                    f"{Caso['indice_conservadurismo']:.2f}"
                ])

            Tabla = Table(Datos_Tabla)
            Tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            Story.append(Tabla)

        elif 'casos_extremos' in Resultado and Resultado['casos_extremos']:
            Story.append(Paragraph(
                f"<b>Casos con valores extremos (>3 SD): "
                f"{len(Resultado['casos_extremos'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Índice', 'Valor', 'Z-Score']]
            for Caso in Resultado['casos_extremos'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['indice'],
                    f"{Caso['valor']:.2f}",
                    f"{Caso['z_score']:.2f}"
                ])

            Tabla = Table(Datos_Tabla)
            Tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            Story.append(Tabla)

        Story.append(Spacer(1, 20))

    Doc.build(Story)
    print(f"\n✓ Reporte PDF generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Control_Calculo_Indices(
    Nombre_Base: str,
    Df: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de cálculo de índices.

    Parámetros:
    - Nombre_Base: 'Generales' o 'Ballotage'.
    - Df: DataFrame con índices calculados a verificar.

    Retorna:
    - True si todas las verificaciones pasan.

    """

    print("\n" + "="*70)
    print(f"CONTROL 02: CÁLCULO DE ÍNDICES - {Nombre_Base}")
    print("="*70)

    Resultados = []

    # Verificación 1: Existencia.
    print("\n1. Verificando existencia de índices...")
    R1 = Verificar_Existencia_Indices(Df, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    # Verificación 2: Rangos índices respuesta.
    print("\n2. Verificando rangos índices respuesta...")
    R2 = Verificar_Rangos_Indices_Respuesta(Df, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    # Verificación 3: Rangos índices tiempo.
    print("\n3. Verificando rangos índices tiempo...")
    R3 = Verificar_Rangos_Indices_Tiempo(Df, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    # Verificación 4: Coherencia ideológica.
    print("\n4. Verificando coherencia ideológica...")
    R4 = Verificar_Coherencia_Progresismo_Conservadurismo(
        Df, Nombre_Base
    )
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    # Verificación 5: NaN.
    print("\n5. Verificando valores NaN...")
    R5 = Verificar_NaN_En_Indices(Df, Nombre_Base)
    Resultados.append(R5)
    print(f"   {'✓' if R5['aprobado'] else '✗'} "
          f"{R5['verificacion']}")

    # Verificación 6: Valores extremos.
    print("\n6. Verificando valores extremos...")
    R6 = Verificar_Valores_Extremos(Df, Nombre_Base)
    Resultados.append(R6)
    print(f"   {'✓' if R6['aprobado'] else '✗'} "
          f"{R6['verificacion']}")

    # Generar reporte PDF.
    print("\n7. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    # Resultado final.
    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Índices correctos")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Control 02 debe ejecutarse importando la función")
    print("Ejecutar_Control_Calculo_Indices()")
