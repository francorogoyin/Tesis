# ============================================================
# CONTROL_15_IDENTIDAD_BASES.PY
# ============================================================
# Control exhaustivo de identidad entre bases procesadas en
# Tesis_Ordenada y bases definitivas del proyecto original.
# Verifica reproducibilidad exacta: dimensiones, columnas y
# valores celda por celda.
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

RUTA_PROYECTO_ORIGINAL = Path(
    "C:/Users/Patricio/Documents/Codigo/Python/"
    "Investigacion/Tesis/Data/Bases definitivas"
)

RUTA_PROYECTO_ORDENADO = (
    Path(__file__).parent.parent.parent / "Tablas" /
    "Bases_Procesadas"
)

ARCHIVOS_COMPARACION = {
    'Generales': {
        'original': 'Bases finalesGenerales.xlsx',
        'ordenado': 'Base_Final_Generales.xlsx'
    },
    'Ballotage': {
        'original': 'Bases finalesBallotage.xlsx',
        'ordenado': 'Base_Final_Ballotage.xlsx'
    }
}

TOLERANCIA_NUMERICA = 1e-10


# ============================================================
# FUNCIONES DE VERIFICACIÓN
# ============================================================

def Verificar_Dimensiones(
    Df_Original: pd.DataFrame,
    Df_Ordenado: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que dimensiones (filas y columnas) sean
    idénticas entre bases.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Dimensiones idénticas',
        'filas_original': len(Df_Original),
        'filas_ordenado': len(Df_Ordenado),
        'columnas_original': len(Df_Original.columns),
        'columnas_ordenado': len(Df_Ordenado.columns),
        'aprobado': True
    }

    if len(Df_Original) != len(Df_Ordenado):
        Resultado['aprobado'] = False
        Resultado['diferencia_filas'] = (
            len(Df_Ordenado) - len(Df_Original)
        )

    if len(Df_Original.columns) != len(Df_Ordenado.columns):
        Resultado['aprobado'] = False
        Resultado['diferencia_columnas'] = (
            len(Df_Ordenado.columns) - len(Df_Original.columns)
        )

    return Resultado


def Verificar_Columnas_Identicas(
    Df_Original: pd.DataFrame,
    Df_Ordenado: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que nombres y orden de columnas sean idénticos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Columnas idénticas',
        'columnas_solo_original': [],
        'columnas_solo_ordenado': [],
        'orden_diferente': False,
        'aprobado': True
    }

    Set_Original = set(Df_Original.columns)
    Set_Ordenado = set(Df_Ordenado.columns)

    Solo_Original = Set_Original - Set_Ordenado
    Solo_Ordenado = Set_Ordenado - Set_Original

    if Solo_Original:
        Resultado['aprobado'] = False
        Resultado['columnas_solo_original'] = list(Solo_Original)

    if Solo_Ordenado:
        Resultado['aprobado'] = False
        Resultado['columnas_solo_ordenado'] = list(Solo_Ordenado)

    # Verificar orden.
    if list(Df_Original.columns) != list(Df_Ordenado.columns):
        Resultado['orden_diferente'] = True

        # Encontrar primera diferencia.
        for i, (C1, C2) in enumerate(
            zip(Df_Original.columns, Df_Ordenado.columns)
        ):
            if C1 != C2:
                Resultado['primera_diferencia_posicion'] = i
                Resultado['primera_diferencia_original'] = C1
                Resultado['primera_diferencia_ordenado'] = C2
                break

    return Resultado


