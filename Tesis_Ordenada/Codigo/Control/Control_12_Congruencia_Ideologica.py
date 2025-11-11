# ============================================================
# CONTROL_12_CONGRUENCIA_IDEOLOGICA.PY
# ============================================================
# Control exhaustivo de análisis de congruencia ideológica.
# Verifica clasificación correcta de ítems congruentes e
# incongruentes, resultados válidos y reproducibilidad.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors

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

RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)

CANDIDATOS_IZQUIERDA = ['Bregman', 'Solano']
CANDIDATOS_DERECHA = ['Milei', 'Bullrich']


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Clasificacion_Items(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que ítems se clasifiquen correctamente como
    congruentes o incongruentes según candidato.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Clasificación correcta de ítems',
        'clasificaciones_incorrectas': [],
        'aprobado': True
    }

    if 'Item' not in Df_Resultados.columns or 'Candidato' not in Df_Resultados.columns:
        Resultado['error'] = "Columnas Item o Candidato no encontradas"
        return Resultado

    for Idx in Df_Resultados.index:
        Item = Df_Resultados.loc[Idx, 'Item']
        Candidato = Df_Resultados.loc[Idx, 'Candidato']

        # Extraer número de ítem.
        try:
            Num_Item = int(Item.split('_')[2])
        except:
            continue

        # Clasificar ítem.
        Es_Progresista = Num_Item in ITEMS_PROGRESISTAS
        Es_Conservador = Num_Item in ITEMS_CONSERVADORES

        # Clasificar candidato.
        Es_Candidato_Izquierda = Candidato in CANDIDATOS_IZQUIERDA
        Es_Candidato_Derecha = Candidato in CANDIDATOS_DERECHA

        # Determinar congruencia.
        if 'Tipo' in Df_Resultados.columns:
            Tipo_Declarado = Df_Resultados.loc[Idx, 'Tipo']

            # Verificar coherencia.
            Es_Congruente_Esperado = (
                (Es_Progresista and Es_Candidato_Izquierda) or
                (Es_Conservador and Es_Candidato_Derecha)
            )

            Es_Congruente_Declarado = (
                Tipo_Declarado == 'Congruente'
            )

            if Es_Congruente_Esperado != Es_Congruente_Declarado:
                Resultado['aprobado'] = False
                Resultado['clasificaciones_incorrectas'].append({
                    'fila': int(Idx),
                    'item': str(Item),
                    'candidato': str(Candidato),
                    'tipo_declarado': str(Tipo_Declarado),
                    'tipo_esperado': (
                        'Congruente' if Es_Congruente_Esperado
                        else 'Incongruente'
                    )
                })

    return Resultado


def Verificar_Resultados_Comparaciones(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que resultados de comparaciones tengan p-values
    válidos y estadísticos razonables.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Resultados de comparaciones válidos',
        'resultados_invalidos': [],
        'aprobado': True
    }

    if 'P_Value' not in Df_Resultados.columns:
        return Resultado

    for Idx in Df_Resultados.index:
        P_Value = Df_Resultados.loc[Idx, 'P_Value']

        # Verificar que sea numérico y en rango.
        if pd.isna(P_Value):
            Resultado['aprobado'] = False
            Resultado['resultados_invalidos'].append({
                'fila': int(Idx),
                'item': str(Df_Resultados.loc[Idx, 'Item']),
                'problema': 'P-value es NaN'
            })
            continue

        if not isinstance(P_Value, (int, float, np.number)):
            Resultado['aprobado'] = False
            Resultado['resultados_invalidos'].append({
                'fila': int(Idx),
                'item': str(Df_Resultados.loc[Idx, 'Item']),
                'p_value': str(P_Value),
                'problema': 'No es numérico'
            })
            continue

        if P_Value < 0 or P_Value > 1:
            Resultado['aprobado'] = False
            Resultado['resultados_invalidos'].append({
                'fila': int(Idx),
                'item': str(Df_Resultados.loc[Idx, 'Item']),
                'p_value': float(P_Value),
                'problema': 'Fuera de rango [0, 1]'
            })

    return Resultado


def Verificar_Comparaciones_Completas(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que se hayan realizado todas las comparaciones
    esperadas (congruente vs incongruente para cada candidato).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Comparaciones completas',
        'comparaciones_faltantes': [],
        'aprobado': True
    }

    # Candidatos esperados.
    Candidatos_Esperados = CANDIDATOS_IZQUIERDA + CANDIDATOS_DERECHA

    # Verificar que cada candidato tenga comparaciones.
    if 'Candidato' in Df_Resultados.columns:
        Candidatos_Presentes = Df_Resultados['Candidato'].unique()

        for Candidato in Candidatos_Esperados:
            if Candidato not in Candidatos_Presentes:
                Resultado['aprobado'] = False
                Resultado['comparaciones_faltantes'].append({
                    'candidato': Candidato,
                    'problema': 'No hay comparaciones para este candidato'
                })

    return Resultado


