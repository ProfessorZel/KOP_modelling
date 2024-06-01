import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from random import sample
import seaborn as sns

# node colors for drawing networks
colors = sns.color_palette('pastel', 6)
# sns.palplot(colors)
sns.set_palette(colors)


def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]


# -----------------------------------------------------------------------
def all_pairs(vertices):  # это все пары неориентированного графа или ориентированного непараллельного
    for i, x in enumerate(vertices):
        for j, y in enumerate(vertices):
            if i < j:
                yield x, y  # создаетcя кортеж из пары x-y: (x,y)


def full_graph(v):  # L.Euler Graph
    graph = nx.Graph()
    vertices = range(v)
    graph.add_nodes_from(vertices)
    graph.add_edges_from(all_pairs(vertices))  # все кортежи графа(u,v) записываются в G
    return graph


def probability_graph(v, p):  # Erdos-Renyi Graph
    graph = nx.Graph()
    vertices = range(v)
    graph.add_nodes_from(vertices)
    graph.add_edges_from(случай_ребра(vertices, p))
    return graph


def случайный_заданный_граф(v, u):  # Random Erdos-Renyi Graph
    граф = nx.Graph()
    вершины = range(v)
    граф.add_nodes_from(вершины)
    граф.add_edges_from(случай_ребра(вершины, u))
    return граф


def локтевые_соседи(вершины, k05):  # это все пары неориентированного графа или ориентированного непараллельного
    n = len(вершины)
    for i, ev in enumerate(вершины):
        for j in range(i + 1, i + k05 + 1):
            v = вершины[j % n]
            yield ev, v  # создаетcя кортеж из пары x-y: (x,y)


