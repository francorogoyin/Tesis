import json

# ============================================================
# COPIAR FUNCIÓN DE CT A CO
# ============================================================

# Leer notebook 70.1 para extraer la función que funciona bien
ruta_ct = r'C:\Users\Patricio\Documents\Codigo\Python\Investigacion\Tesis\Código\70.1. Cleveland CT - Comparaciones Entre Poblaciones.ipynb'

with open(ruta_ct, 'r', encoding='utf-8') as f:
    nb_ct = json.load(f)

# Encontrar celda nueva-6 en 70.1
codigo_ct = None
for cell in nb_ct['cells']:
    if cell.get('id') == 'nueva-6':
        codigo_ct = ''.join(cell['source'])
        break

if not codigo_ct:
    print('ERROR: No se encontró celda nueva-6 en 70.1')
    exit(1)

# Reemplazar todas las referencias de CT por CO
codigo_co = codigo_ct.replace('CT_Congruente', 'CO_Congruente')
codigo_co = codigo_co.replace('CT_Incongruente', 'CO_Incongruente')
codigo_co = codigo_co.replace('Cambio de Tiempo (promedio, segundos)', 'Cambio de Opinión (promedio)')
codigo_co = codigo_co.replace('Cleveland_CT_ConComparaciones', 'Cleveland_CO_ConComparaciones')
codigo_co = codigo_co.replace('CT Congruente vs Incongruente', 'CO Congruente vs Incongruente')
codigo_co = codigo_co.replace('diferencias en CT_', 'diferencias en CO_')

# Cambiar umbrales de 0.5s a 0.1 (para CO)
codigo_co = codigo_co.replace('> 0.5:', '> 0.1:')
codigo_co = codigo_co.replace('< -0.5:', '< -0.1:')
codigo_co = codigo_co.replace("'Mayor Incong (>0.5s)'", "'Mayor Incong (>0.1)'")
codigo_co = codigo_co.replace("'Similar (±0.5s)'", "'Similar (±0.1)'")
codigo_co = codigo_co.replace("'Mayor Cong (<-0.5s)'", "'Mayor Cong (<-0.1)'")

print('Función adaptada de CT a CO')

# Leer notebook 62.1
ruta_co = r'C:\Users\Patricio\Documents\Codigo\Python\Investigacion\Tesis\Código\62.1. Cleveland CO - Comparaciones Entre Poblaciones.ipynb'

with open(ruta_co, 'r', encoding='utf-8') as f:
    nb_co = json.load(f)

# Reemplazar celda nueva-6
for i, cell in enumerate(nb_co['cells']):
    if cell.get('id') == 'nueva-6':
        # Dividir en líneas
        nb_co['cells'][i]['source'] = [
            line + '\n' for line in codigo_co.split('\n')
        ]
        print(f'Celda nueva-6 reemplazada en posición {i}')
        break

# Guardar
with open(ruta_co, 'w', encoding='utf-8') as f:
    json.dump(nb_co, f, ensure_ascii=False, indent=1)

print('OK - Notebook 62.1 actualizado con la misma función que 70.1')