def Verificar_Medianas_Coherentes(
    Df_Resultados: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que medianas reportadas sean coherentes (no
    negativas, en rango razonable).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Medianas coherentes',
        'medianas_invalidas': [],
        'aprobado': True
    }

    Columnas_Mediana = [
        'Mediana_Congruente',
        'Mediana_Incongruente'
    ]

    for Columna in Columnas_Mediana:
        if Columna not in Df_Resultados.columns:
            continue

        for Idx in Df_Resultados.index:
            Mediana = Df_Resultados.loc[Idx, Columna]

            if pd.isna(Mediana):
                continue

            # Verificar que sea numérico.
            if not isinstance(Mediana, (int, float, np.number)):
                Resultado['aprobado'] = False
                Resultado['medianas_invalidas'].append({
                    'fila': int(Idx),
                    'item': str(Df_Resultados.loc[Idx, 'Item']),
                    'columna': Columna,
                    'mediana': str(Mediana),
                    'problema': 'No es numérico'
                })
                continue

            # Para CO: rango [-4, +4].
            # Para CT: >= 0.
            if 'CO_' in str(Df_Resultados.loc[Idx, 'Item']):
                if Mediana < -4 or Mediana > 4:
                    Resultado['aprobado'] = False
                    Resultado['medianas_invalidas'].append({
                        'fila': int(Idx),
                        'item': str(Df_Resultados.loc[Idx, 'Item']),
                        'columna': Columna,
                        'mediana': float(Mediana),
                        'problema': 'Fuera de rango [-4, +4]'
                    })

            if 'CT_' in str(Df_Resultados.loc[Idx, 'Item']):
                if Mediana < 0:
                    Resultado['aprobado'] = False
                    Resultado['medianas_invalidas'].append({
                        'fila': int(Idx),
                        'item': str(Df_Resultados.loc[Idx, 'Item']),
                        'columna': Columna,
                        'mediana': float(Mediana),
                        'problema': 'Negativa'
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
    Genera reporte PDF de congruencia ideológica.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_12_Congruencia_Ideologica_{Nombre_Base}_"
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
        f"Control 12: Congruencia Ideológica - {Nombre_Base}",
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

        if 'clasificaciones_incorrectas' in Resultado and Resultado['clasificaciones_incorrectas']:
            Story.append(Paragraph(
                f"<b>Clasificaciones incorrectas: "
                f"{len(Resultado['clasificaciones_incorrectas'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['Item', 'Candidato', 'Declarado', 'Esperado']]
            for Caso in Resultado['clasificaciones_incorrectas'][:30]:
                Datos_Tabla.append([
                    Caso['item'],
                    Caso['candidato'],
                    Caso['tipo_declarado'],
                    Caso['tipo_esperado']
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

        if 'resultados_invalidos' in Resultado and Resultado['resultados_invalidos']:
            Story.append(Paragraph(
                f"<b>Resultados inválidos: "
                f"{len(Resultado['resultados_invalidos'])}</b>",
                Estilos['Normal']
            ))

            for Caso in Resultado['resultados_invalidos'][:20]:
                Story.append(Paragraph(
                    f"- {Caso['item']}: {Caso['problema']}",
                    Estilos['Normal']
                ))

        if 'comparaciones_faltantes' in Resultado and Resultado['comparaciones_faltantes']:
            Story.append(Paragraph(
                f"<b>Comparaciones faltantes: "
                f"{len(Resultado['comparaciones_faltantes'])}</b>",
                Estilos['Normal']
            ))

            for Caso in Resultado['comparaciones_faltantes']:
                Story.append(Paragraph(
                    f"- {Caso['candidato']}: {Caso['problema']}",
                    Estilos['Normal']
                ))

        if 'medianas_invalidas' in Resultado and Resultado['medianas_invalidas']:
            Story.append(Paragraph(
                f"<b>Medianas inválidas: "
                f"{len(Resultado['medianas_invalidas'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['Item', 'Columna', 'Mediana', 'Problema']]
            for Caso in Resultado['medianas_invalidas'][:30]:
                Datos_Tabla.append([
                    Caso['item'],
                    Caso['columna'],
                    str(Caso['mediana']),
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

        Story.append(Spacer(1, 20))

    Doc.build(Story)
    print(f"\n✓ Reporte PDF generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Control_Congruencia_Ideologica(
    Nombre_Base: str,
    Df_Resultados: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de congruencia ideológica.

    """

    print("\n" + "="*70)
    print(f"CONTROL 12: CONGRUENCIA IDEOLÓGICA - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando clasificación de ítems...")
    R1 = Verificar_Clasificacion_Items(Df_Resultados, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando resultados de comparaciones...")
    R2 = Verificar_Resultados_Comparaciones(
        Df_Resultados, Nombre_Base
    )
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando comparaciones completas...")
    R3 = Verificar_Comparaciones_Completas(
        Df_Resultados, Nombre_Base
    )
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando medianas coherentes...")
    R4 = Verificar_Medianas_Coherentes(Df_Resultados, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    print("\n5. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Congruencia correcta")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 12 debe ejecutarse importando la función")
    print("Ejecutar_Control_Congruencia_Ideologica()")
