# ============================================================
# CONTROL_09_ORDENAMIENTO.PY
# ============================================================
# Control exhaustivo de ordenamiento de columnas. Verifica
# que ID esté primero, agrupación temática correcta, y
# prefijos de nombres aplicados consistentemente.
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

# Orden esperado de grupos de columnas.
GRUPOS_COLUMNAS_ORDEN = [
    'ID',
    'Demograficas',
    'Situacionales',
    'Redes_Sociales',
    'Medios_Prensa',
    'IP_Items',
    'Indices',
    'Variables_Cambio',
    'Categoria_PASO',
    'Variables_Agrupadas',
    'Variables_Dummy'
]

# Prefijos esperados para grupos.
PREFIJOS_ESPERADOS = {
    'IP_Items': 'IP_Item_',
    'Indices': 'Indice_',
    'Variables_Cambio': ['CO_', 'CT_']
}


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_ID_Primera_Columna(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que la columna ID sea la primera del DataFrame.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'ID como primera columna',
        'primera_columna': Df.columns[0],
        'aprobado': True
    }

    if Df.columns[0] != 'ID':
        Resultado['aprobado'] = False

    return Resultado


def Verificar_Agrupacion_Tematica(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que columnas estén agrupadas temáticamente
    (IP juntas, índices juntos, etc.).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Agrupación temática de columnas',
        'problemas': [],
        'aprobado': True
    }

    Columnas = Df.columns.tolist()

    # Verificar que columnas IP estén juntas.
    Columnas_IP = [
        i for i, Col in enumerate(Columnas)
        if Col.startswith('IP_Item_')
    ]

    if Columnas_IP:
        # Verificar que sean consecutivas.
        Diferencias = [
            Columnas_IP[i+1] - Columnas_IP[i]
            for i in range(len(Columnas_IP) - 1)
        ]

        if not all(d == 1 for d in Diferencias):
            Resultado['aprobado'] = False
            Resultado['problemas'].append({
                'grupo': 'IP_Items',
                'mensaje': 'Columnas IP no están consecutivas'
            })

    # Verificar que índices estén juntos.
    Columnas_Indices = [
        i for i, Col in enumerate(Columnas)
        if Col.startswith('Indice_')
    ]

    if Columnas_Indices:
        Diferencias = [
            Columnas_Indices[i+1] - Columnas_Indices[i]
            for i in range(len(Columnas_Indices) - 1)
        ]

        if not all(d == 1 for d in Diferencias):
            Resultado['aprobado'] = False
            Resultado['problemas'].append({
                'grupo': 'Indices',
                'mensaje': 'Columnas de índices no están consecutivas'
            })

    # Verificar variables CO.
    Columnas_CO = [
        i for i, Col in enumerate(Columnas)
        if Col.startswith('CO_')
    ]

    if Columnas_CO:
        Diferencias = [
            Columnas_CO[i+1] - Columnas_CO[i]
            for i in range(len(Columnas_CO) - 1)
        ]

        if not all(d == 1 for d in Diferencias):
            Resultado['aprobado'] = False
            Resultado['problemas'].append({
                'grupo': 'Variables_CO',
                'mensaje': 'Columnas CO no están consecutivas'
            })

    # Verificar variables CT.
    Columnas_CT = [
        i for i, Col in enumerate(Columnas)
        if Col.startswith('CT_')
    ]

    if Columnas_CT:
        Diferencias = [
            Columnas_CT[i+1] - Columnas_CT[i]
            for i in range(len(Columnas_CT) - 1)
        ]

        if not all(d == 1 for d in Diferencias):
            Resultado['aprobado'] = False
            Resultado['problemas'].append({
                'grupo': 'Variables_CT',
                'mensaje': 'Columnas CT no están consecutivas'
            })

    return Resultado


