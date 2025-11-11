import json

# Leer notebook
ruta = r'C:\Users\Patricio\Documents\Codigo\Python\Investigacion\Tesis\Código\62.1. Cleveland CO - Comparaciones Entre Poblaciones.ipynb'
with open(ruta, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Encontrar celda nueva-6 y modificar solo la leyenda
for i, cell in enumerate(nb['cells']):
    if cell.get('id') == 'nueva-6':
        # Buscar y reemplazar las líneas de la leyenda
        source = cell['source']

        # Encontrar el índice donde está la leyenda
        for j, line in enumerate(source):
            if 'Asteriscos izq: diff Cong vs Incong' in line:
                # Reemplazar estas dos líneas
                source[j] = "               label='* Izq: Cong vs Incong (Wilcoxon)'),\n"
                source[j+1] = "        Line2D([0], [0], marker='', color='w',\n"
                source[j+2] = "               label='* Der: CO_Congruente entre poblaciones (Dunn)')\n"
                print(f'Leyenda actualizada en celda nueva-6')
                break

        break

# Guardar
with open(ruta, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('✓ Notebook 62.1 actualizado con leyenda mejorada')
