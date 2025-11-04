# ============================================================
# MODELOS_SEM.PY
# ============================================================
# Modelos de ecuaciones estructurales (SEM) para evaluar
# la relación entre índices ideológicos y cambios de opinión
# y tiempo.
# ============================================================

# ============================================================
# IMPORTACIONES
# ============================================================

import pandas as pd
from semopy import Model
from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).parent.parent / "Utilidades")
)

from Configuracion import (
    COL_INDICE_PROGRESISMO,
    COL_INDICE_CONSERVADURISMO
)


# ============================================================
# FUNCIONES DE MODELADO
# ============================================================

def Ejecutar_Modelo_SEM_Simple(
    Df: pd.DataFrame,
    Variable_Predictora: str,
    Variable_Outcome: str
) -> dict:

    """
    Ejecuta un modelo SEM simple con un predictor y un outcome.

    Parámetros:
    - Df: DataFrame con los datos.
    - Variable_Predictora: Variable independiente.
    - Variable_Outcome: Variable dependiente.

    Retorna:
    - Diccionario con resultados del modelo.

    """

    # Preparar datos (eliminar NaN).
    Df_Limpio = Df[
        [Variable_Predictora, Variable_Outcome]
    ].dropna()

    if len(Df_Limpio) < 30:
        return {
            'Exito': False,
            'Error': 'Datos insuficientes',
            'N': len(Df_Limpio)
        }

    # Definir especificación del modelo.
    Especificacion = f"""
        {Variable_Outcome} ~ {Variable_Predictora}
    """

    try:
        # Crear y ajustar modelo.
        Modelo_SEM = Model(Especificacion)
        Modelo_SEM.fit(Df_Limpio)

        # Extraer resultados.
        Resultados = Modelo_SEM.inspect()

        # Obtener estadísticas del modelo.
        return {
            'Exito': True,
            'N': len(Df_Limpio),
            'Coeficiente': Resultados.loc[
                0,
                'Estimate'
            ] if len(Resultados) > 0 else None,
            'P_Valor': Resultados.loc[
                0,
                'p-value'
            ] if len(Resultados) > 0 else None,
            'R2': Modelo_SEM.inspect(what='r2').iloc[0, 0]
            if hasattr(Modelo_SEM, 'inspect') else None
        }

    except Exception as Error:
        return {
            'Exito': False,
            'Error': str(Error),
            'N': len(Df_Limpio)
        }


# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    print("Módulo de modelos SEM cargado.")
