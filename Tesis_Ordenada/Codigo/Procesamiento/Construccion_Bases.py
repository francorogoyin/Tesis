# ============================================================
# CONSTRUCCION_BASES.PY
# ============================================================
# Construcción de bases de datos desde archivos CSV crudos.
# Combina múltiples archivos de resultados en un solo
# DataFrame consolidado.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from pathlib import Path
import sys

# Agregar ruta de Utilidades al path.
sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import (
    RUTA_DATA_CRUDOS,
    RUTA_DATA_PROCESADOS
)
from Funciones_Comunes import Procesar_Columna_Results


# ============================================================
# DICCIONARIO DE MAPEO DE NOMBRES DE COLUMNAS
# ============================================================

MAPEO_NOMBRES_COLUMNAS = {
   'id': 'ID',
   'fase_1.caracterizacion_personal.genero': 'Genero',
   'fase_1.caracterizacion_personal.edad': 'Edad',
   'fase_1.caracterizacion_personal.nacionalidad': 'Nacionalidad',
   'fase_1.caracterizacion_personal.provincia': 'Provincia',
   'fase_1.caracterizacion_personal.e_social': 'Estrato_Social',
   'fase_1.caracterizacion_personal.niv_educativo':
'Nivel_Educativo',
   'fase_1.caracterizacion_personal.f_ingreso': 'Fuente_Ingreso',
   'fase_1.caracterizacion_personal.inmueble_res':
'Inmueble_Residencia',
   'fase_1.caracterizacion_politica.voto_2019': 'Voto_2019',
   'fase_1.caracterizacion_politica.voto_PASO_2023': 'Voto_PASO_2023',
   'fase_1.caracterizacion_politica.candidato_PASO_2023':
'Candidato_PASO_2023',
   'fase_1.caracterizacion_politica.votara_2023': 'Votara_2023',
   'fase_1.caracterizacion_politica.afiliacion_pol':
'Afiliacion_Politica',
   'fase_1.caracterizacion_politica.autopercepcion_0':
'Autopercepcion_Izq_Der',
   'fase_1.caracterizacion_politica.autopercepcion_1':
'Autopercepcion_Con_Pro',
   'fase_1.caracterizacion_politica.autopercepcion_2':
'Autopercepcion_Per_Antiper',
   'fase_1.caracterizacion_politica.cercania_Sergio_MassaSergio Massa': 'Cercania_Massa',
   'fase_1.caracterizacion_politica.cercania_Patricia_BullrichPatricia Bullrich': 'Cercania_Bullrich',
   'fase_1.caracterizacion_politica.cercania_Myriam_BregmanMyriam Bregman': 'Cercania_Bregman',
   'fase_1.caracterizacion_politica.cercania_Javier_MileiJavier Milei': 'Cercania_Milei',
   'fase_1.caracterizacion_politica.cercania_Juan_SchiarettiJuan Schiaretti': 'Cercania_Schiaretti',
   'fase_1.caracterizacion_medios_comunicacion.medios_informacion':
'Medios_Informacion',
   'fase_1.caracterizacion_medios_comunicacion.red_social': 'Red_Social',
   'fase_1.caracterizacion_medios_comunicacion.influencia_redes_0': 'Influencia_Redes',
   'fase_1.caracterizacion_medios_comunicacion.medios_prensa':
'Medios_Prensa',
   'fase_1.caracterizacion_medios_comunicacion.influencia_prensa_0': 'Influencia_Prensa',
   'fase_2.caracterizacion_electoral.ece_item_1': 'ECE_Item_1',
   'fase_2.caracterizacion_electoral.ece_item_2': 'ECE_Item_2',
   'fase_2.caracterizacion_electoral.ece_item_3': 'ECE_Item_3',
   'fase_2.caracterizacion_electoral.ece_item_4': 'ECE_Item_4',
   'fase_2.caracterizacion_electoral.ece_item_5': 'ECE_Item_5',
   'fase_2.caracterizacion_electoral.ece_item_6': 'ECE_Item_6',
   'fase_2.caracterizacion_electoral.ece_item_7': 'ECE_Item_7',
   'fase_2.caracterizacion_candidatos.Sergio Massa.cdc_0':
'CDC_Massa_0',
   'fase_2.caracterizacion_candidatos.Sergio Massa.cdc_1':
'CDC_Massa_1',
   'fase_2.caracterizacion_candidatos.Sergio Massa.time':
'CDC_Massa_Tiempo',
   'fase_2.caracterizacion_candidatos.Patricia Bullrich.cdc_0':
'CDC_Bullrich_0',
   'fase_2.caracterizacion_candidatos.Patricia Bullrich.cdc_1':
'CDC_Bullrich_1',
   'fase_2.caracterizacion_candidatos.Patricia Bullrich.time':
'CDC_Bullrich_Tiempo',
   'fase_2.caracterizacion_candidatos.Juan Schiaretti.cdc_0':
'CDC_Schiaretti_0',
   'fase_2.caracterizacion_candidatos.Juan Schiaretti.cdc_1':
'CDC_Schiaretti_1',
   'fase_2.caracterizacion_candidatos.Juan Schiaretti.time':
'CDC_Schiaretti_Tiempo',
   'fase_2.caracterizacion_candidatos.Javier Milei.cdc_0':
'CDC_Milei_0',
   'fase_2.caracterizacion_candidatos.Javier Milei.cdc_1':
'CDC_Milei_1',
   'fase_2.caracterizacion_candidatos.Javier Milei.time':
'CDC_Milei_Tiempo',
   'fase_2.caracterizacion_candidatos.Myriam Bregman.cdc_0':
'CDC_Bregman_0',
   'fase_2.caracterizacion_candidatos.Myriam Bregman.cdc_1':
'CDC_Bregman_1',
   'fase_2.caracterizacion_candidatos.Myriam Bregman.time':
'CDC_Bregman_Tiempo',
   'fase_3.IP.IP_item_7.IP_respuesta': 'IP_Item_7_Respuesta',
   'fase_3.IP.IP_item_7.time': 'IP_Item_7_Tiempo',
   'fase_3.IP.IP_item_10.IP_respuesta': 'IP_Item_10_Respuesta',
   'fase_3.IP.IP_item_10.time': 'IP_Item_10_Tiempo',
   'fase_3.IP.IP_item_27.IP_respuesta': 'IP_Item_27_Respuesta',
   'fase_3.IP.IP_item_27.time': 'IP_Item_27_Tiempo',
   'fase_3.IP.IP_item_25.IP_respuesta': 'IP_Item_25_Respuesta',
   'fase_3.IP.IP_item_25.time': 'IP_Item_25_Tiempo',
   'fase_3.IP.IP_item_24.IP_respuesta': 'IP_Item_24_Respuesta',
   'fase_3.IP.IP_item_24.time': 'IP_Item_24_Tiempo',
   'fase_3.IP.IP_item_29.IP_respuesta': 'IP_Item_29_Respuesta',
   'fase_3.IP.IP_item_29.time': 'IP_Item_29_Tiempo',
   'fase_3.IP.IP_item_28.IP_respuesta': 'IP_Item_28_Respuesta',
   'fase_3.IP.IP_item_28.time': 'IP_Item_28_Tiempo',
   'fase_3.IP.IP_item_30.IP_respuesta': 'IP_Item_30_Respuesta',
   'fase_3.IP.IP_item_30.time': 'IP_Item_30_Tiempo',
   'fase_3.IP.IP_item_19.IP_respuesta': 'IP_Item_19_Respuesta',
   'fase_3.IP.IP_item_19.time': 'IP_Item_19_Tiempo',
   'fase_3.IP.IP_item_8.IP_respuesta': 'IP_Item_8_Respuesta',
   'fase_3.IP.IP_item_8.time': 'IP_Item_8_Tiempo',
   'fase_3.IP.IP_item_22.IP_respuesta': 'IP_Item_22_Respuesta',
   'fase_3.IP.IP_item_22.time': 'IP_Item_22_Tiempo',
   'fase_3.IP.IP_item_11.IP_respuesta': 'IP_Item_11_Respuesta',
   'fase_3.IP.IP_item_11.time': 'IP_Item_11_Tiempo',
   'fase_3.IP.IP_item_20.IP_respuesta': 'IP_Item_20_Respuesta',
   'fase_3.IP.IP_item_20.time': 'IP_Item_20_Tiempo',
   'fase_3.IP.IP_item_3.IP_respuesta': 'IP_Item_3_Respuesta',
   'fase_3.IP.IP_item_3.time': 'IP_Item_3_Tiempo',
   'fase_3.IP.IP_item_4.IP_respuesta': 'IP_Item_4_Respuesta',
   'fase_3.IP.IP_item_4.time': 'IP_Item_4_Tiempo',
   'fase_3.IP.IP_item_6.IP_respuesta': 'IP_Item_6_Respuesta',
   'fase_3.IP.IP_item_6.time': 'IP_Item_6_Tiempo',
   'fase_3.IP.IP_item_9.IP_respuesta': 'IP_Item_9_Respuesta',
   'fase_3.IP.IP_item_9.time': 'IP_Item_9_Tiempo',
   'fase_3.IP.IP_item_5.IP_respuesta': 'IP_Item_5_Respuesta',
   'fase_3.IP.IP_item_5.time': 'IP_Item_5_Tiempo',
   'fase_3.IP.IP_item_16.IP_respuesta': 'IP_Item_16_Respuesta',
   'fase_3.IP.IP_item_16.time': 'IP_Item_16_Tiempo',
   'fase_3.IP_modificada.IP_item_16_Izq.candidato':
'IP_Item_16_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_16_Izq.IP_respuesta':
'IP_Item_16_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_16_Izq.tiempo':
'IP_Item_16_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_27_Der.candidato':
'IP_Item_27_Der_Candidato',
   'fase_3.IP_modificada.IP_item_27_Der.IP_respuesta':
'IP_Item_27_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_27_Der.tiempo':
'IP_Item_27_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_10_Izq.candidato':
'IP_Item_10_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_10_Izq.IP_respuesta':
'IP_Item_10_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_10_Izq.tiempo':
'IP_Item_10_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_22_Izq.candidato':
'IP_Item_22_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_22_Izq.IP_respuesta':
'IP_Item_22_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_22_Izq.tiempo':
'IP_Item_22_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_24_Izq.candidato':
'IP_Item_24_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_24_Izq.IP_respuesta':
'IP_Item_24_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_24_Izq.tiempo':
'IP_Item_24_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_28_Izq.candidato':
'IP_Item_28_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_28_Izq.IP_respuesta':
'IP_Item_28_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_28_Izq.tiempo':
'IP_Item_28_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_25_Der.candidato':
'IP_Item_25_Der_Candidato',
   'fase_3.IP_modificada.IP_item_25_Der.IP_respuesta':
'IP_Item_25_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_25_Der.tiempo':
'IP_Item_25_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_24_Der.candidato':
'IP_Item_24_Der_Candidato',
   'fase_3.IP_modificada.IP_item_24_Der.IP_respuesta':
'IP_Item_24_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_24_Der.tiempo':
'IP_Item_24_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_27_Izq.candidato':
'IP_Item_27_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_27_Izq.IP_respuesta':
'IP_Item_27_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_27_Izq.tiempo':
'IP_Item_27_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_10_Der.candidato':
'IP_Item_10_Der_Candidato',
   'fase_3.IP_modificada.IP_item_10_Der.IP_respuesta':
'IP_Item_10_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_10_Der.tiempo':
'IP_Item_10_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_11_Izq.candidato':
'IP_Item_11_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_11_Izq.IP_respuesta':
'IP_Item_11_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_11_Izq.tiempo':
'IP_Item_11_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_6_Der.candidato':
'IP_Item_6_Der_Candidato',
   'fase_3.IP_modificada.IP_item_6_Der.IP_respuesta':
'IP_Item_6_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_6_Der.tiempo':
'IP_Item_6_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_11_Der.candidato':
'IP_Item_11_Der_Candidato',
   'fase_3.IP_modificada.IP_item_11_Der.IP_respuesta':
'IP_Item_11_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_11_Der.tiempo':
'IP_Item_11_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_6_Izq.candidato':
'IP_Item_6_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_6_Izq.IP_respuesta':
'IP_Item_6_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_6_Izq.tiempo':
'IP_Item_6_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_3_Izq.candidato':
'IP_Item_3_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_3_Izq.IP_respuesta':
'IP_Item_3_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_3_Izq.tiempo':
'IP_Item_3_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_16_Der.candidato':
'IP_Item_16_Der_Candidato',
   'fase_3.IP_modificada.IP_item_16_Der.IP_respuesta':
'IP_Item_16_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_16_Der.tiempo':
'IP_Item_16_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_3_Der.candidato':
'IP_Item_3_Der_Candidato',
   'fase_3.IP_modificada.IP_item_3_Der.IP_respuesta':
'IP_Item_3_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_3_Der.tiempo':
'IP_Item_3_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_22_Der.candidato':
'IP_Item_22_Der_Candidato',
   'fase_3.IP_modificada.IP_item_22_Der.IP_respuesta':
'IP_Item_22_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_22_Der.tiempo':
'IP_Item_22_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_28_Der.candidato':
'IP_Item_28_Der_Candidato',
   'fase_3.IP_modificada.IP_item_28_Der.IP_respuesta':
'IP_Item_28_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_28_Der.tiempo':
'IP_Item_28_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_25_Izq.candidato':
'IP_Item_25_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_25_Izq.IP_respuesta':
'IP_Item_25_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_25_Izq.tiempo':
'IP_Item_25_Izq_Tiempo',
   'fase_4.sentimiento_fase_final': 'Sentimiento_Fase_Final',
   'fase_4.evento_estresante': 'Evento_Estresante',
   'fase_4.sabia_del_experimento': 'Sabia_Del_Experimento',
   'fase_4.usa_sustancias': 'Usa_Sustancias',
   'fase_4.tabaco': 'Tabaco',
   'fase_4.tomaste_drogas_recreativas': 'Drogas_Recreativas',
   'fase_4.alcohol': 'Alcohol',
   'fase_4.marihuana': 'Marihuana',
   'fase_4.medicamentos': 'Medicamentos',
   'fase_4.cual_medicamento': 'Cual_Medicamento',
   'fase_4.otras_sustancias': 'Otras_Sustancias',
   'fase_4.cual_droga_recreativa': 'Cual_Droga_Recreativa',
   'fase_4.horas_sueño_promedio': 'Horas_Sueno_Promedio',
   'fase_4.sueño_noche_anterior': 'Sueno_Noche_Anterior',
   'fase_3.IP.IP_item_23.IP_respuesta': 'IP_Item_23_Respuesta',
   'fase_3.IP.IP_item_23.time': 'IP_Item_23_Tiempo',
   'fase_3.IP_modificada.IP_item_5_Der.candidato':
'IP_Item_5_Der_Candidato',
   'fase_3.IP_modificada.IP_item_5_Der.IP_respuesta':
'IP_Item_5_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_5_Der.tiempo':
'IP_Item_5_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_29_Der.candidato':
'IP_Item_29_Der_Candidato',
   'fase_3.IP_modificada.IP_item_29_Der.IP_respuesta':
'IP_Item_29_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_29_Der.tiempo':
'IP_Item_29_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_23_Der.candidato':
'IP_Item_23_Der_Candidato',
   'fase_3.IP_modificada.IP_item_23_Der.IP_respuesta':
'IP_Item_23_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_23_Der.tiempo':
'IP_Item_23_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_30_Der.candidato':
'IP_Item_30_Der_Candidato',
   'fase_3.IP_modificada.IP_item_30_Der.IP_respuesta':
'IP_Item_30_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_30_Der.tiempo':
'IP_Item_30_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_23_Izq.candidato':
'IP_Item_23_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_23_Izq.IP_respuesta':
'IP_Item_23_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_23_Izq.tiempo':
'IP_Item_23_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_30_Izq.candidato':
'IP_Item_30_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_30_Izq.IP_respuesta':
'IP_Item_30_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_30_Izq.tiempo':
'IP_Item_30_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_19_Der.candidato':
'IP_Item_19_Der_Candidato',
   'fase_3.IP_modificada.IP_item_19_Der.IP_respuesta':
'IP_Item_19_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_19_Der.tiempo':
'IP_Item_19_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_8_Der.candidato':
'IP_Item_8_Der_Candidato',
   'fase_3.IP_modificada.IP_item_8_Der.IP_respuesta':
'IP_Item_8_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_8_Der.tiempo':
'IP_Item_8_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_29_Izq.candidato':
'IP_Item_29_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_29_Izq.IP_respuesta':
'IP_Item_29_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_29_Izq.tiempo':
'IP_Item_29_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_5_Izq.candidato':
'IP_Item_5_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_5_Izq.IP_respuesta':
'IP_Item_5_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_5_Izq.tiempo':
'IP_Item_5_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_19_Izq.candidato':
'IP_Item_19_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_19_Izq.IP_respuesta':
'IP_Item_19_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_19_Izq.tiempo':
'IP_Item_19_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_8_Izq.candidato':
'IP_Item_8_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_8_Izq.IP_respuesta':
'IP_Item_8_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_8_Izq.tiempo':
'IP_Item_8_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_4_Der.candidato':
'IP_Item_4_Der_Candidato',
   'fase_3.IP_modificada.IP_item_4_Der.IP_respuesta':
'IP_Item_4_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_4_Der.tiempo':
'IP_Item_4_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_4_Izq.candidato':
'IP_Item_4_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_4_Izq.IP_respuesta':
'IP_Item_4_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_4_Izq.tiempo':
'IP_Item_4_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_9_Izq.candidato':
'IP_Item_9_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_9_Izq.IP_respuesta':
'IP_Item_9_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_9_Izq.tiempo':
'IP_Item_9_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_20_Der.candidato':
'IP_Item_20_Der_Candidato',
   'fase_3.IP_modificada.IP_item_20_Der.IP_respuesta':
'IP_Item_20_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_20_Der.tiempo':
'IP_Item_20_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_9_Der.candidato':
'IP_Item_9_Der_Candidato',
   'fase_3.IP_modificada.IP_item_9_Der.IP_respuesta':
'IP_Item_9_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_9_Der.tiempo':
'IP_Item_9_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_20_Izq.candidato':
'IP_Item_20_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_20_Izq.IP_respuesta':
'IP_Item_20_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_20_Izq.tiempo':
'IP_Item_20_Izq_Tiempo',
   'fase_3.IP_modificada.IP_item_7_Der.candidato':
'IP_Item_7_Der_Candidato',
   'fase_3.IP_modificada.IP_item_7_Der.IP_respuesta':
'IP_Item_7_Der_Respuesta',
   'fase_3.IP_modificada.IP_item_7_Der.tiempo':
'IP_Item_7_Der_Tiempo',
   'fase_3.IP_modificada.IP_item_7_Izq.candidato':
'IP_Item_7_Izq_Candidato',
   'fase_3.IP_modificada.IP_item_7_Izq.IP_respuesta':
'IP_Item_7_Izq_Respuesta',
   'fase_3.IP_modificada.IP_item_7_Izq.tiempo':
'IP_Item_7_Izq_Tiempo'
}


