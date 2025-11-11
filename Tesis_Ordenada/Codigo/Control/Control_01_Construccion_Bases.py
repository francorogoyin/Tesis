# ============================================================
# CONTROL_01_CONSTRUCCION_BASES.PY
# ============================================================
# Control exhaustivo de construcción de bases desde CSVs
# crudos. Verifica integridad fila por fila, detecta
# duplicados, valores faltantes y estructura incorrecta.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
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
    RUTA_DATOS_CRUDOS_GENERALES,
    RUTA_DATOS_CRUDOS_BALLOTAGE
)


# ============================================================
# CONSTANTES
# ============================================================

# Columnas críticas que deben existir.
COLUMNAS_CRITICAS = [
    'ID',
    'Edad',
    'Genero',
    'Provincia'
]

# Ruta de reportes.
RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_IDs_Unicos(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todos los IDs sean únicos.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo de la base.

    Retorna:
    - Dict con resultados de verificación.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'IDs únicos',
        'total_filas': len(Df),
        'ids_unicos': Df['ID'].nunique(),
        'ids_duplicados': [],
        'aprobado': True
    }

    if 'ID' not in Df.columns:
        Resultado['aprobado'] = False
        Resultado['error'] = "Columna 'ID' no encontrada"
        return Resultado

    # Detectar duplicados.
    Duplicados = Df[Df.duplicated(subset='ID', keep=False)]

    if not Duplicados.empty:
        Resultado['aprobado'] = False

        # Agrupar por ID duplicado.
        for ID_Dup in Duplicados['ID'].unique():
            Filas_Dup = Df[Df['ID'] == ID_Dup].index.tolist()
            Resultado['ids_duplicados'].append({
                'id': ID_Dup,
                'filas': [int(f) for f in Filas_Dup],
                'num_repeticiones': len(Filas_Dup)
            })

    return Resultado


def Verificar_Columnas_Criticas(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todas las columnas críticas existan.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con resultados.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Columnas críticas',
        'columnas_esperadas': len(COLUMNAS_CRITICAS),
        'columnas_presentes': 0,
        'columnas_faltantes': [],
        'aprobado': True
    }

    for Columna in COLUMNAS_CRITICAS:
        if Columna in Df.columns:
            Resultado['columnas_presentes'] += 1
        else:
            Resultado['columnas_faltantes'].append(Columna)
            Resultado['aprobado'] = False

    return Resultado


def Verificar_Tipos_Datos(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica tipos de datos de columnas críticas.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con resultados.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Tipos de datos',
        'columnas_verificadas': 0,
        'problemas': [],
        'aprobado': True
    }

    # Verificar ID es numérico o string.
    if 'ID' in Df.columns:
        Resultado['columnas_verificadas'] += 1
        if not (pd.api.types.is_numeric_dtype(Df['ID']) or
                pd.api.types.is_string_dtype(Df['ID'])):
            Resultado['problemas'].append({
                'columna': 'ID',
                'problema': 'Tipo de dato no válido',
                'tipo_actual': str(Df['ID'].dtype)
            })
            Resultado['aprobado'] = False

    # Verificar Edad es numérico.
    if 'Edad' in Df.columns:
        Resultado['columnas_verificadas'] += 1
        if not pd.api.types.is_numeric_dtype(Df['Edad']):
            Resultado['problemas'].append({
                'columna': 'Edad',
                'problema': 'Debe ser numérico',
                'tipo_actual': str(Df['Edad'].dtype)
            })
            Resultado['aprobado'] = False

    return Resultado


def Verificar_Valores_Faltantes_Criticos(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica valores faltantes en columnas críticas,
    reportando exactamente qué sujetos tienen NaN.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con resultados detallados por sujeto.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Valores faltantes en columnas críticas',
        'sujetos_con_nan': [],
        'aprobado': True
    }

    for Columna in COLUMNAS_CRITICAS:
        if Columna not in Df.columns:
            continue

        # Encontrar filas con NaN.
        Mask_NaN = Df[Columna].isna()
        Indices_NaN = Df[Mask_NaN].index.tolist()

        if Indices_NaN:
            Resultado['aprobado'] = False

            # Reportar cada sujeto con NaN.
            for Idx in Indices_NaN:
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Resultado['sujetos_con_nan'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'columna': Columna
                })

    return Resultado


