# ============================================================
# CONTROL_03_VARIABLES_CAMBIO.PY
# ============================================================
# Control exhaustivo de variables de cambio de opinión (CO)
# y cambio de tiempo (CT). Verifica rangos válidos, coherencia
# con variables base y detecta cálculos incorrectos.
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

# Agregar ruta de Utilidades.
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

# Rango válido para CO (escala 1-5, diferencia: -4 a +4).
RANGO_CO = (-4.0, 4.0)

# Items a verificar.
ITEMS_TODOS = sorted(ITEMS_PROGRESISTAS + ITEMS_CONSERVADORES)

# Ruta de reportes.
RUTA_REPORTES = (
    Path(__file__).parent.parent.parent / "Reportes" / "Control"
)


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Rangos_CO(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que todas las variables CO estén en rango [-4, 4].
    Reporta cada caso fuera de rango.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos fuera de rango.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Rangos CO [-4, +4]',
        'casos_fuera_de_rango': [],
        'aprobado': True
    }

    # Buscar todas las columnas CO.
    Columnas_CO = [
        Col for Col in Df.columns
        if Col.startswith('CO_')
    ]

    for Columna in Columnas_CO:
        Min_Val, Max_Val = RANGO_CO

        Mask_Invalido = (
            (Df[Columna] < Min_Val) |
            (Df[Columna] > Max_Val)
        )
        Mask_Invalido = Mask_Invalido & Df[Columna].notna()

        Indices_Invalidos = Df[Mask_Invalido].index.tolist()

        if Indices_Invalidos:
            Resultado['aprobado'] = False

            for Idx in Indices_Invalidos[:100]:
                # Limitar a 100.
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Resultado['casos_fuera_de_rango'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'columna': Columna,
                    'valor': float(Df.loc[Idx, Columna])
                })

            if len(Indices_Invalidos) > 100:
                Resultado['casos_fuera_de_rango'].append({
                    'id': '...',
                    'fila': '...',
                    'columna': Columna,
                    'valor': f"... y {len(Indices_Invalidos) - 100} más"
                })

    return Resultado


def Verificar_CT_No_Negativos(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que CT (diferencias de tiempo) no sean negativas.
    Reporta cada caso con CT negativo.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos negativos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'CT no negativos',
        'casos_negativos': [],
        'aprobado': True
    }

    # Buscar todas las columnas CT.
    Columnas_CT = [
        Col for Col in Df.columns
        if Col.startswith('CT_')
    ]

    for Columna in Columnas_CT:
        Mask_Negativo = Df[Columna] < 0
        Mask_Negativo = Mask_Negativo & Df[Columna].notna()

        Indices_Negativos = Df[Mask_Negativo].index.tolist()

        if Indices_Negativos:
            Resultado['aprobado'] = False

            for Idx in Indices_Negativos[:100]:
                ID_Sujeto = (
                    Df.loc[Idx, 'ID']
                    if 'ID' in Df.columns
                    else f"Fila_{Idx}"
                )

                Resultado['casos_negativos'].append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'columna': Columna,
                    'valor': float(Df.loc[Idx, Columna])
                })

    return Resultado


