# ============================================================
# CONTROL_16_EJECUTAR_TODOS.PY
# ============================================================
# Script maestro que ejecuta todos los controles
# secuencialmente y genera reporte consolidado.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors
import sys
import io

# Configurar codificación UTF-8 para Windows.
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8',
        errors='replace'
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer,
        encoding='utf-8',
        errors='replace'
    )

# Agregar rutas.
Ruta_Actual = Path(__file__).parent
sys.path.append(str(Ruta_Actual))

# Importar controles.
from Control_01_Construccion_Bases import (
    Ejecutar_Control_Construccion_Bases
)
from Control_02_Calculo_Indices import (
    Ejecutar_Control_Calculo_Indices
)
from Control_03_Variables_Cambio import (
    Ejecutar_Control_Variables_Cambio
)
from Control_04_Limpieza_Datos import (
    Ejecutar_Control_Limpieza_Datos
)
from Control_05_Relleno_Medianas import (
    Ejecutar_Control_Relleno_Medianas
)
from Control_06_Redes_Y_Medios import (
    Ejecutar_Control_Redes_Y_Medios
)
from Control_07_Agrupamientos import (
    Ejecutar_Control_Agrupamientos
)
from Control_08_Variables_Dummy import (
    Ejecutar_Control_Variables_Dummy
)
from Control_09_Ordenamiento import (
    Ejecutar_Control_Ordenamiento
)
from Control_10_Clusters import (
    Ejecutar_Control_Clusters
)
from Control_15_Identidad_Bases import (
    Ejecutar_Control_Identidad_Bases
)


# ============================================================
# CONSTANTES
# ============================================================

RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)

RUTA_BASES_ORIGINALES = (
    Path(__file__).parent.parent.parent.parent / "Data" /
    "Bases definitivas"
)

RUTA_BASES_NUEVAS = (
    Path(__file__).parent.parent.parent / "Tablas" /
    "Bases_Procesadas"
)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def Cargar_Bases() -> Dict[str, pd.DataFrame]:

    """
    Carga las bases nuevas generadas por el pipeline.

    """

    print("\n" + "="*70)
    print("CARGANDO BASES DE DATOS NUEVAS")
    print("="*70)

    Bases = {}

    Archivo_Generales = (
        RUTA_BASES_NUEVAS / "Base_Final_Generales.xlsx"
    )
    Archivo_Ballotage = (
        RUTA_BASES_NUEVAS / "Base_Final_Ballotage.xlsx"
    )

    if Archivo_Generales.exists():
        print(f"\n✓ Cargando Generales: {Archivo_Generales}")
        Bases['Generales'] = pd.read_excel(Archivo_Generales)
    else:
        print(f"\n✗ No se encontró: {Archivo_Generales}")

    if Archivo_Ballotage.exists():
        print(f"\n✓ Cargando Ballotage: {Archivo_Ballotage}")
        Bases['Ballotage'] = pd.read_excel(Archivo_Ballotage)
    else:
        print(f"\n✗ No se encontró: {Archivo_Ballotage}")

    return Bases


# ============================================================
# GENERACIÓN DE REPORTE CONSOLIDADO
# ============================================================