def Verificar_Prefijos_Aplicados(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que prefijos se hayan aplicado correctamente a
    grupos de columnas (Medios_Prensa_, etc.).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Prefijos aplicados correctamente',
        'columnas_sin_prefijo': [],
        'aprobado': True
    }

    # Verificar que medios de prensa tengan prefijo.
    Medios_Esperados = [
        'Ambito_Financiero', 'Prensa_Obrera', 'Diario_Universal',
        'Popular', 'Izquierda_Diario', 'Clarin', 'Perfil',
        'Pagina_12', 'Infobae', 'El_Cronista', 'La_Nacion',
        'Tiempo_Argentino', 'Medios_Prensa_Ninguno'
    ]

    for Medio in Medios_Esperados:
        # Verificar que no exista sin prefijo.
        if Medio in Df.columns:
            Resultado['aprobado'] = False
            Resultado['columnas_sin_prefijo'].append({
                'columna': Medio,
                'prefijo_esperado': 'Medios_Prensa_'
            })

        # Verificar que exista con prefijo.
        Columna_Con_Prefijo = f'Medios_Prensa_{Medio}'
        if Columna_Con_Prefijo not in Df.columns:
            Resultado['aprobado'] = False
            Resultado['columnas_sin_prefijo'].append({
                'columna': Medio,
                'prefijo_esperado': 'Medios_Prensa_',
                'mensaje': 'No existe con prefijo'
            })

    return Resultado


def Verificar_Nombres_Consistentes(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que nombres de columnas sigan convención
    Pascal_Snake_Case y no tengan caracteres inválidos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Nombres consistentes (Pascal_Snake_Case)',
        'columnas_invalidas': [],
        'aprobado': True
    }

    for Columna in Df.columns:
        # Verificar que no tenga espacios.
        if ' ' in Columna:
            Resultado['aprobado'] = False
            Resultado['columnas_invalidas'].append({
                'columna': Columna,
                'problema': 'Contiene espacios'
            })

        # Verificar que no tenga guiones.
        if '-' in Columna:
            Resultado['aprobado'] = False
            Resultado['columnas_invalidas'].append({
                'columna': Columna,
                'problema': 'Contiene guiones'
            })

        # Verificar que no tenga puntos (excepto decimales en datos).
        if '.' in Columna:
            Resultado['aprobado'] = False
            Resultado['columnas_invalidas'].append({
                'columna': Columna,
                'problema': 'Contiene puntos'
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
    Genera reporte PDF de ordenamiento de columnas.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_09_Ordenamiento_{Nombre_Base}_"
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
        f"Control 09: Ordenamiento de Columnas - {Nombre_Base}",
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

        if 'primera_columna' in Resultado:
            Story.append(Paragraph(
                f"Primera columna: {Resultado['primera_columna']}",
                Estilos['Normal']
            ))

        if 'problemas' in Resultado and Resultado['problemas']:
            Story.append(Paragraph(
                f"<b>Problemas encontrados: "
                f"{len(Resultado['problemas'])}</b>",
                Estilos['Normal']
            ))

            for Problema in Resultado['problemas']:
                Story.append(Paragraph(
                    f"- {Problema['grupo']}: {Problema['mensaje']}",
                    Estilos['Normal']
                ))

        if 'columnas_sin_prefijo' in Resultado and Resultado['columnas_sin_prefijo']:
            Story.append(Paragraph(
                f"<b>Columnas sin prefijo: "
                f"{len(Resultado['columnas_sin_prefijo'])}</b>",
                Estilos['Normal']
            ))

            for Col in Resultado['columnas_sin_prefijo'][:30]:
                Mensaje = Col.get('mensaje', 'Sin prefijo esperado')
                Story.append(Paragraph(
                    f"- {Col['columna']}: {Mensaje} "
                    f"(esperado: {Col['prefijo_esperado']})",
                    Estilos['Normal']
                ))

        if 'columnas_invalidas' in Resultado and Resultado['columnas_invalidas']:
            Story.append(Paragraph(
                f"<b>Columnas con nombres inválidos: "
                f"{len(Resultado['columnas_invalidas'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['Columna', 'Problema']]
            for Col in Resultado['columnas_invalidas'][:30]:
                Datos_Tabla.append([
                    Col['columna'],
                    Col['problema']
                ])

            Tabla = Table(Datos_Tabla)
            Tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
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

def Ejecutar_Control_Ordenamiento(
    Nombre_Base: str,
    Df: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de ordenamiento de columnas.

    """

    print("\n" + "="*70)
    print(f"CONTROL 09: ORDENAMIENTO DE COLUMNAS - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando ID como primera columna...")
    R1 = Verificar_ID_Primera_Columna(Df, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando agrupación temática...")
    R2 = Verificar_Agrupacion_Tematica(Df, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando prefijos aplicados...")
    R3 = Verificar_Prefijos_Aplicados(Df, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando nombres consistentes...")
    R4 = Verificar_Nombres_Consistentes(Df, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    print("\n5. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Ordenamiento correcto")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 09 debe ejecutarse importando la función")
    print("Ejecutar_Control_Ordenamiento()")
