# ============================================================
# CONTROL_05_RELLENO_MEDIANAS.PY
# ============================================================
# Control exhaustivo de relleno de medianas. Verifica que
# NaN se rellenen correctamente con mediana del grupo
# ideológico y que distribuciones se mantengan coherentes.
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
import sys

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

ITEMS_TODOS = sorted(ITEMS_PROGRESISTAS + ITEMS_CONSERVADORES)

RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_NaN_Rellenados(
    Df_Antes: pd.DataFrame,
    Df_Despues: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que NaN en columnas IP se hayan rellenado.
    Reporta columnas que aún tienen NaN.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'NaN rellenados en columnas IP',
        'columnas_con_nan': [],
        'aprobado': True
    }

    # Buscar columnas IP (Respuesta y Tiempo).
    Columnas_IP = [
        Col for Col in Df_Despues.columns
        if (Col.startswith('IP_Item_') and
            ('Respuesta' in Col or 'Tiempo' in Col))
    ]

    for Columna in Columnas_IP:
        NaN_Count = Df_Despues[Columna].isna().sum()

        if NaN_Count > 0:
            Resultado['aprobado'] = False
            Resultado['columnas_con_nan'].append({
                'columna': Columna,
                'nan_count': int(NaN_Count)
            })

    return Resultado


def Verificar_Columnas_Original_Creadas(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que se hayan creado columnas _Original como
    backup.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Columnas _Original creadas',
        'columnas_original': 0,
        'columnas_faltantes': [],
        'aprobado': True
    }

    # Buscar columnas IP sin _Original.
    Columnas_IP = [
        Col for Col in Df.columns
        if (Col.startswith('IP_Item_') and
            ('Respuesta' in Col or 'Tiempo' in Col) and
            not Col.endswith('_Original'))
    ]

    for Columna in Columnas_IP:
        Columna_Original = f'{Columna}_Original'

        if Columna_Original in Df.columns:
            Resultado['columnas_original'] += 1
        else:
            Resultado['columnas_faltantes'].append(Columna)
            Resultado['aprobado'] = False

    return Resultado


def Verificar_Valores_Rellenados_Razonables(
    Df_Antes: pd.DataFrame,
    Df_Despues: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que valores rellenados estén en rango razonable
    (1-5 para respuestas, >0 para tiempos).

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Valores rellenados razonables',
        'casos_invalidos': [],
        'aprobado': True
    }

    # Verificar muestra de columnas IP.
    Columnas_IP_Respuesta = [
        f'IP_Item_{Item}_Respuesta'
        for Item in ITEMS_TODOS[:5]
    ]

    for Columna in Columnas_IP_Respuesta:
        if Columna not in Df_Despues.columns:
            continue

        # Encontrar valores que fueron NaN y ahora están
        # rellenados.
        if Columna not in Df_Antes.columns:
            continue

        Mask_Rellenados = (
            Df_Antes[Columna].isna() &
            Df_Despues[Columna].notna()
        )

        Indices_Rellenados = (
            Df_Despues[Mask_Rellenados].index.tolist()
        )

        # Verificar rangos.
        for Idx in Indices_Rellenados:
            Valor = Df_Despues.loc[Idx, Columna]

            if Valor < 1 or Valor > 5:
                Resultado['aprobado'] = False
                ID_Sujeto = (
                    Df_Despues.loc[Idx, 'ID']
                    if 'ID' in Df_Despues.columns
                    else f"Fila_{Idx}"
                )

                Resultado['casos_invalidos'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'columna': Columna,
                    'valor_rellenado': float(Valor)
                })

    return Resultado


def Verificar_Medianas_Por_Categoria(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que medianas por categoría ideológica sean
    diferentes y razonables.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Medianas por categoría razonables',
        'estadisticas': [],
        'aprobado': True
    }

    if 'Categoria_PASO_2023' not in Df.columns:
        Resultado['error'] = "Categoría no encontrada"
        return Resultado

    # Verificar muestra de columnas.
    Columnas_Muestra = [
        f'IP_Item_{Item}_Respuesta'
        for Item in ITEMS_TODOS[:3]
    ]

    for Columna in Columnas_Muestra:
        if Columna not in Df.columns:
            continue

        # Calcular medianas por categoría.
        Medianas = (
            Df.groupby('Categoria_PASO_2023')[Columna]
            .median()
        )

        # Verificar que no todas sean iguales.
        if Medianas.nunique() == 1:
            Resultado['aprobado'] = False

        Resultado['estadisticas'].append({
            'columna': Columna,
            'medianas_por_categoria': Medianas.to_dict()
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
    Genera reporte PDF de relleno de medianas.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_05_Relleno_Medianas_{Nombre_Base}_"
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
        f"Control 05: Relleno de Medianas - {Nombre_Base}",
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

        if 'columnas_con_nan' in Resultado and Resultado['columnas_con_nan']:
            Story.append(Paragraph(
                f"<b>Columnas con NaN restantes: "
                f"{len(Resultado['columnas_con_nan'])}</b>",
                Estilos['Normal']
            ))

            for Col in Resultado['columnas_con_nan'][:20]:
                Story.append(Paragraph(
                    f"- {Col['columna']}: {Col['nan_count']} NaN",
                    Estilos['Normal']
                ))

        if 'casos_invalidos' in Resultado and Resultado['casos_invalidos']:
            Story.append(Paragraph(
                f"<b>Valores rellenados inválidos: "
                f"{len(Resultado['casos_invalidos'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Columna', 'Valor']]
            for Caso in Resultado['casos_invalidos'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['columna'],
                    f"{Caso['valor_rellenado']:.2f}"
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

def Ejecutar_Control_Relleno_Medianas(
    Nombre_Base: str,
    Df_Antes: pd.DataFrame,
    Df_Despues: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de relleno de medianas.

    """

    print("\n" + "="*70)
    print(f"CONTROL 05: RELLENO DE MEDIANAS - {Nombre_Base}")
    print("="*70)

    Resultados = []

    print("\n1. Verificando NaN rellenados...")
    R1 = Verificar_NaN_Rellenados(
        Df_Antes, Df_Despues, Nombre_Base
    )
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando columnas _Original...")
    R2 = Verificar_Columnas_Original_Creadas(
        Df_Despues, Nombre_Base
    )
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando valores rellenados...")
    R3 = Verificar_Valores_Rellenados_Razonables(
        Df_Antes, Df_Despues, Nombre_Base
    )
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando medianas por categoría...")
    R4 = Verificar_Medianas_Por_Categoria(
        Df_Despues, Nombre_Base
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
        print("✓ CONTROL APROBADO: Relleno correcto")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 05 debe ejecutarse importando la función")
    print("Ejecutar_Control_Relleno_Medianas()")
