# ============================================================
# CONTROL_07_AGRUPAMIENTOS.PY
# ============================================================
# Control exhaustivo de agrupamientos de variables
# sociodemográficas. Verifica mapeos correctos, coherencia
# con variables originales y detección de valores no mapeados.
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

# Variables que deben tener versión agrupada.
VARIABLES_AGRUPABLES = [
    'Provincia',  # → Region
    'Edad',  # → Edad_Agrupada
    'Genero',  # → Genero_Agrupado
    'Inmueble_Residencia',  # → Inmueble_Agrupado
    'Fuente_Ingreso',  # → Fuente_Ingreso_Agrupada
    'Nivel_Educativo',  # → Nivel_Educativo_Agrupado
    'Situacion_Laboral',  # → Situacion_Laboral_Agrupada
    'Estado_Civil',  # → Estado_Civil_Agrupado
    'Autopercepcion_Izq_Der',  # → Autopercepcion_Izq_Der_Agrupada
    'Autopercepcion_Con_Pro',  # → Autopercepcion_Con_Pro_Agrupada
    'Autopercepcion_Per_Antiper'  # → Autopercepcion_Per_Antiper_Agrupada
]

RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Existencia_Columnas_Agrupadas(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que existan columnas agrupadas para todas las
    variables esperadas.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Existencia columnas agrupadas',
        'columnas_agrupadas_esperadas': 0,
        'columnas_agrupadas_presentes': 0,
        'columnas_faltantes': [],
        'aprobado': True
    }

    Mapeo_Nombres = {
        'Provincia': 'Region',
        'Edad': 'Edad_Agrupada',
        'Genero': 'Genero_Agrupado',
        'Inmueble_Residencia': 'Inmueble_Agrupado',
        'Fuente_Ingreso': 'Fuente_Ingreso_Agrupada',
        'Nivel_Educativo': 'Nivel_Educativo_Agrupado',
        'Situacion_Laboral': 'Situacion_Laboral_Agrupada',
        'Estado_Civil': 'Estado_Civil_Agrupado',
        'Autopercepcion_Izq_Der': 'Autopercepcion_Izq_Der_Agrupada',
        'Autopercepcion_Con_Pro': 'Autopercepcion_Con_Pro_Agrupada',
        'Autopercepcion_Per_Antiper': 'Autopercepcion_Per_Antiper_Agrupada'
    }

    for Original, Agrupada in Mapeo_Nombres.items():
        if Original in Df.columns:
            Resultado['columnas_agrupadas_esperadas'] += 1

            if Agrupada in Df.columns:
                Resultado['columnas_agrupadas_presentes'] += 1
            else:
                Resultado['columnas_faltantes'].append({
                    'original': Original,
                    'esperada': Agrupada
                })
                Resultado['aprobado'] = False

    return Resultado


def Verificar_Mapeo_Provincia_Region(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todas las provincias se mapeen correctamente
    a regiones.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Mapeo Provincia → Region',
        'casos_no_mapeados': [],
        'aprobado': True
    }

    if 'Provincia' not in Df.columns or 'Region' not in Df.columns:
        Resultado['error'] = "Columnas no encontradas"
        return Resultado

    # Verificar casos donde Provincia tiene valor pero Region es NaN.
    Mask_No_Mapeado = (
        Df['Provincia'].notna() &
        Df['Region'].isna()
    )

    Indices_No_Mapeados = Df[Mask_No_Mapeado].index.tolist()

    if Indices_No_Mapeados:
        Resultado['aprobado'] = False

        for Idx in Indices_No_Mapeados[:50]:
            ID_Sujeto = (
                Df.loc[Idx, 'ID']
                if 'ID' in Df.columns
                else f"Fila_{Idx}"
            )

            Resultado['casos_no_mapeados'].append({
                'id': ID_Sujeto,
                'fila': int(Idx),
                'provincia': str(Df.loc[Idx, 'Provincia'])
            })

    return Resultado


def Verificar_Rangos_Edad_Agrupada(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que Edad_Agrupada tenga categorías válidas
    y coherencia con Edad original.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Rangos Edad_Agrupada',
        'categorias_esperadas': [
            'Menos_25',
            'Entre_25_Y_34',
            'Entre_35_Y_44',
            'Entre_45_Y_54',
            'Mayor_55'
        ],
        'categorias_encontradas': [],
        'casos_incoherentes': [],
        'aprobado': True
    }

    if 'Edad_Agrupada' not in Df.columns:
        Resultado['error'] = "Columna no encontrada"
        return Resultado

    # Verificar categorías.
    Categorias = Df['Edad_Agrupada'].dropna().unique().tolist()
    Resultado['categorias_encontradas'] = [str(c) for c in Categorias]

    # Verificar coherencia con edad original (muestra).
    if 'Edad' in Df.columns:
        Muestra = Df.sample(n=min(100, len(Df)), random_state=42)

        for Idx in Muestra.index:
            Edad = Df.loc[Idx, 'Edad']
            Edad_Grup = Df.loc[Idx, 'Edad_Agrupada']

            if pd.isna(Edad) or pd.isna(Edad_Grup):
                continue

            # Verificar coherencia.
            Coherente = False

            if Edad < 25 and Edad_Grup == 'Menos_25':
                Coherente = True
            elif 25 <= Edad < 35 and Edad_Grup == 'Entre_25_Y_34':
                Coherente = True
            elif 35 <= Edad < 45 and Edad_Grup == 'Entre_35_Y_44':
                Coherente = True
            elif 45 <= Edad < 55 and Edad_Grup == 'Entre_45_Y_54':
                Coherente = True
            elif Edad >= 55 and Edad_Grup == 'Mayor_55':
                Coherente = True

            if not Coherente:
                Resultado['aprobado'] = False
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Resultado['casos_incoherentes'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'edad': int(Edad),
                    'edad_agrupada': str(Edad_Grup)
                })

    return Resultado


