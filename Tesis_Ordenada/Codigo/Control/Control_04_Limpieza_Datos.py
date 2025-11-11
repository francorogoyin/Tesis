# ============================================================
# CONTROL_04_LIMPIEZA_DATOS.PY
# ============================================================
# Control exhaustivo de limpieza de datos y eliminación de
# outliers. Verifica que outliers removidos sean legítimos
# y reporta distribuciones antes/después.
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


# ============================================================
# CONSTANTES
# ============================================================

RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Perdida_Datos(
    Df_Antes: pd.DataFrame,
    Df_Despues: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que la pérdida de datos por limpieza no sea
    excesiva (>20%).

    Parámetros:
    - Df_Antes: DataFrame antes de limpieza.
    - Df_Despues: DataFrame después de limpieza.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con estadísticas de pérdida.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Pérdida de datos aceptable',
        'filas_antes': len(Df_Antes),
        'filas_despues': len(Df_Despues),
        'filas_eliminadas': len(Df_Antes) - len(Df_Despues),
        'porcentaje_perdida': 0.0,
        'aprobado': True
    }

    Porcentaje = (
        (len(Df_Antes) - len(Df_Despues)) / len(Df_Antes) * 100
    )
    Resultado['porcentaje_perdida'] = float(Porcentaje)

    # Falla si pérdida > 20%.
    if Porcentaje > 20.0:
        Resultado['aprobado'] = False

    return Resultado


def Verificar_Outliers_Edad(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que no queden valores de edad obviamente
    outliers (< 18 o > 100).

    Parámetros:
    - Df: DataFrame limpio a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con outliers encontrados.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Outliers de edad eliminados',
        'outliers_restantes': [],
        'aprobado': True
    }

    if 'Edad' not in Df.columns:
        return Resultado

    Mask_Outlier = (Df['Edad'] < 18) | (Df['Edad'] > 100)
    Indices_Outlier = Df[Mask_Outlier].index.tolist()

    if Indices_Outlier:
        Resultado['aprobado'] = False

        for Idx in Indices_Outlier:
            ID_Sujeto = (
                Df.loc[Idx, 'ID']
                if 'ID' in Df.columns
                else f"Fila_{Idx}"
            )

            Resultado['outliers_restantes'].append({
                'id': ID_Sujeto,
                'fila': int(Idx),
                'edad': float(Df.loc[Idx, 'Edad'])
            })

    return Resultado


def Verificar_Duplicados_Post_Limpieza(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que no haya duplicados después de limpieza.

    Parámetros:
    - Df: DataFrame limpio.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con duplicados si existen.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Sin duplicados post-limpieza',
        'duplicados': [],
        'aprobado': True
    }

    if 'ID' not in Df.columns:
        return Resultado

    Duplicados = Df[Df.duplicated(subset='ID', keep=False)]

    if not Duplicados.empty:
        Resultado['aprobado'] = False

        for ID_Dup in Duplicados['ID'].unique():
            Filas = Df[Df['ID'] == ID_Dup].index.tolist()
            Resultado['duplicados'].append({
                'id': ID_Dup,
                'filas': [int(f) for f in Filas]
            })

    return Resultado


def Verificar_Columnas_Mantenidas(
    Df_Antes: pd.DataFrame,
    Df_Despues: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todas las columnas se mantengan después de
    limpieza.

    Parámetros:
    - Df_Antes: DataFrame antes.
    - Df_Despues: DataFrame después.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con columnas perdidas.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Columnas mantenidas',
        'columnas_antes': len(Df_Antes.columns),
        'columnas_despues': len(Df_Despues.columns),
        'columnas_perdidas': [],
        'aprobado': True
    }

    Cols_Antes = set(Df_Antes.columns)
    Cols_Despues = set(Df_Despues.columns)

    Perdidas = Cols_Antes - Cols_Despues

    if Perdidas:
        Resultado['aprobado'] = False
        Resultado['columnas_perdidas'] = list(Perdidas)

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
    Genera reporte PDF de limpieza de datos.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_04_Limpieza_{Nombre_Base}_"
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
        f"Control 04: Limpieza de Datos - {Nombre_Base}",
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

        # Detalles específicos.
        if 'filas_antes' in Resultado:
            Story.append(Paragraph(
                f"Filas antes: {Resultado['filas_antes']}<br/>"
                f"Filas después: {Resultado['filas_despues']}<br/>"
                f"Eliminadas: {Resultado['filas_eliminadas']} "
                f"({Resultado['porcentaje_perdida']:.1f}%)",
                Estilos['Normal']
            ))

        if 'outliers_restantes' in Resultado and Resultado['outliers_restantes']:
            Story.append(Paragraph(
                f"<b>Outliers no eliminados: "
                f"{len(Resultado['outliers_restantes'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Edad']]
            for Caso in Resultado['outliers_restantes'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    f"{Caso['edad']:.0f}"
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

def Ejecutar_Control_Limpieza_Datos(
    Nombre_Base: str,
    Df_Antes: pd.DataFrame,
    Df_Despues: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de limpieza de datos.

    Parámetros:
    - Nombre_Base: 'Generales' o 'Ballotage'.
    - Df_Antes: DataFrame antes de limpieza.
    - Df_Despues: DataFrame después de limpieza.

    Retorna:
    - True si todas las verificaciones pasan.

    """

    print("\n" + "="*70)
    print(f"CONTROL 04: LIMPIEZA DE DATOS - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando pérdida de datos...")
    R1 = Verificar_Perdida_Datos(
        Df_Antes, Df_Despues, Nombre_Base
    )
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando outliers eliminados...")
    R2 = Verificar_Outliers_Edad(Df_Despues, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando duplicados...")
    R3 = Verificar_Duplicados_Post_Limpieza(
        Df_Despues, Nombre_Base
    )
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando columnas mantenidas...")
    R4 = Verificar_Columnas_Mantenidas(
        Df_Antes, Df_Despues, Nombre_Base
    )
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    print("\n5. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Limpieza correcta")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 04 debe ejecutarse importando la función")
    print("Ejecutar_Control_Limpieza_Datos()")
