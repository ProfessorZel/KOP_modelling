# КоП_1 "Моделирование малых систем после итуационного анализа объектов и процессов
# в отдельном выделенном бизнес-процессе организации (строительной сферы)."
# Триадная инфографическая модель подпроцесса работы экспедитора-снабженца в бизнес-процессе "Логистика строительной компании"
import json

# Библиотеки для доп.типов данных,доп.функционала, визуализации данных и организации работы с СОД (в данном случае- файловая система компьютера)
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import textwrap

result_folder = Path('./Результат_КоП1')
result_folder.mkdir(parents=True, exist_ok=True)  # 2.работа с файловой структурой средствами ОС.
f = open('./metadata.json', 'r+', encoding='utf-8')
metadata = json.load(f)
# print(metadata)
wight = metadata['metadata']['size']['wight']
height = metadata['metadata']['size']['height']
dpi = metadata['metadata']['dpi']
fileName = metadata['metadata']['file_name']
monads = metadata['monads']
# effects =
triad = nx.DiGraph()  # 7. Работа со специальными типами данных, не явл. системными в Python.
triad.add_nodes_from(monads)
labels = {}
for effect in metadata['effects']:
    color = effect['color'] if "color" in effect else "black"
    triad.add_edge(effect['actor'], effect['object'], color=color)
    labels[(effect['actor'], effect['object'])] = '\n'.join(textwrap.wrap(effect['effect'], width=20))

for i, effect_result in enumerate(metadata['effect_results']):
    key = '\n'.join(textwrap.wrap(effect_result['object'] + " - " + effect_result['result'], width=20))
    triad.add_node(key)
    color = effect_result['color'] if "color" in effect_result else "black"
    triad.add_edge(effect_result['actor'], key,
                   color=color)
    # labels[(effect_result['actor'], key)] = effect_result['result']

for i, load_result in enumerate(metadata['load_results']):
    key = '\n'.join(textwrap.wrap(str(load_result['load']) + " - " + load_result['result'], width=20))
    triad.add_node(key)
    color = load_result['color'] if "color" in load_result else "black"
    triad.add_edge(load_result['actor'], key,
                   color=color)
    # labels[(load_results['actor'], key)] = load_results['result']

# Параметрическая подготовка к визуализации ифгр-модели_________________
plt.figure(figsize=(wight, height), dpi=dpi)  # размер в дюймах
options = {'node_color': "green",  # цвета вершин
           'node_size': 3000,  # размер вершин
           'width': 2,  # толщина линии ребер
           'arrowstyle': '-|>',  # стиль стрелок для орграфа
           # 'arrowsize': 16,  # размер стрелки
           # 'edge_color': "#000000",  # 'k' 'black' цвета ребер
           }

plt.suptitle(metadata['function']).set_fontsize(16)
plt.title(metadata['title']).set_fontsize(14)

# 10  Подграф.
effect = set(triad) - set(monads)
layout = nx.circular_layout(triad.subgraph(effect))
layout[monads[0]] = np.array([0.45, 0.6])
layout[monads[1]] = np.array([-0.45, 0])
layout[monads[2]] = np.array([0.3, -0.6])

# Функциональная подготовка к визуализации ифгр-модели_________________
edges, colors = zip(*nx.get_edge_attributes(triad, 'color').items())
nx.draw(triad, edgelist=edges, edge_color=colors, pos=layout, with_labels=True, # font_weight='bold',
        arrows=True, connectionstyle='arc3, rad= 0.1', **options)
nx.draw_networkx_edge_labels(triad, pos=layout, edge_labels=labels, label_pos=0.35, verticalalignment='center',
    font_size=9, font_color='red',  bbox=dict(facecolor='none', edgecolor='none', alpha=0))
plt.show()
# Работа с СОД:организация I/O процессов______#11 работа с операционной системой
result_file = Path(result_folder, fileName)
# Реализация ифгр-модели (отчуждение из среды разработки в электронный документ_________________
plt.savefig(result_file)
print("Граф успешно сохранен в", result_file, "в формате png")