# _______________________________________________________________________________
def круглый_стол(v, k):  # Кольцевой регулярный граф
    граф = nx.Graph()
    вершины = range(v)
    граф.add_nodes_from(вершины)
    граф.add_edges_from(локтевые_соседи(вершины, k // 2))
    return граф


# оптимизировать, чтобы один и тот же узел не появл. в стеке неск. раз (меньше проверок?быстрее?)
def узлы_соседи(граф, узел_начала):
    видимые_узлы = set()  # изначально - пустое множество неупорядоченных уникальных элементов
    stack = [узел_начала]
    while stack:
        узел = stack.pop()
        if узел not in видимые_узлы:
            видимые_узлы.add(узел)
            # соседи = set(граф[узел]) - видимые_узлы
            # stack.extend(соседи)
            stack.extend(граф.neighbors(узел))
    return видимые_узлы


def связный_граф(граф):
    узел_начала = next(iter(граф))
    соседи = узлы_соседи(граф, узел_начала)
    return len(соседи) == len(граф)


def связность_вывод(граф, имя):
    if граф:
        print('Данный граф ', имя, ' является связным')
    else:
        print('Данный граф ', имя, ' является несвязным')


def переплетение(граф, вероятность):  # Watts_Strogatz Graphs
    вершины = set(граф)
    for ev, v in граф.edges():
        if случай(вероятность):
            выбор = вершины - {ev} - set(граф[ev])
            нов_v = np.random.choice(list(выбор))
            граф.remove_edge(ev, v)
            граф.add_edge(ev, нов_v)
    return граф


# _______________________________________________________________________________
def случай(p):
    return np.random.random() < p


def случай_ребра(вершины, двойная):
    if type(двойная) == float:
        for ребро in all_pairs(вершины):
            if случай(двойная):
                yield ребро
    elif type(двойная) == int:
        x = 1 / len(вершины)
        # вершины=[i for i in range(вершины)]
        # print(вершины)
        вершины = sample(вершины, len(вершины))
        # print(вершины)
        z = []
        while двойная > len(z):
            v = int(np.random.random() // x)
            vv = int(np.random.random() // x)
            ребро = (вершины[v], вершины[vv])
            # print(len(z), ребро, ребро[::-1])
            if v == vv:
                # print("петля!")
                # raise SystemExit("loop")
                continue
            if ребро in z or ребро[::-1] in z:
                # print("повторение!")
                # raise SystemExit("repeat!")
                continue
            # print("новое ребро","z=", len(z), ребро)
            z.append(ребро)
            yield ребро  # print(z)


# ____#Ввод и проверка качества данных_____________________________________
while True:
    узлы, ребра, соседи, вероятность = ((параметры) for параметры in input(
        "Введите через пробел\nЧисло вершин графа ( <= 20, чтобы не нагружать вычислительные мощности)\nЧисло ребер графа\nCтепень вершин графа (число ближайших сеседей):\nBероятность \"переплетения\" ребра(связи) - вероятность[0,1]\n:").split())
    if узлы == 'стоп': raise SystemExit("Код(4)Пользователь прервал выполнение программы")
    try:
        узлы = int(узлы)
        ребра = int(ребра)
        соседи = int(соседи)
        вероятность = float(вероятность)
        if ((узлы <= 20 or узлы > 2) or (вероятность < 1 or вероятность > 0)) or (
                (узлы <= 20 or узлы > 2) and (вероятность < 1 or вероятность > 0)):
            print(
                f'Количество узлов(вершин): {узлы} \nCтепень вершин структуры: {соседи} \nВероятность наличия связи(ребра): {вероятность}\nПринято.\n')
            break
        print("\nНарушены границы условий ввода данных!\n")
    except ValueError:
        print("Код(3)Ошибка при вводе числа!")
# 1. Полный(Эйлеров) граф_________________________________________
ПНГ = full_graph(узлы)
print(namestr(ПНГ, globals()), ПНГ)
связность_вывод(связный_граф(ПНГ), namestr(ПНГ, globals()))
# 2.Случайный полный граф_____________________________________________________
CПГ = probability_graph(узлы, np.random.random())
print(namestr(CПГ, globals()), CПГ)
связность_вывод(связный_граф(CПГ), namestr(CПГ, globals()))
# 3.Случайный заданный вероятностный граф_____________________________________________________
CЗГ = случайный_заданный_граф(узлы, ребра)
print(namestr(CЗГ, globals()), CЗГ)
связность_вывод(связный_граф(CЗГ), namestr(CЗГ, globals()))
# raise SystemExit("RRR")"""
# 4 Кольцевой вероятностный граф
ВРГ = probability_graph(узлы, вероятность)
print(namestr(ВРГ, globals()), ВРГ)
связность_вывод(связный_граф(ВРГ), namestr(ВРГ, globals()))
# 5. Кольцевой регулярный граф_________________________________________
КСТ = круглый_стол(узлы, соседи)
print(namestr(КСТ, globals()), КСТ)
связность_вывод(связный_граф(КСТ), namestr(КСТ, globals()))
# 6. Кольцевой вероятностный граф W-S ________________________________________
ВСГ = круглый_стол(узлы, соседи)
ВСГ = переплетение(ВСГ, вероятность)
print(namestr(ВСГ, globals()), ВСГ)
связность_вывод(связный_граф(КСТ), namestr(ВСГ, globals()))

plt.subplot(2, 3, 1)
nx.draw_circular(ПНГ, node_color='C0', node_size=150, with_labels=True)
plt.axis('equal')
plt.suptitle(
    "Кольцевые графы коммуникаций в организации \'Круглый стол (Кольцо)\'\nКоличество сотрудников: n=" + str(узлы))
plt.title("Полный граф")
plt.text(-0.8, 1.2, "(степень вершин=" + str(узлы - 1) + ": [n-1])")

plt.subplot(2, 3, 2)
nx.draw_circular(CПГ, node_color='C2', node_size=150, with_labels=True)
plt.axis('equal')
plt.title("Полный граф (степень вершин, \nи кол-во ребер - случайные величины)")

plt.subplot(2, 3, 3)
nx.draw_circular(CЗГ, node_color='C3', node_size=150, with_labels=True)
plt.axis('equal')
plt.title("Вероятностный  граф (степень вершин, \nрасполож. ребер случайно)")
plt.text(-0.8, 1.2, "(степень вершин  - случайная величина)")

plt.subplot(2, 3, 4)
nx.draw_circular(ВРГ, node_color='C4', node_size=150, with_labels=True)
plt.axis('equal')
plt.title("Вероятностный  граф \n(располож. ребер вероятностно)")
plt.text(-0.8, 1.2, "(вершин =" + str(узлы) + "  ребер=" + str(ребра) + " p=" + str(вероятность) + ")")

plt.subplot(2, 3, 5)
nx.draw_circular(КСТ, node_color='C5', node_size=150, with_labels=True)
plt.axis('equal')
plt.title("Регулярный  граф")
plt.text(-0.8, 1.2, "(степень вершин=" + str(соседи) + ")")

plt.subplot(2, 3, 6)
nx.draw_circular(ВСГ, node_color='C6', node_size=150, with_labels=True)
plt.axis('equal')
plt.title("Регулярный граф с вероятностным переплетением ребер")
plt.text(-0.8, 1.2, "(степ. верш.(кол-во прямых контактов=" + str(соседи) + " , p=" + str(вероятность) + ")")

plt.show()