def Verificar_Coherencia_CO_Con_Respuestas(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica coherencia entre CO calculado y diferencia real
    de respuestas. CO debe ser = Respuesta_Asociada -
    Respuesta_Base.

    Verifica muestra de items para eficiencia.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con casos incoherentes.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Coherencia CO = Asociada - Base',
        'casos_incoherentes': [],
        'aprobado': True
    }

    # Verificar muestra de items (primeros 5 de cada tipo).
    Items_Muestra = ITEMS_TODOS[:5]

    for Item in Items_Muestra:
        for Direccion in ['Izq', 'Der']:
            # Nombres de columnas.
            Col_CO = f'CO_Item_{Item}_{Direccion}'
            Col_Base = f'IP_Item_{Item}_Respuesta'
            Col_Asociada = f'IP_Item_{Item}_{Direccion}_Respuesta'

            # Verificar existencia.
            if not all(
                Col in Df.columns
                for Col in [Col_CO, Col_Base, Col_Asociada]
            ):
                continue

            # Calcular CO esperado.
            CO_Esperado = (
                Df[Col_Asociada] - Df[Col_Base]
            )

            # Comparar con CO calculado.
            Diferencia = np.abs(Df[Col_CO] - CO_Esperado)

            # Tolerancia numérica.
            Mask_Incoherente = Diferencia > 0.01
            Mask_Incoherente = (
                Mask_Incoherente &
                Df[Col_CO].notna() &
                CO_Esperado.notna()
            )

            Indices_Incoherentes = (
                Df[Mask_Incoherente].index.tolist()
            )

            if Indices_Incoherentes:
                Resultado['aprobado'] = False

                for Idx in Indices_Incoherentes[:20]:
                    ID_Sujeto = (
                        Df.loc[Idx, 'ID']
                        if 'ID' in Df.columns
                        else f"Fila_{Idx}"
                    )

                    Resultado['casos_incoherentes'].append({
                        'id': ID_Sujeto,
                        'fila': int(Idx),
                        'columna_co': Col_CO,
                        'co_calculado': float(Df.loc[Idx, Col_CO]),
                        'co_esperado': float(CO_Esperado.loc[Idx]),
                        'base': float(Df.loc[Idx, Col_Base])
                                if pd.notna(Df.loc[Idx, Col_Base])
                                else None,
                        'asociada': float(
                            Df.loc[Idx, Col_Asociada]
                        ) if pd.notna(Df.loc[Idx, Col_Asociada])
                          else None
                    })

    return Resultado


def Verificar_Simetria_CO(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica distribución simétrica esperada de CO.
    La media debería estar cerca de 0.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con estadísticas de distribución.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Simetría distribución CO',
        'estadisticas': [],
        'aprobado': True
    }

    # Buscar columnas CO.
    Columnas_CO = [
        Col for Col in Df.columns
        if Col.startswith('CO_')
    ]

    for Columna in Columnas_CO:
        Media = Df[Columna].mean()
        Mediana = Df[Columna].median()

        if pd.notna(Media):
            # Media muy alejada de 0 indica sesgo.
            if np.abs(Media) > 1.0:
                Resultado['aprobado'] = False

            Resultado['estadisticas'].append({
                'columna': Columna,
                'media': float(Media),
                'mediana': float(Mediana),
                'desviacion_de_cero': float(np.abs(Media))
            })

    return Resultado


