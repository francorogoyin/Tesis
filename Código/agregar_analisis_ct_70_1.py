import json

# ============================================================
# SCRIPT PARA AGREGAR ANÁLISIS DE COMPARACIONES A 70.1
# ============================================================

ruta = r'C:\Users\Patricio\Documents\Codigo\Python\Investigacion\Tesis\Código\70.1. Cleveland CT - Comparaciones Entre Poblaciones.ipynb'

with open(ruta, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Celdas nuevas a agregar (adaptadas para CT)
celdas_nuevas = [
    # Nueva-1: Markdown explicativo
    {
        'cell_type': 'markdown',
        'id': 'nueva-1',
        'metadata': {},
        'source': [
            '## 4.2. Comparaciones Entre Poblaciones (Test Post-Hoc)\n',
            '\n',
            '**NUEVO**: Análisis de diferencias significativas **entre las 6 categorías ideológicas** usando el test de Dunn con corrección de Bonferroni.\n',
            '\n',
            'Este análisis responde: ¿Existen diferencias significativas entre Left Wing y Progressivism? ¿Entre Moderate Right A y Moderate Right B? Etc.'
        ]
    },
    # Nueva-2: Código de análisis
    {
        'cell_type': 'code',
        'execution_count': None,
        'id': 'nueva-2',
        'metadata': {},
        'outputs': [],
        'source': [
            '# Instalar si es necesario: pip install scikit-posthocs\n',
            'import scikit_posthocs as sp\n',
            'from scipy.stats import kruskal\n',
            '\n',
            'def Analizar_Diferencias_Entre_Poblaciones(df, variable, nombre_dataset):\n',
            '\n',
            '    """\n',
            '    Realiza test de Kruskal-Wallis seguido de test post-hoc de Dunn\n',
            '    para comparar diferencias entre categorías ideológicas.\n',
            '\n',
            '    """\n',
            '\n',
            '    print(f\'\\n{"="*70}\')\n',
            '    print(f\'COMPARACIONES ENTRE POBLACIONES: {variable} - {nombre_dataset}\')\n',
            '    print(f\'{"="*70}\')\n',
            '\n',
            '    # Preparar datos por categoría\n',
            '    Grupos = []\n',
            '    Categorias_Con_Datos = []\n',
            '\n',
            '    for cat in Categorias:\n',
            '        datos_cat = df[df[\'Categoria_PASO_2023\'] == cat][variable].dropna()\n',
            '        if len(datos_cat) > 0:\n',
            '            Grupos.append(datos_cat)\n',
            '            Categorias_Con_Datos.append(cat)\n',
            '\n',
            '    # Test de Kruskal-Wallis\n',
            '    if len(Grupos) < 2:\n',
            '        print(\'⚠️  No hay suficientes grupos para comparar\')\n',
            '        return None, []\n',
            '\n',
            '    H_stat, p_kruskal = kruskal(*Grupos)\n',
            '\n',
            '    print(f\'\\nTest de Kruskal-Wallis:\')\n',
            '    print(f\'  Estadístico H: {H_stat:.4f}\')\n',
            '    print(f\'  p-valor: {p_kruskal:.6f}\')\n',
            '\n',
            '    if p_kruskal >= 0.05:\n',
            '        print(f\'  ❌ NO SIGNIFICATIVO (p ≥ 0.05)\')\n',
            '        print(f\'     No hay diferencias significativas entre poblaciones\')\n',
            '        return None, []\n',
            '\n',
            '    print(f\'  ✅ SIGNIFICATIVO (p < 0.05)\')\n',
            '    print(f\'     Existen diferencias significativas entre poblaciones\')\n',
            '\n',
            '    # Test post-hoc de Dunn con corrección de Bonferroni\n',
            '    print(f\'\\nTest Post-Hoc de Dunn (corrección de Bonferroni):\')\n',
            '\n',
            '    # Preparar DataFrame para el test\n',
            '    df_test = df[df[\'Categoria_PASO_2023\'].isin(Categorias_Con_Datos)].copy()\n',
            '    df_test = df_test[[\'Categoria_PASO_2023\', variable]].dropna()\n',
            '\n',
            '    # Ejecutar test de Dunn\n',
            '    Matriz_Pvalores = sp.posthoc_dunn(\n',
            '        df_test,\n',
            '        val_col=variable,\n',
            '        group_col=\'Categoria_PASO_2023\',\n',
            '        p_adjust=\'bonferroni\'\n',
            '    )\n',
            '\n',
            '    # Renombrar índices y columnas con etiquetas legibles\n',
            '    Mapeo_Etiquetas = {\n',
            '        cat: Etiquetas_Categorias[cat]\n',
            '        for cat in Categorias_Con_Datos\n',
            '    }\n',
            '    Matriz_Pvalores.index = Matriz_Pvalores.index.map(Mapeo_Etiquetas)\n',
            '    Matriz_Pvalores.columns = Matriz_Pvalores.columns.map(Mapeo_Etiquetas)\n',
            '\n',
            '    # Mostrar comparaciones significativas\n',
            '    print(f\'\\nComparaciones significativas (p < 0.05):\')\n',
            '\n',
            '    Comparaciones_Sig = []\n',
            '    for i in range(len(Matriz_Pvalores)):\n',
            '        for j in range(i+1, len(Matriz_Pvalores)):\n',
            '            p_val = Matriz_Pvalores.iloc[i, j]\n',
            '            if p_val < 0.05:\n',
            '                cat1 = Matriz_Pvalores.index[i]\n',
            '                cat2 = Matriz_Pvalores.index[j]\n',
            '\n',
            '                # Determinar asteriscos\n',
            '                if p_val < 0.001:\n',
            '                    sig = \'***\'\n',
            '                elif p_val < 0.01:\n',
            '                    sig = \'**\'\n',
            '                else:\n',
            '                    sig = \'*\'\n',
            '\n',
            '                Comparaciones_Sig.append((cat1, cat2, p_val, sig))\n',
            '                print(\n',
            '                    f\'  {sig:3s} {cat1:25s} vs {cat2:25s} | \'\n',
            '                    f\'p={p_val:.4f}\'\n',
            '                )\n',
            '\n',
            '    if len(Comparaciones_Sig) == 0:\n',
            '        print(f\'  ⚪ No hay comparaciones significativas después de corrección\')\n',
            '\n',
            '    return Matriz_Pvalores, Comparaciones_Sig\n',
            '\n',
            '\n',
            '# Análisis para ambos datasets y ambas variables\n',
            'Resultados_Comparaciones = {}\n',
            '\n',
            'for nombre_ds in [\'Generales\', \'Ballotage\']:\n',
            '    Resultados_Comparaciones[nombre_ds] = {}\n',
            '\n',
            '    for variable in [\'CT_Congruente\', \'CT_Incongruente\']:\n',
            '        matriz, comp = Analizar_Diferencias_Entre_Poblaciones(\n',
            '            dfs[nombre_ds],\n',
            '            variable,\n',
            '            nombre_ds\n',
            '        )\n',
            '        Resultados_Comparaciones[nombre_ds][variable] = (matriz, comp)\n',
            '\n',
            'print(f\'\\n{"="*70}\')\n',
            'print(f\'ANÁLISIS DE COMPARACIONES COMPLETADO\')\n',
            'print(f\'{"="*70}\')'
        ]
    },
    # Nueva-3: Markdown matrices
    {
        'cell_type': 'markdown',
        'id': 'nueva-3',
        'metadata': {},
        'source': [
            '## 4.3. Matrices de Significancia\n',
            '\n',
            'Visualización en forma de heatmap de los p-valores de todas las comparaciones por pares.'
        ]
    },
    # Nueva-4: Código matrices
    {
        'cell_type': 'code',
        'execution_count': None,
        'id': 'nueva-4',
        'metadata': {},
        'outputs': [],
        'source': [
            'def Crear_Matriz_Significancia(matriz_pvalores, titulo, nombre_archivo=None):\n',
            '\n',
            '    """\n',
            '    Crea un heatmap de la matriz de p-valores de comparaciones por pares.\n',
            '\n',
            '    """\n',
            '\n',
            '    if matriz_pvalores is None:\n',
            '        print(f\'⚠️  No hay datos de comparaciones para {titulo}\')\n',
            '        return None\n',
            '\n',
            '    mask = np.triu(np.ones_like(matriz_pvalores, dtype=bool))\n',
            '\n',
            '    fig, ax = plt.subplots(figsize=(10, 8))\n',
            '\n',
            '    sns.heatmap(\n',
            '        matriz_pvalores,\n',
            '        mask=mask,\n',
            '        annot=True,\n',
            '        fmt=\'.3f\',\n',
            '        cmap=\'RdYlGn_r\',\n',
            '        vmin=0,\n',
            '        vmax=0.1,\n',
            '        cbar_kws={\'label\': \'p-valor\'},\n',
            '        square=True,\n',
            '        linewidths=0.5,\n',
            '        ax=ax\n',
            '    )\n',
            '\n',
            '    ax.set_title(titulo, fontsize=14, fontweight=\'bold\', pad=20)\n',
            '    plt.xticks(rotation=45, ha=\'right\')\n',
            '    plt.yticks(rotation=0)\n',
            '\n',
            '    plt.tight_layout()\n',
            '\n',
            '    if nombre_archivo:\n',
            '        ruta = os.path.join(\'Graficos_Cleveland\', f\'{nombre_archivo}.svg\')\n',
            '        plt.savefig(\n',
            '            ruta,\n',
            '            format=\'svg\',\n',
            '            bbox_inches=\'tight\',\n',
            '            facecolor=\'white\'\n',
            '        )\n',
            '        print(f\'Matriz guardada: {ruta}\')\n',
            '\n',
            '    plt.show()\n',
            '\n',
            '    return fig, ax\n',
            '\n',
            '\n',
            '# Generar matrices para cada dataset y variable\n',
            'print(f\'\\n{"="*70}\')\n',
            'print(f\'MATRICES DE SIGNIFICANCIA (p-valores de comparaciones por pares)\')\n',
            'print(f\'{"="*70}\\n\')\n',
            '\n',
            'for nombre_ds in [\'Generales\', \'Ballotage\']:\n',
            '    for variable in [\'CT_Congruente\', \'CT_Incongruente\']:\n',
            '        matriz, _ = Resultados_Comparaciones[nombre_ds][variable]\n',
            '\n',
            '        if matriz is not None:\n',
            '            titulo = f\'Matriz de p-valores: {variable} - {nombre_ds}\'\n',
            '            nombre_archivo = f\'Matriz_{variable}_{nombre_ds}\'.replace(\' \', \'_\')\n',
            '\n',
            '            Crear_Matriz_Significancia(matriz, titulo, nombre_archivo)\n',
            '\n',
            'print(f\'\\n{"="*70}\')\n',
            'print(f\'Verde = p-valor bajo (significativo)\')\n',
            'print(f\'Rojo = p-valor alto (no significativo)\')\n',
            'print(f\'{"="*70}\')'
        ]
    },
    # Nueva-5: Markdown gráficos mejorados
    {
        'cell_type': 'markdown',
        'id': 'nueva-5',
        'metadata': {},
        'source': [
            '## 4.4. Gráficos Cleveland con Comparaciones Entre Poblaciones\n',
            '\n',
            'Regeneramos los gráficos Cleveland incluyendo **corchetes en el margen derecho** que muestran qué poblaciones tienen diferencias significativas entre sí.\n',
            '\n',
            '- **Corchetes azules**: Diferencias significativas en CT_Congruente\n',
            '- **Corchetes rojos**: Diferencias significativas en CT_Incongruente'
        ]
    },
    # Nueva-6: Código gráficos mejorados
    {
        'cell_type': 'code',
        'execution_count': None,
        'id': 'nueva-6',
        'metadata': {},
        'outputs': [],
        'source': []  # Se llenará con el código
    }
]

# Código para la celda nueva-6 (CT)
codigo_nueva_6 = '''def Crear_Cleveland_Con_Comparaciones(
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
    Los corchetes azules indican diferencias en CT_Congruente.
    Los corchetes rojos indican diferencias en CT_Incongruente.

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
        cong_val = row['CT_Congruente']
        incong_val = row['CT_Incongruente']
        diferencia = row['Diferencia']

        if diferencia > 0.5:
            color_linea = '#2ecc71'
            alpha = 0.7
        elif diferencia < -0.5:
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
        df_sorted['CT_Congruente'],
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
        df_sorted['CT_Incongruente'],
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
        'Cambio de Tiempo (promedio, segundos)',
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

    # Dibujar corchetes AZULES para CT_Congruente
    if comparaciones_sig_cong and len(comparaciones_sig_cong) > 0:
        for cat1, cat2, p_val, sig in comparaciones_sig_cong[:5]:
            if cat1 in etiqueta_a_pos and cat2 in etiqueta_a_pos:
                y1 = etiqueta_a_pos[cat1]
                y2 = etiqueta_a_pos[cat2]
                y_min = min(y1, y2)
                y_max = max(y1, y2)

                x_pos = x_bracket_base + contador_corchetes * rango_x * 0.05
                contador_corchetes += 1

                color = '#3498db'

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

    # Dibujar corchetes ROJOS para CT_Incongruente
    if comparaciones_sig_incong and len(comparaciones_sig_incong) > 0:
        for cat1, cat2, p_val, sig in comparaciones_sig_incong[:5]:
            if cat1 in etiqueta_a_pos and cat2 in etiqueta_a_pos:
                y1 = etiqueta_a_pos[cat1]
                y2 = etiqueta_a_pos[cat2]
                y_min = min(y1, y2)
                y_max = max(y1, y2)

                x_pos = x_bracket_base + contador_corchetes * rango_x * 0.05
                contador_corchetes += 1

                color = '#e74c3c'

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

    # Leyenda simplificada
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
            label='Mayor Incong (>0.5s)'
        ),
        Line2D(
            [0], [0],
            color='#95a5a6',
            linewidth=2.5,
            label='Similar (±0.5s)'
        ),
        Line2D(
            [0], [0],
            color='#e74c3c',
            linewidth=2.5,
            label='Mayor Cong (<-0.5s)'
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
        'CT_Congruente',
        (None, [])
    )
    _, comp_sig_incong = Resultados_Comparaciones[nombre_ds].get(
        'CT_Incongruente',
        (None, [])
    )

    if len(comp_sig_cong) > 0:
        print(
            f'  {len(comp_sig_cong)} comparaciones '
            f'significativas detectadas (CT_Congruente)'
        )
        for cat1, cat2, p, sig in comp_sig_cong[:5]:
            print(f'    {sig} {cat1} vs {cat2} (p={p:.4f})')

    if len(comp_sig_incong) > 0:
        print(
            f'  {len(comp_sig_incong)} comparaciones '
            f'significativas detectadas (CT_Incongruente)'
        )
        for cat1, cat2, p, sig in comp_sig_incong[:5]:
            print(f'    {sig} {cat1} vs {cat2} (p={p:.4f})')

    if len(comp_sig_cong) == 0 and len(comp_sig_incong) == 0:
        print(f'  No hay comparaciones significativas entre poblaciones')

    print(f'\\n  Generando grafico...')

    fig, ax = Crear_Cleveland_Con_Comparaciones(
        datos_graficos[nombre_ds],
        titulo=(
            f'CT Congruente vs Incongruente - {nombre_ds}\\n'
            f'(con comparaciones entre poblaciones)'
        ),
        comparaciones_sig_cong=comp_sig_cong,
        comparaciones_sig_incong=comp_sig_incong,
        nombre_archivo=f'Cleveland_CT_ConComparaciones_{nombre_ds}'
    )

print('\\n' + '='*70)
print('GRAFICOS COMPLETADOS')
print('='*70)'''

# Llenar código en celda nueva-6
celdas_nuevas[5]['source'] = [
    line + '\n' for line in codigo_nueva_6.split('\n')
]

# Insertar las celdas nuevas después de la celda 13 (después del análisis de significancia)
# Buscar la celda 13 que contiene "ANÁLISIS DE SIGNIFICANCIA ESTADÍSTICA"
insert_position = None
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        source_text = ''.join(cell.get('source', []))
        if 'ANÁLISIS DE SIGNIFICANCIA ESTADÍSTICA' in source_text and 'Wilcoxon' in source_text:
            insert_position = i + 1
            break

if insert_position:
    # Insertar las nuevas celdas
    for j, nueva_celda in enumerate(celdas_nuevas):
        nb['cells'].insert(insert_position + j, nueva_celda)
    print(f'Se insertaron {len(celdas_nuevas)} celdas nuevas en posición {insert_position}')
else:
    print('No se encontró la posición para insertar las celdas')

# Guardar
with open(ruta, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('OK - Notebook 70.1 creado con análisis de comparaciones entre poblaciones')