# ============================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================

def Cargar_CSV_Crudo(Ruta_Archivo: Path) -> pd.DataFrame:

    """
    Carga un archivo CSV crudo individual.

    Parámetros:
    - Ruta_Archivo: Ruta completa al archivo CSV.

    Retorna:
    - DataFrame con los datos cargados.

    """

    try:
        Df = pd.read_csv(Ruta_Archivo, encoding='utf-8')
        print(f"✓ Cargado: {Ruta_Archivo.name}")
        return Df
    except Exception as Error:
        print(f"✗ Error cargando {Ruta_Archivo.name}: {Error}")
        return pd.DataFrame()


def Combinar_Archivos_Generales() -> pd.DataFrame:

    """
    Combina los 5 archivos de resultados de elecciones
    Generales en un solo DataFrame.

    Retorna:
    - DataFrame consolidado de elecciones Generales.

    """

    print("\n" + "="*60)
    print("COMBINANDO ARCHIVOS DE ELECCIONES GENERALES")
    print("="*60 + "\n")

    Lista_Dataframes = []

    for Numero in range(1, 6):
        Ruta = RUTA_DATA_CRUDOS / f"Generales {Numero}.csv"
        if Ruta.exists():
            Df = Cargar_CSV_Crudo(Ruta)
            if not Df.empty:
                Lista_Dataframes.append(Df)

    if Lista_Dataframes:
        Df_Combinado = pd.concat(
            Lista_Dataframes,
            ignore_index=True
        )
        print(
            f"\n✓ Total de filas combinadas: "
            f"{len(Df_Combinado)}"
        )
        return Df_Combinado
    else:
        print("✗ No se pudieron combinar archivos.")
        return pd.DataFrame()


