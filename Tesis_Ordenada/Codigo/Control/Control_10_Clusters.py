# ============================================================
# CONTROL_10_CLUSTERS.PY
# ============================================================
# Control exhaustivo de carga de variables de clusters.
# Verifica que columnas se carguen correctamente, merge por ID
# exitoso, distribuciones balanceadas y sin NaN.
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

# Columnas de cluster esperadas.
COLUMNAS_CLUSTER_ESPERADAS = [
    'Cluster_Kmeans',
    'Cluster_Jerarquico',
    'Cluster_DBSCAN'
]


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Existencia_Columnas_Cluster(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todas las columnas de cluster esperadas
    existan en el DataFrame.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Existencia de columnas de cluster',
        'columnas_faltantes': [],
        'aprobado': True
    }

    for Columna in COLUMNAS_CLUSTER_ESPERADAS:
        if Columna not in Df.columns:
            Resultado['aprobado'] = False
            Resultado['columnas_faltantes'].append(Columna)

    return Resultado


def Verificar_Merge_Por_ID(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que el merge por ID haya sido exitoso, sin filas
    perdidas ni duplicadas.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Merge por ID exitoso',
        'duplicados_encontrados': [],
        'aprobado': True
    }

    if 'ID' not in Df.columns:
        Resultado['aprobado'] = False
        Resultado['error'] = "Columna ID no encontrada"
        return Resultado

    # Verificar duplicados.
    Duplicados = Df[Df.duplicated(subset='ID', keep=False)]

    if not Duplicados.empty:
        Resultado['aprobado'] = False

        for ID_Dup in Duplicados['ID'].unique():
            Filas = Df[Df['ID'] == ID_Dup].index.tolist()
            Resultado['duplicados_encontrados'].append({
                'id': ID_Dup,
                'filas': [int(f) for f in Filas]
            })

    return Resultado


def Verificar_Sin_NaN_En_Clusters(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que no haya valores NaN en columnas de cluster.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Sin NaN en columnas de cluster',
        'columnas_con_nan': [],
        'aprobado': True
    }

    for Columna in COLUMNAS_CLUSTER_ESPERADAS:
        if Columna not in Df.columns:
            continue

        NaN_Count = Df[Columna].isna().sum()

        if NaN_Count > 0:
            Resultado['aprobado'] = False
            Resultado['columnas_con_nan'].append({
                'columna': Columna,
                'nan_count': int(NaN_Count)
            })

    return Resultado


def Verificar_Distribucion_Clusters(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que distribución de clusters no esté muy
    desbalanceada (ningún cluster < 5% del total).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Distribución de clusters balanceada',
        'distribuciones': [],
        'clusters_desbalanceados': [],
        'aprobado': True
    }

    Total = len(Df)

    for Columna in COLUMNAS_CLUSTER_ESPERADAS:
        if Columna not in Df.columns:
            continue

        # Calcular distribución.
        Distribucion = Df[Columna].value_counts()
        Porcentajes = (Distribucion / Total * 100).to_dict()

        Resultado['distribuciones'].append({
            'columna': Columna,
            'distribucion': {
                str(k): f"{v:.1f}%" for k, v in Porcentajes.items()
            }
        })

        # Verificar que ningún cluster sea < 5%.
        for Cluster, Porcentaje in Porcentajes.items():
            if Porcentaje < 5.0:
                Resultado['aprobado'] = False
                Resultado['clusters_desbalanceados'].append({
                    'columna': Columna,
                    'cluster': str(Cluster),
                    'porcentaje': f"{Porcentaje:.1f}%",
                    'cantidad': int(Distribucion[Cluster])
                })

    return Resultado