def Verificar_Rangos_Edad(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que edades estén en rango razonable [18-100],
    reportando cada caso fuera de rango.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos problemáticos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Rangos de edad válidos',
        'casos_fuera_de_rango': [],
        'aprobado': True
    }

    if 'Edad' not in Df.columns:
        Resultado['error'] = "Columna 'Edad' no encontrada"
        Resultado['aprobado'] = False
        return Resultado

    # Verificar rango.
    Mask_Invalida = (Df['Edad'] < 18) | (Df['Edad'] > 100)
    Indices_Invalidos = Df[Mask_Invalida].index.tolist()

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
                'edad': float(Df.loc[Idx, 'Edad'])
                        if pd.notna(Df.loc[Idx, 'Edad'])
                        else None
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
    Genera reporte PDF detallado de verificaciones.

    Parámetros:
    - Resultados: Lista de diccionarios con resultados.
    - Nombre_Base: Nombre de la base verificada.
    - Ruta_Salida: Path donde guardar PDF.

    """

    # Crear documento.
    Archivo_PDF = (
        Ruta_Salida /
        f"Control_01_Construccion_{Nombre_Base}_"
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

    # Estilos.
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

    # Contenido.
    Story = []

    # Título.
    Story.append(Paragraph(
        f"Control 01: Construcción de Bases - {Nombre_Base}",
        Estilo_Titulo
    ))
    Story.append(Paragraph(
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        Estilos['Normal']
    ))
    Story.append(Spacer(1, 20))

    # Resumen ejecutivo.
    Aprobados = sum(1 for R in Resultados if R['aprobado'])
    Total = len(Resultados)

    Color_Resumen = (
        colors.green if Aprobados == Total
        else colors.red
    )

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

        # Detalles específicos según tipo.
        if 'ids_duplicados' in Resultado:
            if Resultado['ids_duplicados']:
                Story.append(Paragraph(
                    f"<b>IDs duplicados encontrados: "
                    f"{len(Resultado['ids_duplicados'])}</b>",
                    Estilos['Normal']
                ))

                # Tabla de duplicados.
                Datos_Tabla = [['ID', 'Filas', 'Repeticiones']]
                for Dup in Resultado['ids_duplicados'][:20]:
                    Datos_Tabla.append([
                        str(Dup['id']),
                        ', '.join(map(str, Dup['filas'])),
                        str(Dup['num_repeticiones'])
                    ])

                Tabla = Table(Datos_Tabla)
                Tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0),
                     colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0),
                     colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1),
                     colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                Story.append(Tabla)

                if len(Resultado['ids_duplicados']) > 20:
                    Story.append(Paragraph(
                        f"... y {len(Resultado['ids_duplicados']) - 20} más",
                        Estilos['Italic']
                    ))

        elif 'sujetos_con_nan' in Resultado:
            if Resultado['sujetos_con_nan']:
                Story.append(Paragraph(
                    f"<b>Sujetos con valores faltantes: "
                    f"{len(Resultado['sujetos_con_nan'])}</b>",
                    Estilos['Normal']
                ))

                # Tabla de NaN.
                Datos_Tabla = [['ID', 'Fila', 'Columna']]
                for Caso in Resultado['sujetos_con_nan'][:30]:
                    Datos_Tabla.append([
                        str(Caso['id']),
                        str(Caso['fila']),
                        Caso['columna']
                    ])

                Tabla = Table(Datos_Tabla)
                Tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0),
                     colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0),
                     colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0),
                     'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1),
                     colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                Story.append(Tabla)

                if len(Resultado['sujetos_con_nan']) > 30:
                    Story.append(Paragraph(
                        f"... y "
                        f"{len(Resultado['sujetos_con_nan']) - 30} "
                        f"más",
                        Estilos['Italic']
                    ))

        elif 'casos_fuera_de_rango' in Resultado:
            if Resultado['casos_fuera_de_rango']:
                Story.append(Paragraph(
                    f"<b>Casos con edad fuera de rango: "
                    f"{len(Resultado['casos_fuera_de_rango'])}</b>",
                    Estilos['Normal']
                ))

                # Tabla de rangos.
                Datos_Tabla = [['ID', 'Fila', 'Edad']]
                for Caso in Resultado['casos_fuera_de_rango'][:30]:
                    Datos_Tabla.append([
                        str(Caso['id']),
                        str(Caso['fila']),
                        str(Caso['edad']) if Caso['edad'] is not None
                        else 'NaN'
                    ])

                Tabla = Table(Datos_Tabla)
                Tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0),
                     colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0),
                     'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                Story.append(Tabla)

                if len(Resultado['casos_fuera_de_rango']) > 30:
                    Story.append(Paragraph(
                        f"... y "
                        f"{len(Resultado['casos_fuera_de_rango']) - 30} "
                        f"más",
                        Estilos['Italic']
                    ))

        Story.append(Spacer(1, 20))

    # Construir PDF.
    Doc.build(Story)
    print(f"\n✓ Reporte PDF generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Control_Construccion_Bases(
    Nombre_Base: str,
    Df: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de construcción de bases.

    Parámetros:
    - Nombre_Base: 'Generales' o 'Ballotage'.
    - Df: DataFrame construido a verificar.

    Retorna:
    - True si todas las verificaciones pasan, False caso
      contrario.

    """

    print("\n" + "="*70)
    print(f"CONTROL 01: CONSTRUCCIÓN DE BASES - {Nombre_Base}")
    print("="*70)

    Resultados = []

    # Verificación 1: IDs únicos.
    print("\n1. Verificando IDs únicos...")
    R1 = Verificar_IDs_Unicos(Df, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    # Verificación 2: Columnas críticas.
    print("\n2. Verificando columnas críticas...")
    R2 = Verificar_Columnas_Criticas(Df, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    # Verificación 3: Tipos de datos.
    print("\n3. Verificando tipos de datos...")
    R3 = Verificar_Tipos_Datos(Df, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    # Verificación 4: Valores faltantes críticos.
    print("\n4. Verificando valores faltantes...")
    R4 = Verificar_Valores_Faltantes_Criticos(Df, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    # Verificación 5: Rangos de edad.
    print("\n5. Verificando rangos de edad...")
    R5 = Verificar_Rangos_Edad(Df, Nombre_Base)
    Resultados.append(R5)
    print(f"   {'✓' if R5['aprobado'] else '✗'} "
          f"{R5['verificacion']}")

    # Generar reporte PDF.
    print("\n6. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    # Resultado final.
    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Construcción correcta")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Control 01 debe ejecutarse importando la función")
    print("Ejecutar_Control_Construccion_Bases()")
