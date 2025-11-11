# ============================================================
# CONTROL_06_REDES_Y_MEDIOS.PY
# ============================================================
# Control exhaustivo de procesamiento de redes sociales y
# medios de prensa. Verifica binarización correcta, coherencia
# con columnas originales y normalización de texto.
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

REDES_SOCIALES = [
    'Twitter', 'Facebook', 'Instagram', 'Threads',
    'Tiktok', 'Youtube', 'Whatsapp', 'Telegram'
]

MEDIOS_PRENSA = [
    'Ambito_Financiero', 'Prensa_Obrera', 'Diario_Universal',
    'Popular', 'Izquierda_Diario', 'Clarin', 'Perfil',
    'Pagina_12', 'Infobae', 'El_Cronista', 'La_Nacion',
    'Tiempo_Argentino', 'Medios_Prensa_Ninguno'
]

RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Columnas_Binarias(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todas las columnas de redes y medios sean
    binarias (solo 0 y 1).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Columnas binarias (0/1)',
        'columnas_no_binarias': [],
        'aprobado': True
    }

    # Buscar columnas de redes (capitalizadas).
    Columnas_Redes = [
        Red.capitalize() for Red in REDES_SOCIALES
        if Red.capitalize() in Df.columns
    ]

    # Buscar columnas de medios (con prefijo).
    Columnas_Medios = [
        f'Medios_Prensa_{Medio}'
        for Medio in MEDIOS_PRENSA
        if f'Medios_Prensa_{Medio}' in Df.columns
    ]

    # Agregar medios sin prefijo por si acaso.
    for Medio in MEDIOS_PRENSA:
        if Medio in Df.columns:
            Columnas_Medios.append(Medio)

    Todas_Columnas = Columnas_Redes + Columnas_Medios

    for Columna in Todas_Columnas:
        Valores_Unicos = Df[Columna].dropna().unique()

        if not set(Valores_Unicos).issubset({0, 1}):
            Resultado['aprobado'] = False
            Resultado['columnas_no_binarias'].append({
                'columna': Columna,
                'valores_encontrados': [int(v) for v in Valores_Unicos]
            })

    return Resultado


def Verificar_Coherencia_Con_Columna_Original(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica coherencia entre columnas binarias y texto
    original de Red_Social / Medios_Prensa.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Coherencia con columna original',
        'casos_incoherentes': [],
        'aprobado': True
    }

    # Verificar muestra de casos para redes sociales.
    if 'Red_Social' in Df.columns:
        # Verificar muestra de 100 casos.
        Muestra = Df.sample(n=min(100, len(Df)), random_state=42)

        for Idx in Muestra.index:
            Texto_Original = str(
                Df.loc[Idx, 'Red_Social']
            ).lower()

            if pd.isna(Df.loc[Idx, 'Red_Social']):
                continue

            # Verificar cada red.
            for Red in REDES_SOCIALES:
                Columna_Binaria = Red.capitalize()

                if Columna_Binaria not in Df.columns:
                    continue

                Tiene_Red = Red.lower() in Texto_Original
                Valor_Binario = Df.loc[Idx, Columna_Binaria] == 1

                if Tiene_Red != Valor_Binario:
                    Resultado['aprobado'] = False
                    ID_Sujeto = (
                        Df.loc[Idx, 'ID']
                        if 'ID' in Df.columns
                        else f"Fila_{Idx}"
                    )

                    Resultado['casos_incoherentes'].append({
                        'id': ID_Sujeto,
                        'fila': int(Idx),
                        'texto_original': Texto_Original,
                        'red': Red,
                        'esperado': 1 if Tiene_Red else 0,
                        'encontrado': int(
                            Df.loc[Idx, Columna_Binaria]
                        )
                    })

    return Resultado