def Generar_Reporte_Consolidado(
    Resultados_Controles: List[Dict],
    Ruta_Salida: Path
) -> None:

    """
    Genera reporte PDF consolidado de todos los controles.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_Consolidado_"
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
        fontSize=18,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30
    )
    Estilo_Subtitulo = ParagraphStyle(
        'CustomHeading',
        parent=Estilos['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12
    )

    Story = []

    Story.append(Paragraph(
        "Reporte Consolidado de Controles - Tesis",
        Estilo_Titulo
    ))
    Story.append(Paragraph(
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        Estilos['Normal']
    ))
    Story.append(Spacer(1, 30))

    # Resumen ejecutivo.
    Aprobados = sum(
        1 for R in Resultados_Controles if R['aprobado']
    )
    Total = len(Resultados_Controles)

    Story.append(Paragraph(
        f"<b>RESUMEN EJECUTIVO</b>",
        Estilo_Subtitulo
    ))

    Story.append(Paragraph(
        f"Controles aprobados: {Aprobados}/{Total}",
        Estilos['Normal']
    ))

    if Aprobados == Total:
        Story.append(Paragraph(
            "<font color='green'><b>✓ TODOS LOS CONTROLES "
            "APROBADOS</b></font>",
            Estilos['Normal']
        ))
    else:
        Story.append(Paragraph(
            f"<font color='red'><b>✗ {Total - Aprobados} "
            f"CONTROLES FALLIDOS</b></font>",
            Estilos['Normal']
        ))

    Story.append(Spacer(1, 20))

    # Tabla resumen.
    Story.append(Paragraph(
        "<b>Detalle de Controles</b>",
        Estilo_Subtitulo
    ))

    Datos_Tabla = [['Control', 'Nombre', 'Base', 'Estado']]

    for Resultado in Resultados_Controles:
        Numero = Resultado['numero_control']
        Nombre = Resultado['nombre_control']
        Base = Resultado.get('nombre_base', 'N/A')
        Estado = "✓ OK" if Resultado['aprobado'] else "✗ FALLÓ"

        Datos_Tabla.append([
            f"Control {Numero:02d}",
            Nombre,
            Base,
            Estado
        ])

    Tabla = Table(Datos_Tabla)
    Tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    Story.append(Tabla)
    Story.append(Spacer(1, 30))

    # Detalles de controles fallidos.
    Fallidos = [R for R in Resultados_Controles if not R['aprobado']]

    if Fallidos:
        Story.append(Paragraph(
            "<b>CONTROLES FALLIDOS - DETALLES</b>",
            Estilo_Subtitulo
        ))

        for Resultado in Fallidos:
            Story.append(Paragraph(
                f"<b>Control {Resultado['numero_control']:02d}: "
                f"{Resultado['nombre_control']}</b>",
                Estilos['Heading3']
            ))

            Story.append(Paragraph(
                f"Base: {Resultado.get('nombre_base', 'N/A')}",
                Estilos['Normal']
            ))

            if 'error' in Resultado:
                Story.append(Paragraph(
                    f"Error: {Resultado['error']}",
                    Estilos['Normal']
                ))

            Story.append(Spacer(1, 12))

    Doc.build(Story)
    print(f"\n✓ Reporte consolidado generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Todos_Los_Controles() -> None:

    """
    Ejecuta todos los controles secuencialmente y genera
    reporte consolidado.

    """

    print("\n" + "="*70)
    print("INICIANDO EJECUCIÓN DE TODOS LOS CONTROLES")
    print("="*70)

    Inicio = datetime.now()
    Resultados_Controles = []

    # Cargar bases.
    Bases = Cargar_Bases()

    if not Bases:
        print("\n✗ No se pudieron cargar las bases. Abortando.")
        return

    # Ejecutar controles para cada base.
    for Nombre_Base, Df in Bases.items():
        print(f"\n{'='*70}")
        print(f"PROCESANDO BASE: {Nombre_Base}")
        print(f"{'='*70}")

        # Control 01: Construcción de bases.
        try:
            Aprobado_01 = Ejecutar_Control_Construccion_Bases(
                Nombre_Base, Df
            )
            Resultados_Controles.append({
                'numero_control': 1,
                'nombre_control': 'Construcción de bases',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_01
            })
        except Exception as e:
            print(f"\n✗ Error en Control 01: {e}")
            Resultados_Controles.append({
                'numero_control': 1,
                'nombre_control': 'Construcción de bases',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

        # Control 02: Cálculo de índices.
        try:
            Aprobado_02 = Ejecutar_Control_Calculo_Indices(
                Nombre_Base, Df
            )
            Resultados_Controles.append({
                'numero_control': 2,
                'nombre_control': 'Cálculo de índices',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_02
            })
        except Exception as e:
            print(f"\n✗ Error en Control 02: {e}")
            Resultados_Controles.append({
                'numero_control': 2,
                'nombre_control': 'Cálculo de índices',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

        # Control 03: Variables de cambio.
        try:
            Aprobado_03 = Ejecutar_Control_Variables_Cambio(
                Nombre_Base, Df
            )
            Resultados_Controles.append({
                'numero_control': 3,
                'nombre_control': 'Variables de cambio',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_03
            })
        except Exception as e:
            print(f"\n✗ Error en Control 03: {e}")
            Resultados_Controles.append({
                'numero_control': 3,
                'nombre_control': 'Variables de cambio',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

        # Control 06: Redes y medios.
        try:
            Aprobado_06 = Ejecutar_Control_Redes_Y_Medios(
                Nombre_Base, Df
            )
            Resultados_Controles.append({
                'numero_control': 6,
                'nombre_control': 'Redes y medios',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_06
            })
        except Exception as e:
            print(f"\n✗ Error en Control 06: {e}")
            Resultados_Controles.append({
                'numero_control': 6,
                'nombre_control': 'Redes y medios',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

        # Control 07: Agrupamientos.
        try:
            Aprobado_07 = Ejecutar_Control_Agrupamientos(
                Nombre_Base, Df
            )
            Resultados_Controles.append({
                'numero_control': 7,
                'nombre_control': 'Agrupamientos',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_07
            })
        except Exception as e:
            print(f"\n✗ Error en Control 07: {e}")
            Resultados_Controles.append({
                'numero_control': 7,
                'nombre_control': 'Agrupamientos',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

        # Control 08: Variables dummy.
        try:
            Aprobado_08 = Ejecutar_Control_Variables_Dummy(
                Nombre_Base, Df
            )
            Resultados_Controles.append({
                'numero_control': 8,
                'nombre_control': 'Variables dummy',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_08
            })
        except Exception as e:
            print(f"\n✗ Error en Control 08: {e}")
            Resultados_Controles.append({
                'numero_control': 8,
                'nombre_control': 'Variables dummy',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

        # Control 09: Ordenamiento.
        try:
            Aprobado_09 = Ejecutar_Control_Ordenamiento(
                Nombre_Base, Df
            )
            Resultados_Controles.append({
                'numero_control': 9,
                'nombre_control': 'Ordenamiento',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_09
            })
        except Exception as e:
            print(f"\n✗ Error en Control 09: {e}")
            Resultados_Controles.append({
                'numero_control': 9,
                'nombre_control': 'Ordenamiento',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

        # Control 10: Clusters.
        try:
            Aprobado_10 = Ejecutar_Control_Clusters(
                Nombre_Base, Df
            )
            Resultados_Controles.append({
                'numero_control': 10,
                'nombre_control': 'Clusters',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_10
            })
        except Exception as e:
            print(f"\n✗ Error en Control 10: {e}")
            Resultados_Controles.append({
                'numero_control': 10,
                'nombre_control': 'Clusters',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

        # Control 15: Identidad de bases.
        try:
            Aprobado_15 = Ejecutar_Control_Identidad_Bases(
                Nombre_Base
            )
            Resultados_Controles.append({
                'numero_control': 15,
                'nombre_control': 'Identidad de bases',
                'nombre_base': Nombre_Base,
                'aprobado': Aprobado_15
            })
        except Exception as e:
            print(f"\n✗ Error en Control 15: {e}")
            Resultados_Controles.append({
                'numero_control': 15,
                'nombre_control': 'Identidad de bases',
                'nombre_base': Nombre_Base,
                'aprobado': False,
                'error': str(e)
            })

    # Generar reporte consolidado.
    print("\n" + "="*70)
    print("GENERANDO REPORTE CONSOLIDADO")
    print("="*70)

    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_Consolidado(Resultados_Controles, RUTA_REPORTES)

    # Resumen final.
    Fin = datetime.now()
    Duracion = Fin - Inicio

    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)

    Aprobados = sum(1 for R in Resultados_Controles if R['aprobado'])
    Total = len(Resultados_Controles)

    print(f"\nControles ejecutados: {Total}")
    print(f"Controles aprobados: {Aprobados}")
    print(f"Controles fallidos: {Total - Aprobados}")
    print(f"Duración total: {Duracion}")

    if Aprobados == Total:
        print("\n✓ TODOS LOS CONTROLES APROBADOS")
    else:
        print(f"\n✗ {Total - Aprobados} CONTROLES FALLARON")

    print("="*70)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    Ejecutar_Todos_Los_Controles()