def Verificar_Valores_Identicos(
    Df_Original: pd.DataFrame,
    Df_Ordenado: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que valores sean idénticos celda por celda.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Valores idénticos celda por celda',
        'columnas_diferentes': [],
        'aprobado': True
    }

    # Solo comparar columnas comunes.
    Columnas_Comunes = list(
        set(Df_Original.columns) & set(Df_Ordenado.columns)
    )

    if not Columnas_Comunes:
        Resultado['aprobado'] = False
        Resultado['error'] = "No hay columnas comunes"
        return Resultado

    for Columna in Columnas_Comunes:
        Serie_Original = Df_Original[Columna]
        Serie_Ordenado = Df_Ordenado[Columna]

        # Verificar tipos.
        if Serie_Original.dtype != Serie_Ordenado.dtype:
            Resultado['aprobado'] = False
            Resultado['columnas_diferentes'].append({
                'columna': Columna,
                'tipo_diferencia': 'dtype',
                'dtype_original': str(Serie_Original.dtype),
                'dtype_ordenado': str(Serie_Ordenado.dtype)
            })
            continue

        # Comparar valores.
        if pd.api.types.is_numeric_dtype(Serie_Original):
            # Comparación numérica con tolerancia.
            Diferencias_Mask = ~np.isclose(
                Serie_Original,
                Serie_Ordenado,
                rtol=TOLERANCIA_NUMERICA,
                atol=TOLERANCIA_NUMERICA,
                equal_nan=True
            )
        else:
            # Comparación exacta.
            Diferencias_Mask = (Serie_Original != Serie_Ordenado)

            # Manejar NaN.
            Nan_Mask = (
                Serie_Original.isna() & Serie_Ordenado.isna()
            )
            Diferencias_Mask = Diferencias_Mask & ~Nan_Mask

        Num_Diferencias = Diferencias_Mask.sum()

        if Num_Diferencias > 0:
            Resultado['aprobado'] = False

            # Reportar primeras 10 diferencias.
            Indices_Diff = Df_Original[Diferencias_Mask].index.tolist()

            Casos = []
            for Idx in Indices_Diff[:10]:
                ID_Sujeto = (
                    Df_Original.loc[Idx, 'ID']
                    if 'ID' in Df_Original.columns
                    else f"Fila_{Idx}"
                )

                Casos.append({
                    'id': ID_Sujeto,
                    'fila': int(Idx),
                    'valor_original': str(
                        Serie_Original.loc[Idx]
                    ),
                    'valor_ordenado': str(
                        Serie_Ordenado.loc[Idx]
                    )
                })

            Resultado['columnas_diferentes'].append({
                'columna': Columna,
                'tipo_diferencia': 'valores',
                'num_diferencias': int(Num_Diferencias),
                'porcentaje': float(
                    Num_Diferencias / len(Serie_Original) * 100
                ),
                'casos_ejemplo': Casos
            })

    return Resultado