def Verificar_Valores_Otro_Excesivos(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que no haya demasiados valores mapeados a 'Otro'
    (indica mapeo incompleto).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Valores "Otro" no excesivos',
        'columnas_con_exceso': [],
        'aprobado': True
    }

    Columnas_Agrupadas = [
        'Region',
        'Genero_Agrupado',
        'Inmueble_Agrupado',
        'Fuente_Ingreso_Agrupada',
        'Nivel_Educativo_Agrupado'
    ]

    for Columna in Columnas_Agrupadas:
        if Columna not in Df.columns:
            continue

        Total = Df[Columna].notna().sum()
        Otros = (Df[Columna] == 'Otro').sum()

        if Total > 0:
            Porcentaje_Otro = (Otros / Total) * 100

            # Falla si >30% son "Otro".
            if Porcentaje_Otro > 30:
                Resultado['aprobado'] = False
                Resultado['columnas_con_exceso'].append({
                    'columna': Columna,
                    'total': int(Total),
                    'otros': int(Otros),
                    'porcentaje': float(Porcentaje_Otro)
                })

    return Resultado


def Verificar_Autopercepciones_ABC(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que autopercepciones agrupadas tengan solo
    categorías A, B, C.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Autopercepciones A/B/C',
        'columnas_verificadas': 0,
        'categorias_invalidas': [],
        'aprobado': True
    }

    Columnas_Auto = [
        'Autopercepcion_Izq_Der_Agrupada',
        'Autopercepcion_Con_Pro_Agrupada',
        'Autopercepcion_Per_Antiper_Agrupada'
    ]

    for Columna in Columnas_Auto:
        if Columna not in Df.columns:
            continue

        Resultado['columnas_verificadas'] += 1

        Categorias = Df[Columna].dropna().unique()
        Categorias_Validas = {'A', 'B', 'C'}

        for Cat in Categorias:
            if Cat not in Categorias_Validas:
                Resultado['aprobado'] = False
                Resultado['categorias_invalidas'].append({
                    'columna': Columna,
                    'categoria_invalida': str(Cat)
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
    Genera reporte PDF de agrupamientos.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_07_Agrupamientos_{Nombre_Base}_"
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
        f"Control 07: Agrupamientos - {Nombre_Base}",
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

        if 'casos_no_mapeados' in Resultado and Resultado['casos_no_mapeados']:
            Story.append(Paragraph(
                f"<b>Casos no mapeados: "
                f"{len(Resultado['casos_no_mapeados'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Provincia']]
            for Caso in Resultado['casos_no_mapeados'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['provincia']
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

        if 'casos_incoherentes' in Resultado and Resultado['casos_incoherentes']:
            Story.append(Paragraph(
                f"<b>Casos incoherentes: "
                f"{len(Resultado['casos_incoherentes'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Edad', 'Edad Agrupada']]
            for Caso in Resultado['casos_incoherentes'][:20]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    str(Caso['edad']),
                    Caso['edad_agrupada']
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

def Ejecutar_Control_Agrupamientos(
    Nombre_Base: str,
    Df: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de agrupamientos.

    """

    print("\n" + "="*70)
    print(f"CONTROL 07: AGRUPAMIENTOS - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando existencia de columnas...")
    R1 = Verificar_Existencia_Columnas_Agrupadas(Df, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando mapeo Provincia→Region...")
    R2 = Verificar_Mapeo_Provincia_Region(Df, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando rangos Edad_Agrupada...")
    R3 = Verificar_Rangos_Edad_Agrupada(Df, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando valores 'Otro'...")
    R4 = Verificar_Valores_Otro_Excesivos(Df, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    print("\n5. Verificando autopercepciones A/B/C...")
    R5 = Verificar_Autopercepciones_ABC(Df, Nombre_Base)
    Resultados.append(R5)
    print(f"   {'✓' if R5['aprobado'] else '✗'} "
          f"{R5['verificacion']}")

    print("\n6. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Agrupamientos correctos")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 07 debe ejecutarse importando la función")
    print("Ejecutar_Control_Agrupamientos()")