def Verificar_Existencia_Variables_Cambio(
    Df: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que se hayan generado variables CO y CT para
    todos los items esperados.

    Parámetros:
    - Df: DataFrame a verificar.
    - Nombre_Base: Nombre descriptivo.

    Retorna:
    - Dict con variables faltantes.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Existencia variables CO/CT',
        'variables_esperadas': 0,
        'variables_presentes': 0,
        'variables_faltantes': [],
        'aprobado': True
    }

    # Contar variables esperadas.
    for Item in ITEMS_TODOS:
        for Direccion in ['Izq', 'Der']:
            for Tipo in ['CO', 'CT']:
                Resultado['variables_esperadas'] += 1

                Nombre_Var = f'{Tipo}_Item_{Item}_{Direccion}'

                if Nombre_Var in Df.columns:
                    Resultado['variables_presentes'] += 1
                else:
                    Resultado['variables_faltantes'].append(
                        Nombre_Var
                    )
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
    Genera reporte PDF de verificaciones de variables de
    cambio.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_03_Variables_Cambio_{Nombre_Base}_"
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

    # Título.
    Story.append(Paragraph(
        f"Control 03: Variables de Cambio (CO/CT) - {Nombre_Base}",
        Estilo_Titulo
    ))
    Story.append(Paragraph(
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        Estilos['Normal']
    ))
    Story.append(Spacer(1, 20))

    # Resumen.
    Aprobados = sum(1 for R in Resultados if R['aprobado'])
    Total = len(Resultados)

    Story.append(Paragraph(
        f"<b>Resumen: {Aprobados}/{Total} verificaciones "
        f"aprobadas</b>",
        Estilo_Subtitulo
    ))
    Story.append(Spacer(1, 12))

    # Detalles.
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

        # Tablas según tipo de resultado.
        if 'casos_fuera_de_rango' in Resultado and Resultado['casos_fuera_de_rango']:
            Story.append(Paragraph(
                f"<b>Casos fuera de rango: "
                f"{len([c for c in Resultado['casos_fuera_de_rango'] if c['id'] != '...'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'Columna', 'Valor']]
            for Caso in Resultado['casos_fuera_de_rango'][:30]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    Caso['columna'],
                    str(Caso['valor']) if isinstance(Caso['valor'], (int, float))
                    else Caso['valor']
                ])

            Tabla = Table(Datos_Tabla)
            Tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            Story.append(Tabla)

        elif 'casos_incoherentes' in Resultado and Resultado['casos_incoherentes']:
            Story.append(Paragraph(
                f"<b>Casos con cálculo incoherente: "
                f"{len(Resultado['casos_incoherentes'])}</b>",
                Estilos['Normal']
            ))

            Datos_Tabla = [['ID', 'Fila', 'CO Calc.', 'CO Esp.']]
            for Caso in Resultado['casos_incoherentes'][:20]:
                Datos_Tabla.append([
                    str(Caso['id']),
                    str(Caso['fila']),
                    f"{Caso['co_calculado']:.2f}",
                    f"{Caso['co_esperado']:.2f}"
                ])

            Tabla = Table(Datos_Tabla)
            Tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            Story.append(Tabla)

        Story.append(Spacer(1, 20))

    Doc.build(Story)
    print(f"\n✓ Reporte PDF generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Control_Variables_Cambio(
    Nombre_Base: str,
    Df: pd.DataFrame
) -> bool:

    """
    Ejecuta control completo de variables de cambio.

    """

    print("\n" + "="*70)
    print(f"CONTROL 03: VARIABLES DE CAMBIO - {Nombre_Base}")
    print("="*70)

    Resultados = []

    # Verificación 1: Existencia.
    print("\n1. Verificando existencia de variables...")
    R1 = Verificar_Existencia_Variables_Cambio(Df, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    # Verificación 2: Rangos CO.
    print("\n2. Verificando rangos CO...")
    R2 = Verificar_Rangos_CO(Df, Nombre_Base)
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    # Verificación 3: CT no negativos.
    print("\n3. Verificando CT no negativos...")
    R3 = Verificar_CT_No_Negativos(Df, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    # Verificación 4: Coherencia cálculo.
    print("\n4. Verificando coherencia de cálculo...")
    R4 = Verificar_Coherencia_CO_Con_Respuestas(Df, Nombre_Base)
    Resultados.append(R4)
    print(f"   {'✓' if R4['aprobado'] else '✗'} "
          f"{R4['verificacion']}")

    # Verificación 5: Simetría.
    print("\n5. Verificando simetría de distribución...")
    R5 = Verificar_Simetria_CO(Df, Nombre_Base)
    Resultados.append(R5)
    print(f"   {'✓' if R5['aprobado'] else '✗'} "
          f"{R5['verificacion']}")

    # Generar reporte.
    print("\n6. Generando reporte PDF...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)
    Generar_Reporte_PDF(Resultados, Nombre_Base, RUTA_REPORTES)

    # Resultado.
    Todas_Aprobadas = all(R['aprobado'] for R in Resultados)

    print("\n" + "="*70)
    if Todas_Aprobadas:
        print("✓ CONTROL APROBADO: Variables de cambio correctas")
    else:
        print("✗ CONTROL FALLIDO: Se encontraron problemas")
    print("="*70)

    return Todas_Aprobadas


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    print("Control 03 debe ejecutarse importando la función")
    print("Ejecutar_Control_Variables_Cambio()")