def Verificar_Tipos_Datos(
    Df_Original: pd.DataFrame,
    Df_Ordenado: pd.DataFrame,
    Nombre_Base: str
) -> Dict:

    """
    Verifica que tipos de datos de columnas sean idénticos.

    """

    Resultado = {
        'nombre_base': Nombre_Base,
        'verificacion': 'Tipos de datos idénticos',
        'tipos_diferentes': [],
        'aprobado': True
    }

    Columnas_Comunes = list(
        set(Df_Original.columns) & set(Df_Ordenado.columns)
    )

    for Columna in Columnas_Comunes:
        Tipo_Original = Df_Original[Columna].dtype
        Tipo_Ordenado = Df_Ordenado[Columna].dtype

        if Tipo_Original != Tipo_Ordenado:
            Resultado['aprobado'] = False
            Resultado['tipos_diferentes'].append({
                'columna': Columna,
                'tipo_original': str(Tipo_Original),
                'tipo_ordenado': str(Tipo_Ordenado)
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
    Genera reporte PDF de verificación de identidad.

    """

    Archivo_PDF = (
        Ruta_Salida /
        f"Control_15_Identidad_Bases_{Nombre_Base}_"
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
        f"Control 15: Identidad de Bases - {Nombre_Base}",
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

        # Dimensiones.
        if 'filas_original' in Resultado:
            Story.append(Paragraph(
                f"Original: {Resultado['filas_original']} filas, "
                f"{Resultado['columnas_original']} columnas<br/>"
                f"Ordenado: {Resultado['filas_ordenado']} filas, "
                f"{Resultado['columnas_ordenado']} columnas",
                Estilos['Normal']
            ))

            if 'diferencia_filas' in Resultado:
                Story.append(Paragraph(
                    f"<font color='red'>Diferencia filas: "
                    f"{Resultado['diferencia_filas']:+d}</font>",
                    Estilos['Normal']
                ))

            if 'diferencia_columnas' in Resultado:
                Story.append(Paragraph(
                    f"<font color='red'>Diferencia columnas: "
                    f"{Resultado['diferencia_columnas']:+d}</font>",
                    Estilos['Normal']
                ))

        # Columnas diferentes.
        if 'columnas_solo_original' in Resultado and Resultado['columnas_solo_original']:
            Story.append(Paragraph(
                f"<b>Columnas solo en original: "
                f"{len(Resultado['columnas_solo_original'])}</b>",
                Estilos['Normal']
            ))

            for Col in Resultado['columnas_solo_original'][:20]:
                Story.append(Paragraph(
                    f"- {Col}",
                    Estilos['Normal']
                ))

        if 'columnas_solo_ordenado' in Resultado and Resultado['columnas_solo_ordenado']:
            Story.append(Paragraph(
                f"<b>Columnas solo en ordenado: "
                f"{len(Resultado['columnas_solo_ordenado'])}</b>",
                Estilos['Normal']
            ))

            for Col in Resultado['columnas_solo_ordenado'][:20]:
                Story.append(Paragraph(
                    f"- {Col}",
                    Estilos['Normal']
                ))

        # Valores diferentes.
        if 'columnas_diferentes' in Resultado and Resultado['columnas_diferentes']:
            Story.append(Paragraph(
                f"<b>Columnas con diferencias: "
                f"{len(Resultado['columnas_diferentes'])}</b>",
                Estilos['Normal']
            ))

            for Col_Diff in Resultado['columnas_diferentes'][:10]:
                if Col_Diff['tipo_diferencia'] == 'dtype':
                    Story.append(Paragraph(
                        f"- {Col_Diff['columna']}: Tipo diferente<br/>"
                        f"  Original: {Col_Diff['dtype_original']}<br/>"
                        f"  Ordenado: {Col_Diff['dtype_ordenado']}",
                        Estilos['Normal']
                    ))
                else:
                    Story.append(Paragraph(
                        f"- {Col_Diff['columna']}: "
                        f"{Col_Diff['num_diferencias']} valores "
                        f"difieren ({Col_Diff['porcentaje']:.2f}%)",
                        Estilos['Normal']
                    ))

                    if 'casos_ejemplo' in Col_Diff and Col_Diff['casos_ejemplo']:
                        Datos_Tabla = [
                            ['ID', 'Fila', 'Original', 'Ordenado']
                        ]

                        for Caso in Col_Diff['casos_ejemplo'][:5]:
                            Datos_Tabla.append([
                                str(Caso['id']),
                                str(Caso['fila']),
                                Caso['valor_original'],
                                Caso['valor_ordenado']
                            ])

                        Tabla = Table(Datos_Tabla)
                        Tabla.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 8),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ]))
                        Story.append(Tabla)
                        Story.append(Spacer(1, 8))

        Story.append(Spacer(1, 20))

    Doc.build(Story)
    print(f"\n✓ Reporte PDF generado: {Archivo_PDF}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def Ejecutar_Control_Identidad_Bases(
    Nombre_Base: str,
    Ruta_Original: Path = RUTA_PROYECTO_ORIGINAL,
    Ruta_Ordenado: Path = RUTA_PROYECTO_ORDENADO
) -> bool:

    """
    Ejecuta control completo de identidad de bases.

    """

    print("\n" + "="*70)
    print(f"CONTROL 15: IDENTIDAD DE BASES - {Nombre_Base}")
    print("="*70)

    # Cargar archivos.
    Archivo_Original = (
        Ruta_Original / ARCHIVOS_COMPARACION[Nombre_Base]['original']
    )
    Archivo_Ordenado = (
        Ruta_Ordenado / ARCHIVOS_COMPARACION[Nombre_Base]['ordenado']
    )

    print(f"\nArchivo original: {Archivo_Original}")
    print(f"Archivo ordenado: {Archivo_Ordenado}")

    if not Archivo_Original.exists():
        print(f"\n✗ Archivo original no encontrado")
        return False

    if not Archivo_Ordenado.exists():
        print(f"\n✗ Archivo ordenado no encontrado")
        return False

    print("\nCargando archivos...")
    Df_Original = pd.read_excel(Archivo_Original)
    Df_Ordenado = pd.read_excel(Archivo_Ordenado)
    print("✓ Archivos cargados")

    Resultados = []

    print("\n1. Verificando dimensiones...")
    R1 = Verificar_Dimensiones(Df_Original, Df_Ordenado, Nombre_Base)
    Resultados.append(R1)
    print(f"   {'✓' if R1['aprobado'] else '✗'} "
          f"{R1['verificacion']}")

    print("\n2. Verificando columnas idénticas...")
    R2 = Verificar_Columnas_Identicas(
        Df_Original, Df_Ordenado, Nombre_Base
    )
    Resultados.append(R2)
    print(f"   {'✓' if R2['aprobado'] else '✗'} "
          f"{R2['verificacion']}")

    print("\n3. Verificando tipos de datos...")
    R3 = Verificar_Tipos_Datos(Df_Original, Df_Ordenado, Nombre_Base)
    Resultados.append(R3)
    print(f"   {'✓' if R3['aprobado'] else '✗'} "
          f"{R3['verificacion']}")

    print("\n4. Verificando valores celda por celda...")
    R4 = Verificar_Valores_Identicos(
        Df_Original, Df_Ordenado, Nombre_Base
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
        print("✓ IDENTIDAD 100% VERIFICADA")
        print("Las bases son completamente idénticas.")
    else:
        print("✗ DIFERENCIAS ENCONTRADAS")
        print("Las bases NO son idénticas.")
    print("="*70)

    return Todas_Aprobadas


if __name__ == "__main__":
    print("Control 15 debe ejecutarse importando la función")
    print("Ejecutar_Control_Identidad_Bases()")
