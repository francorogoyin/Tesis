# ============================================================
# CONTROL_08_VARIABLES_DUMMY.PY
# ============================================================
# Control exhaustivo de creación de variables dummy. Verifica
# que one-hot encoding sea correcto, columnas binarias, suma
# por fila coherente y sin multicolinealidad.
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

# Variables que deben tener dummies creadas.
VARIABLES_CON_DUMMIES = [
    'Sexo',
    'Nivel_Educativo',
    'Region',
    'Edad_Agrupada',
    'Categoria_PASO_2023'
]


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Existencia_Dummies(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que se hayan creado columnas dummy para todas
    las variables categóricas esperadas.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Existencia de variables dummy',
        'variables_sin_dummies': [],
        'aprobado': True
    }

    for Variable in VARIABLES_CON_DUMMIES:
        # Buscar columnas que empiecen con el nombre de la variable.
        Columnas_Dummy = [
            Col for Col in Df.columns
            if Col.startswith(f'{Variable}_')
        ]

        if not Columnas_Dummy:
            Resultado['aprobado'] = False
            Resultado['variables_sin_dummies'].append(Variable)

    return Resultado


def Verificar_Columnas_Dummy_Binarias(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todas las columnas dummy sean binarias
    (solo 0 y 1).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Columnas dummy binarias (0/1)',
        'columnas_no_binarias': [],
        'aprobado': True
    }

    # Buscar todas las columnas dummy.
    Columnas_Dummy = []
    for Variable in VARIABLES_CON_DUMMIES:
        Columnas_Dummy.extend([
            Col for Col in Df.columns
            if Col.startswith(f'{Variable}_')
        ])

    for Columna in Columnas_Dummy:
        Valores_Unicos = Df[Columna].dropna().unique()

        if not set(Valores_Unicos).issubset({0, 1}):
            Resultado['aprobado'] = False
            Resultado['columnas_no_binarias'].append({
                'columna': Columna,
                'valores_encontrados': [int(v) for v in Valores_Unicos]
            })

    return Resultado


def Verificar_Suma_Por_Fila(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que la suma de dummies por fila sea 1 para cada
    variable categórica (solo una categoría activa).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Suma de dummies = 1 por variable',
        'casos_invalidos': [],
        'aprobado': True
    }

    for Variable in VARIABLES_CON_DUMMIES:
        # Buscar columnas dummy para esta variable.
        Columnas_Dummy = [
            Col for Col in Df.columns
            if Col.startswith(f'{Variable}_')
        ]

        if not Columnas_Dummy:
            continue

        # Sumar por fila.
        Suma = Df[Columnas_Dummy].sum(axis=1)

        # Encontrar filas donde suma != 1.
        Indices_Invalidos = Df[Suma != 1].index.tolist()

        if Indices_Invalidos:
            Resultado['aprobado'] = False

            for Idx in Indices_Invalidos[:50]:
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Resultado['casos_invalidos'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'variable': Variable,
                    'suma': int(Suma.loc[Idx])
                })

    return Resultado


def Verificar_Coherencia_Con_Original(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que valores dummy sean coherentes con la columna
    original categórica (muestra de 100 casos).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Coherencia con columna original',
        'casos_incoherentes': [],
        'aprobado': True
    }

    # Verificar muestra de 100 casos.
    Muestra = Df.sample(n=min(100, len(Df)), random_state=42)

    for Variable in VARIABLES_CON_DUMMIES:
        if Variable not in Df.columns:
            continue

        # Buscar columnas dummy.
        Columnas_Dummy = [
            Col for Col in Df.columns
            if Col.startswith(f'{Variable}_')
        ]

        if not Columnas_Dummy:
            continue

        for Idx in Muestra.index:
            Valor_Original = Df.loc[Idx, Variable]

            if pd.isna(Valor_Original):
                continue

            # Construir nombre de columna dummy esperada.
            Columna_Esperada = f'{Variable}_{Valor_Original}'

            # Verificar si existe y está activa.
            if Columna_Esperada in Df.columns:
                if Df.loc[Idx, Columna_Esperada] != 1:
                    Resultado['aprobado'] = False
                    ID_Sujeto = (
                        Df.loc[Idx, 'ID']
                        if 'ID' in Df.columns
                        else f"Fila_{Idx}"
                    )

                    Resultado['casos_incoherentes'].append({
                        'id': ID_Sujeto,
                        'fila': int(Idx),
                        'variable': Variable,
                        'valor_original': str(Valor_Original),
                        'columna_esperada': Columna_Esperada,
                        'valor_encontrado': int(
                            Df.loc[Idx, Columna_Esperada]
                        )
                    })

    return Resultado