def Combinar_Archivos_Ballotage() -> pd.DataFrame:

    """
    Combina los 2 archivos de resultados de Ballotage en un
    solo DataFrame.

    Retorna:
    - DataFrame consolidado de Ballotage.

    """

    print("\n" + "="*60)
    print("COMBINANDO ARCHIVOS DE BALLOTAGE")
    print("="*60 + "\n")

    Lista_Dataframes = []

    for Numero in range(1, 3):
        Ruta = RUTA_DATA_CRUDOS / f"Ballotage {Numero}.csv"
        if Ruta.exists():
            Df = Cargar_CSV_Crudo(Ruta)
            if not Df.empty:
                Lista_Dataframes.append(Df)

    if Lista_Dataframes:
        Df_Combinado = pd.concat(
            Lista_Dataframes,
            ignore_index=True
        )
        print(
            f"\n✓ Total de filas combinadas: "
            f"{len(Df_Combinado)}"
        )
        return Df_Combinado
    else:
        print("✗ No se pudieron combinar archivos.")
        return pd.DataFrame()


# ============================================================
# FUNCIONES DE PROCESAMIENTO
# ============================================================

def Procesar_Base_Completa(
    Df_Crudo: pd.DataFrame
) -> pd.DataFrame:

    """
    Procesa la base cruda extrayendo y aplanando la columna
    'results' en formato JSON, y renombra las columnas.

    Parámetros:
    - Df_Crudo: DataFrame crudo con columna 'results'.

    Retorna:
    - DataFrame procesado con datos aplanados y nombres
      de columnas limpios.

    """

    print("\nProcesando columna 'results'...")
    Df_Procesado = Procesar_Columna_Results(Df_Crudo)
    print(f"✓ Filas procesadas: {len(Df_Procesado)}")

    # Aplicar mapeo de nombres de columnas.
    print("\nRenombrando columnas...")
    Mapeo_Filtrado = {
        Viejo: Nuevo for Viejo, Nuevo in
        MAPEO_NOMBRES_COLUMNAS.items()
        if Viejo in Df_Procesado.columns
    }

    Df_Procesado = Df_Procesado.rename(columns=Mapeo_Filtrado)
    print(f"✓ {len(Mapeo_Filtrado)} columnas renombradas")

    return Df_Procesado