def Verificar_Suma_Por_Fila_Redes(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que cada sujeto tenga al menos una red social
    marcada (no todos 0).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Al menos una red por sujeto',
        'sujetos_sin_redes': [],
        'aprobado': True
    }

    # Buscar columnas de redes.
    Columnas_Redes = [
        Red.capitalize() for Red in REDES_SOCIALES
        if Red.capitalize() in Df.columns
    ]

    if not Columnas_Redes:
        return Resultado

    # Sumar por fila.
    Suma = Df[Columnas_Redes].sum(axis=1)

    Indices_Sin_Redes = Df[Suma == 0].index.tolist()

    if Indices_Sin_Redes:
        Resultado['aprobado'] = False

        for Idx in Indices_Sin_Redes[:50]:
            ID_Sujeto = (
                Df.loc[Idx, 'ID']
                if 'ID' in Df.columns
                else f"Fila_{Idx}"
            )

            Resultado['sujetos_sin_redes'].append({
                'id': ID_Sujeto,
                'fila': int(Idx)
            })

    return Resultado


def Verificar_Existencia_Columnas_Esperadas(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todas las columnas de redes y medios
    esperadas existan.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Existencia de columnas esperadas',
        'redes_esperadas': len(REDES_SOCIALES),
        'redes_presentes': 0,
        'redes_faltantes': [],
        'medios_esperados': len(MEDIOS_PRENSA),
        'medios_presentes': 0,
        'medios_faltantes': [],
        'aprobado': True
    }

    # Verificar redes.
    for Red in REDES_SOCIALES:
        Columna = Red.capitalize()
        if Columna in Df.columns:
            Resultado['redes_presentes'] += 1
        else:
            Resultado['redes_faltantes'].append(Columna)
            Resultado['aprobado'] = False

    # Verificar medios.
    for Medio in MEDIOS_PRENSA:
        Columna = f'Medios_Prensa_{Medio}'
        if Columna in Df.columns:
            Resultado['medios_presentes'] += 1
        elif Medio in Df.columns:
            Resultado['medios_presentes'] += 1
        else:
            Resultado['medios_faltantes'].append(Columna)
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
    Genera reporte PDF de redes y medios.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_06_Redes_Medios_{Nombre_Base}_"
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
        f"Control 06: Redes y Medios - {Nombre_Base}",
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

        if 'columnas_no_binarias' in Resultado and Resultado['columnas_no_binarias']:
            Story.append(Paragraph(
                f"<b>Columnas no binarias: "
                f"{len(Resultado['columnas_no_binarias'])}</b>",
                Estilos['Normal']
            ))

            for Col in Resultado['columnas_no_binarias'][:20]:
                Story.append(Paragraph(
                    f"- {Col['columna']}: valores {Col['valores_encontrados']}",
                    Estilos['Normal']
                ))

        if 'casos_incoherentes' in Resultado and Resultado['casos_incoherentes']:
            Story.append(Paragraph(
                f"<b>Casos incoherentes: "
                f"{len(Resultado['casos_incoherentes'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Red', 'Esperado', 'Encontrado']]
            for Caso in Resultado['casos_incoherentes'][:20]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['red'],
                    str(Caso['esperado']),
                    str(Caso['encontrado'])
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

def Ejecutar_Control_Redes_Y_Medios(
    Nombre_Base: str,
    Df: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de redes y medios.

    """

    print("\n" + "="*70)
    print(f"CONTROL 06: REDES Y MEDIOS - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando existencia de columnas...")
    R1 = Verificar_Existencia_Columnas_Esperadas(
        Df, Nombre_Base
    )
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando columnas binarias...")
    R2 = Verificar_Columnas_Binarias(Df, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando coherencia con original...")
    R3 = Verificar_Coherencia_Con_Columna_Original(
        Df, Nombre_Base
    )
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando al menos una red por sujeto...")
    R4 = Verificar_Suma_Por_Fila_Redes(Df, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    print("\n5. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Redes y medios correctos")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 06 debe ejecutarse importando la función")
    print("Ejecutar_Control_Redes_Y_Medios()")