def Verificar_Sin_Multicolinealidad(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que no se hayan incluido todas las categorías
    (debe faltar una para evitar multicolinealidad).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Sin multicolinealidad (n-1 dummies)',
        'variables_con_problema': [],
        'aprobado': True
    }

    for Variable in VARIABLES_CON_DUMMIES:
        if Variable not in Df.columns:
            continue

        # Contar categorías únicas en original.
        Categorias_Originales = Df[Variable].nunique()

        # Contar columnas dummy creadas.
        Columnas_Dummy = [
            Col for Col in Df.columns
            if Col.startswith(f'{Variable}_')
        ]

        Num_Dummies = len(Columnas_Dummy)

        # Debe haber n-1 dummies (se omite categoría de referencia).
        if Num_Dummies == Categorias_Originales:
            Resultado['aprobado'] = False
            Resultado['variables_con_problema'].append({
                'variable': Variable,
                'categorias_originales': int(Categorias_Originales),
                'dummies_creadas': int(Num_Dummies),
                'esperado': int(Categorias_Originales - 1)
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
    Genera reporte PDF de variables dummy.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_08_Variables_Dummy_{Nombre_Base}_"
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
        f"Control 08: Variables Dummy - {Nombre_Base}",
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

        if 'variables_sin_dummies' in Resultado and Resultado['variables_sin_dummies']:
            Story.append(Paragraph(
                f"<b>Variables sin dummies: "
                f"{len(Resultado['variables_sin_dummies'])}</b>",
                Estilos['Normal']
            ))

            for Var in Resultado['variables_sin_dummies']:
                Story.append(Paragraph(
                    f"- {Var}",
                    Estilos['Normal']
                ))

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

        if 'casos_invalidos' in Resultado and Resultado['casos_invalidos']:
            Story.append(Paragraph(
                f"<b>Casos con suma inválida: "
                f"{len(Resultado['casos_invalidos'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Variable', 'Suma']]
            for Caso in Resultado['casos_invalidos'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['variable'],
                    str(Caso['suma'])
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

            Datos_Tabla = [['ID', 'Fila', 'Variable', 'Esperado', 'Encontrado']]
            for Caso in Resultado['casos_incoherentes'][:20]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['variable'],
                    Caso['columna_esperada'],
                    str(Caso['valor_encontrado'])
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

def Ejecutar_Control_Variables_Dummy(
    Nombre_Base: str,
    Df: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de variables dummy.

    """

    print("\n" + "="*70)
    print(f"CONTROL 08: VARIABLES DUMMY - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando existencia de dummies...")
    R1 = Verificar_Existencia_Dummies(Df, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando columnas binarias...")
    R2 = Verificar_Columnas_Dummy_Binarias(Df, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando suma por fila...")
    R3 = Verificar_Suma_Por_Fila(Df, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando coherencia con original...")
    R4 = Verificar_Coherencia_Con_Original(Df, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    print("\n5. Verificando sin multicolinealidad...")
    R5 = Verificar_Sin_Multicolinealidad(Df, Nombre_Base)
    Resultados.append(R5)
    print(f"   {'✓' if R5['aprobado'] else '✗'} "
          f"{R5['verificacion']}")

    print("\n6. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Variables dummy correctas")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 08 debe ejecutarse importando la función")
    print("Ejecutar_Control_Variables_Dummy()")
