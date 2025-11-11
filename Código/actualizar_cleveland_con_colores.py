import json

# ============================================================
# SCRIPT PARA ACTUALIZAR GRÁFICOS CLEVELAND
# ============================================================
# Modifica los notebooks 62.1 y crea 70.1 con corchetes
# de color según la variable (azul=Congruente, rojo=Incongruente)


def Crear_Celda_Nueva_6_CO():
    """
    Crea el código para la celda nueva-6 del notebook 62.1 (CO).

    """

    codigo = '''def Crear_Cleveland_Con_Comparaciones(
    df,
    titulo,
    comparaciones_sig_cong=None,
    comparaciones_sig_incong=None,
    nombre_archivo=None,
    carpeta_destino='Graficos_Cleveland'
):

    """
    Crea gráfico de Cleveland con corchetes mostrando comparaciones
    significativas entre poblaciones.
    Los corchetes azules indican diferencias en CO_Congruente.
    Los corchetes rojos indican diferencias en CO_Incongruente.

    """

    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    df_sorted = df.sort_values(
        'Diferencia',
        ascending=True
    ).reset_index(drop=True)

    # Crear figura con espacio adicional si hay comparaciones
    tiene_comparaciones = (
        (comparaciones_sig_cong and len(comparaciones_sig_cong) > 0)
        or
        (comparaciones_sig_incong and len(comparaciones_sig_incong) > 0)
    )
    ancho = 16 if tiene_comparaciones else 12
    fig, ax = plt.subplots(figsize=(ancho, 10))

    y_positions = np.arange(len(df_sorted))

    # Dibujar líneas y puntos
    for idx, row in df_sorted.iterrows():
        cong_val = row['CO_Congruente']
        incong_val = row['CO_Incongruente']
        diferencia = row['Diferencia']

        if diferencia > 0.1:
            color_linea = '#2ecc71'
            alpha = 0.7
        elif diferencia < -0.1:
            color_linea = '#e74c3c'
            alpha = 0.7
        else:
            color_linea = '#95a5a6'
            alpha = 0.4

        ax.plot(
            [cong_val, incong_val],
            [idx, idx],
            color=color_linea,
            linewidth=2,
            alpha=alpha,
            zorder=1
        )

    ax.scatter(
        df_sorted['CO_Congruente'],
        y_positions,
        s=150,
        c='#3498db',
        marker='o',
        edgecolors='white',
        linewidths=2,
        label='Congruente',
        zorder=3,
        alpha=0.9
    )

    ax.scatter(
        df_sorted['CO_Incongruente'],
        y_positions,
        s=150,
        c='#e74c3c',
        marker='o',
        edgecolors='white',
        linewidths=2,
        label='Incongruente',
        zorder=3,
        alpha=0.9
    )

    ax.axvline(
        x=0,
        color='black',
        linestyle='--',
        linewidth=0.8,
        alpha=0.3,
        zorder=0
    )

    # Configurar ejes
    ax.set_yticks(y_positions)
    etiquetas_con_sig = [
        f"{row['Etiqueta']} {row['Significancia']}"
        if row['Significancia'] else row['Etiqueta']
        for _, row in df_sorted.iterrows()
    ]
    ax.set_yticklabels(etiquetas_con_sig, fontsize=11)

    ax.set_xlabel(
        'Cambio de Opinión (promedio)',
        fontsize=12,
        fontweight='bold'
    )
    ax.set_ylabel(
        'Categoría Ideológica',
        fontsize=12,
        fontweight='bold'
    )
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)

    ax.grid(True, axis='x', alpha=0.3, linestyle=':', linewidth=0.5)
    ax.set_axisbelow(True)

    # Mapear etiquetas a posiciones Y
    etiqueta_a_pos = {
        row['Etiqueta']: idx
        for idx, row in df_sorted.iterrows()
    }

    xlims = ax.get_xlim()
    rango_x = xlims[1] - xlims[0]
    x_bracket_base = xlims[1] + rango_x * 0.08

    contador_corchetes = 0

    # Dibujar corchetes AZULES para CO_Congruente
    if comparaciones_sig_cong and len(comparaciones_sig_cong) > 0:
        for cat1, cat2, p_val, sig in comparaciones_sig_cong[:5]:
            if cat1 in etiqueta_a_pos and cat2 in etiqueta_a_pos:
                y1 = etiqueta_a_pos[cat1]
                y2 = etiqueta_a_pos[cat2]
                y_min = min(y1, y2)
                y_max = max(y1, y2)

                x_pos = x_bracket_base + contador_corchetes * rango_x * 0.05
                contador_corchetes += 1

                color = '#3498db'  # Azul (mismo color que puntos Congruente)

                ax.plot(
                    [x_pos, x_pos],
                    [y_min, y_max],
                    color=color,
                    linewidth=2.5,
                    clip_on=False,
                    zorder=10
                )

                tick_len = rango_x * 0.015
                ax.plot(
                    [x_pos, x_pos + tick_len],
                    [y_max, y_max],
                    color=color,
                    linewidth=2.5,
                    clip_on=False,
                    zorder=10
                )
                ax.plot(
                    [x_pos, x_pos + tick_len],
                    [y_min, y_min],
                    color=color,
                    linewidth=2.5,
                    clip_on=False,
                    zorder=10
                )

                ax.text(
                    x_pos + tick_len * 1.5,
                    (y_min + y_max) / 2,
                    sig,
                    fontsize=10,
                    va='center',
                    color=color,
                    fontweight='bold',
                    clip_on=False
                )

    # Dibujar corchetes ROJOS para CO_Incongruente
    if comparaciones_sig_incong and len(comparaciones_sig_incong) > 0:
        for cat1, cat2, p_val, sig in comparaciones_sig_incong[:5]:
            if cat1 in etiqueta_a_pos and cat2 in etiqueta_a_pos:
                y1 = etiqueta_a_pos[cat1]
                y2 = etiqueta_a_pos[cat2]
                y_min = min(y1, y2)
                y_max = max(y1, y2)

                x_pos = x_bracket_base + contador_corchetes * rango_x * 0.05
                contador_corchetes += 1

                color = '#e74c3c'  # Rojo (mismo color que puntos Incongruente)

                ax.plot(
                    [x_pos, x_pos],
                    [y_min, y_max],
                    color=color,
                    linewidth=2.5,
                    clip_on=False,
                    zorder=10
                )

                tick_len = rango_x * 0.015
                ax.plot(
                    [x_pos, x_pos + tick_len],
                    [y_max, y_max],
                    color=color,
                    linewidth=2.5,
                    clip_on=False,
                    zorder=10
                )
                ax.plot(
                    [x_pos, x_pos + tick_len],
                    [y_min, y_min],
                    color=color,
                    linewidth=2.5,
                    clip_on=False,
                    zorder=10
                )

                ax.text(
                    x_pos + tick_len * 1.5,
                    (y_min + y_max) / 2,
                    sig,
                    fontsize=10,
                    va='center',
                    color=color,
                    fontweight='bold',
                    clip_on=False
                )

    # Leyenda simplificada (SIN líneas de texto explicativo)
    legend_elements = [
        Line2D(
            [0], [0],
            marker='o',
            color='w',
            markerfacecolor='#3498db',
            markersize=11,
            label='Congruente',
            markeredgecolor='white',
            markeredgewidth=1.5
        ),
        Line2D(
            [0], [0],
            marker='o',
            color='w',
            markerfacecolor='#e74c3c',
            markersize=11,
            label='Incongruente',
            markeredgecolor='white',
            markeredgewidth=1.5
        ),
        Line2D(
            [0], [0],
            color='#2ecc71',
            linewidth=2.5,
            label='Mayor Incong (>0.1)'
        ),
        Line2D(
            [0], [0],
            color='#95a5a6',
            linewidth=2.5,
            label='Similar (±0.1)'
        ),
        Line2D(
            [0], [0],
            color='#e74c3c',
            linewidth=2.5,
            label='Mayor Cong (<-0.1)'
        )
    ]

    ax.legend(
        handles=legend_elements,
        loc='center left',
        bbox_to_anchor=(1.02, 0.5),
        fontsize=9,
        framealpha=0.95,
        edgecolor='gray'
    )

    plt.tight_layout()

    if nombre_archivo:
        ruta_completa = os.path.join(
            carpeta_destino,
            f'{nombre_archivo}.svg'
        )
        plt.savefig(
            ruta_completa,
            format='svg',
            bbox_inches='tight',
            facecolor='white'
        )
        print(f'Grafico guardado: {ruta_completa}')

    plt.show()

    return fig, ax


# Generar graficos
print('='*70)
print('GRAFICOS CLEVELAND CON COMPARACIONES ENTRE POBLACIONES')
print('='*70)

for nombre_ds in ['Generales', 'Ballotage']:
    print(f'\\n{nombre_ds}:')
    print('-'*70)

    # Obtener comparaciones para ambas variables
    _, comp_sig_cong = Resultados_Comparaciones[nombre_ds].get(
        'CO_Congruente',
        (None, [])
    )
    _, comp_sig_incong = Resultados_Comparaciones[nombre_ds].get(
        'CO_Incongruente',
        (None, [])
    )

    if len(comp_sig_cong) > 0:
        print(
            f'  {len(comp_sig_cong)} comparaciones '
            f'significativas detectadas (CO_Congruente)'
        )
        for cat1, cat2, p, sig in comp_sig_cong[:5]:
            print(f'    {sig} {cat1} vs {cat2} (p={p:.4f})')

    if len(comp_sig_incong) > 0:
        print(
            f'  {len(comp_sig_incong)} comparaciones '
            f'significativas detectadas (CO_Incongruente)'
        )
        for cat1, cat2, p, sig in comp_sig_incong[:5]:
            print(f'    {sig} {cat1} vs {cat2} (p={p:.4f})')

    if len(comp_sig_cong) == 0 and len(comp_sig_incong) == 0:
        print(f'  No hay comparaciones significativas entre poblaciones')

    print(f'\\n  Generando grafico...')

    fig, ax = Crear_Cleveland_Con_Comparaciones(
        datos_graficos[nombre_ds],
        titulo=(
            f'CO Congruente vs Incongruente - {nombre_ds}\\n'
            f'(con comparaciones entre poblaciones)'
        ),
        comparaciones_sig_cong=comp_sig_cong,
        comparaciones_sig_incong=comp_sig_incong,
        nombre_archivo=f'Cleveland_CO_ConComparaciones_{nombre_ds}'
    )

print('\\n' + '='*70)
print('GRAFICOS COMPLETADOS')
print('='*70)'''

    return codigo


# Leer notebook 62.1
print('Actualizando notebook 62.1...')
ruta_62_1 = r'C:\Users\Patricio\Documents\Codigo\Python\Investigacion\Tesis\Código\62.1. Cleveland CO - Comparaciones Entre Poblaciones.ipynb'

with open(ruta_62_1, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Encontrar y reemplazar celda nueva-6
for i, cell in enumerate(nb['cells']):
    if cell.get('id') == 'nueva-6':
        # Dividir el código en líneas
        codigo_nuevo = Crear_Celda_Nueva_6_CO()
        nb['cells'][i]['source'] = [
            line + '\n' for line in codigo_nuevo.split('\n')
        ]
        print(f'Celda nueva-6 actualizada en posicion {i}')
        break

# Guardar
with open(ruta_62_1, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('OK - Notebook 62.1 actualizado con corchetes de colores')