def Verificar_Valores_Cluster_Validos(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que valores de cluster sean enteros positivos
    o etiquetas válidas.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Valores de cluster válidos',
        'valores_invalidos': [],
        'aprobado': True
    }

    for Columna in COLUMNAS_CLUSTER_ESPERADAS:
        if Columna not in Df.columns:
            continue

        Valores_Unicos = Df[Columna].dropna().unique()

        for Valor in Valores_Unicos:
            # Verificar que sea entero o string.
            if not isinstance(Valor, (int, np.integer, str)):
                Resultado['aprobado'] = False
                Resultado['valores_invalidos'].append({
                    'columna': Columna,
                    'valor': str(Valor),
                    'tipo': str(type(Valor))
                })

            # Si es numérico, debe ser >= 0 o -1 (noise en DBSCAN).
            if isinstance(Valor, (int, np.integer)):
                if Valor < -1:
                    Resultado['aprobado'] = False
                    Resultado['valores_invalidos'].append({
                        'columna': Columna,
                        'valor': int(Valor),
                        'problema': 'Valor numérico < -1'
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
    Genera reporte PDF de variables de cluster.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_10_Clusters_{Nombre_Base}_"
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
        f"Control 10: Variables de Cluster - {Nombre_Base}",
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

        if 'duplicados_encontrados' in Resultado and Resultado['duplicados_encontrados']:
            Story.append(Paragraph(
                f"<b>Duplicados encontrados: "
                f"{len(Resultado['duplicados_encontrados'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Filas']]
            for Dup in Resultado['duplicados_encontrados'][:30]:
                Datos_Tabla.append([
                    str(Dup['id']),
                    str(Dup['filas'])
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

        if 'columnas_con_nan' in Resultado and Resultado['columnas_con_nan']:
            Story.append(Paragraph(
                f"<b>Columnas con NaN: "
                f"{len(Resultado['columnas_con_nan'])}</b>",
                Estilos['Normal']
            ))

            for Col in Resultado['columnas_con_nan']:
                Story.append(Paragraph(
                    f"- {Col['columna']}: {Col['nan_count']} NaN",
                    Estilos['Normal']
                ))

        if 'distribuciones' in Resultado and Resultado['distribuciones']:
            Story.append(Paragraph(
                "<b>Distribución de clusters:</b>",
                Estilos['Normal']
            ))

            for Dist in Resultado['distribuciones']:
                Story.append(Paragraph(
                    f"<b>{Dist['columna']}:</b>",
                    Estilos['Normal']
                ))

                for Cluster, Porcentaje in Dist['distribucion'].items():
                    Story.append(Paragraph(
                        f"  - Cluster {Cluster}: {Porcentaje}",
                        Estilos['Normal']
                    ))

        if 'clusters_desbalanceados' in Resultado and Resultado['clusters_desbalanceados']:
            Story.append(Paragraph(
                f"<b>Clusters desbalanceados (< 5%): "
                f"{len(Resultado['clusters_desbalanceados'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['Columna', 'Cluster', 'Porcentaje', 'Cantidad']]
            for Cluster in Resultado['clusters_desbalanceados']:
                Datos_Tabla.append([
                    Cluster['columna'],
                    Cluster['cluster'],
                    Cluster['porcentaje'],
                    str(Cluster['cantidad'])
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

        if 'valores_invalidos' in Resultado and Resultado['valores_invalidos']:
            Story.append(Paragraph(
                f"<b>Valores inválidos: "
                f"{len(Resultado['valores_invalidos'])}</b>",
                Estilos['Normal']
            ))

            for Val in Resultado['valores_invalidos'][:20]:
                Problema = Val.get('problema', f"Tipo: {Val.get('tipo', 'N/A')}")
                Story.append(Paragraph(
                    f"- {Val['columna']}: valor {Val['valor']} ({Problema})",
                    Estilos['Normal']
                ))

        Story.append(Spacer(1, 20))

    Doc.build(Story)
    print(f"\n✓ Reporte PDF generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Control_Clusters(
    Nombre_Base: str,
    Df: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de variables de cluster.

    """

    print("\n" + "="*70)
    print(f"CONTROL 10: VARIABLES DE CLUSTER - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando existencia de columnas...")
    R1 = Verificar_Existencia_Columnas_Cluster(Df, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando merge por ID...")
    R2 = Verificar_Merge_Por_ID(Df, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando sin NaN...")
    R3 = Verificar_Sin_NaN_En_Clusters(Df, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando distribución balanceada...")
    R4 = Verificar_Distribucion_Clusters(Df, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    print("\n5. Verificando valores válidos...")
    R5 = Verificar_Valores_Cluster_Validos(Df, Nombre_Base)
    Resultados.append(R5)
    print(f"   {'✓' if R5['aprobado'] else '✗'} "
          f"{R5['verificacion']}")

    print("\n6. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Variables de cluster correctas")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 10 debe ejecutarse importando la función")
    print("Ejecutar_Control_Clusters()")