# ============================================================
# FUNCIONES DE EXPORTACION
# ============================================================

def Guardar_Base_Procesada(
    Df: pd.DataFrame,
    Nombre_Archivo: str
) -> None:

    """
    Guarda el DataFrame procesado en formato Excel.

    Parámetros:
    - Df: DataFrame a guardar.
    - Nombre_Archivo: Nombre del archivo (sin extensión).

    """

    Ruta_Salida = (
        RUTA_DATA_PROCESADOS / f"{Nombre_Archivo}.xlsx"
    )

    try:
        Df.to_excel(Ruta_Salida, index=False)
        print(f"✓ Base guardada en: {Ruta_Salida}")
    except Exception as Error:
        print(f"✗ Error guardando base: {Error}")


# ============================================================
# EJECUCION PRINCIPAL
# ============================================================

def Ejecutar_Construccion_Bases():

    """
    Ejecuta el pipeline completo de construcción de bases.

    """

    print("\n" + "="*60)
    print("PIPELINE DE CONSTRUCCION DE BASES")
    print("="*60)

    # Combinar archivos Generales.
    Df_Generales_Crudo = Combinar_Archivos_Generales()
    if not Df_Generales_Crudo.empty:
        Df_Generales = Procesar_Base_Completa(
            Df_Generales_Crudo
        )
        Guardar_Base_Procesada(Df_Generales, "Base_Generales")

    # Combinar archivos Ballotage.
    Df_Ballotage_Crudo = Combinar_Archivos_Ballotage()
    if not Df_Ballotage_Crudo.empty:
        Df_Ballotage = Procesar_Base_Completa(
            Df_Ballotage_Crudo
        )
        Guardar_Base_Procesada(Df_Ballotage, "Base_Ballotage")

    print("\n" + "="*60)
    print("CONSTRUCCION DE BASES COMPLETADA")
    print("="*60 + "\n")


if __name__ == "__main__":
    Ejecutar_Construccion_Bases()
