import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from Generators import FullGraphGenerator, ProbabilityGraphGenerator, ProbabilitySetNGraphGenerator, \
    CircleGraphGenerator
from kop2.GraphBuilder import GraphBuilder
from kop2.Mutators import WeaveGraphMutator

# node colors for drawing networks
colors = sns.color_palette('pastel', 6)
# sns.palplot(colors)
sns.set_palette(colors)


def связность_вывод(граф, имя):
    if граф:
        print('Данный граф ', имя, ' является связным')
    else:
        print('Данный граф ', имя, ' является несвязным')


def retrieveArguments():
    while True:
        args = input(
            "Введите через пробел\nЧисло вершин графа ( <= 20, чтобы не нагружать вычислительные мощности)\nЧисло ребер графа\nCтепень вершин графа (число ближайших сеседей):\nBероятность \"переплетения\" edge_count(связи) - probability[0,1]\n:").split()

        if len(args) == 0:
            print("No argument supplied")
            continue

        if args[0] == 'стоп':
            raise SystemExit("Код(4)Пользователь прервал выполнение программы")

        if len(args) != 4:
            print("There must be 4 arguments")
            continue

        if not args[0].isdigit():
            print("Node count must number and positive")
            continue

        if not args[1].isdigit():
            print("Edge count must number and positive")
            continue

        if not args[2].isdigit():
            print("Neighbour count must number and positive")
            continue

        try:
            node_count = int(args[0])
            edge_count = int(args[1])
            neighbour_count = int(args[2])
            probability = float(args[3])

            if ((node_count <= 20 or node_count > 2) or (probability < 1 or probability > 0)) or (
                    (node_count <= 20 or node_count > 2) and (probability < 1 or probability > 0)):
                print(
                    f'Количество узлов(вершин): {node_count} \nCтепень вершин структуры: {neighbour_count} \nВероятность наличия связи(edge_count): {probability}\nПринято.\n')
                return node_count, edge_count, neighbour_count, probability
            print("\nНарушены границы условий ввода данных!\n")
        except ValueError:
            print("Код(3)Ошибка при вводе числа!")


def main():
    node_count, edge_count, neighbour_count, probability = retrieveArguments()

    # 1. Полный(Эйлеров) граф_________________________________________
    fullGraphGenerator = FullGraphGenerator()
    eulerGraph = GraphBuilder(node_count).set_name("ПНГ").set_edges_generator(fullGraphGenerator).generate_graph()
    print(eulerGraph.name, eulerGraph)
    связность_вывод(nx.is_connected(eulerGraph), eulerGraph.name)

    # 2. Случайный полный граф_____________________________________________________
    probabilityGraphGenerator = ProbabilityGraphGenerator(np.random.random())
    randomProbabilityFullGraph = GraphBuilder(node_count).set_name("CПГ").set_edges_generator(
        probabilityGraphGenerator).generate_graph()
    print(randomProbabilityFullGraph.name, randomProbabilityFullGraph)
    связность_вывод(nx.is_connected(randomProbabilityFullGraph), randomProbabilityFullGraph.name)

    # 3. Случайный заданный вероятностный граф_____________________________________________________
    probabilityGraphGenerator = ProbabilitySetNGraphGenerator(edge_count)
    randomFullGraph = GraphBuilder(node_count).set_name("CЗГ").set_edges_generator(
        probabilityGraphGenerator).generate_graph()
    print(randomFullGraph.name, randomFullGraph)
    связность_вывод(nx.is_connected(randomFullGraph), randomFullGraph.name)

    # 4 Кольцевой вероятностный граф
    setProbabilityGraphGenerator = ProbabilityGraphGenerator(probability)
    setProbabilityFullGraph = GraphBuilder(node_count).set_name(
        "ВРГ").set_edges_generator(setProbabilityGraphGenerator).generate_graph()
    print(setProbabilityFullGraph.name, setProbabilityFullGraph)
    связность_вывод(nx.is_connected(setProbabilityFullGraph), setProbabilityFullGraph.name)

    # 5. Кольцевой регулярный граф_________________________________________
    circleGraphGenerator = CircleGraphGenerator(neighbour_count)
    circleRegularGraph = GraphBuilder(node_count).set_name("КСТ").set_edges_generator(
        circleGraphGenerator).generate_graph()
    print(circleRegularGraph.name, circleRegularGraph)
    связность_вывод(nx.is_connected(circleRegularGraph), circleRegularGraph.name)

    # 6. Кольцевой вероятностный граф W-S ________________________________________
    circleGraphGenerator = CircleGraphGenerator(neighbour_count)
    weaveGraphMutator = WeaveGraphMutator(probability)
    circleWeaveGraph = GraphBuilder(node_count).set_name(
        "ВСГ").set_edges_generator(circleGraphGenerator).set_graph_mutator(weaveGraphMutator).generate_graph()
    print(circleWeaveGraph.name, circleWeaveGraph)
    связность_вывод(nx.is_connected(circleWeaveGraph), circleWeaveGraph.name)

    plt.subplot(2, 3, 1)
    nx.draw_circular(eulerGraph, node_color='C0', node_size=150, with_labels=True)
    plt.axis('equal')
    plt.suptitle(
        "Кольцевые графы коммуникаций в организации \'Круглый стол (Кольцо)\'\nКоличество сотрудников: n=" + str(
            node_count))
    plt.title("Полный граф")
    plt.text(-0.8, 1.2, "(степень вершин=" + str(node_count - 1) + ": [n-1])")

    plt.subplot(2, 3, 2)
    nx.draw_circular(randomProbabilityFullGraph, node_color='C2', node_size=150, with_labels=True)
    plt.axis('equal')
    plt.title("Полный граф (степень вершин, \nи кол-во ребер - случайные величины)")

    plt.subplot(2, 3, 3)
    nx.draw_circular(randomFullGraph, node_color='C3', node_size=150, with_labels=True)
    plt.axis('equal')
    plt.title("Вероятностный  граф (степень вершин, \nрасполож. ребер случайно)")
    plt.text(-0.8, 1.2, "(степень вершин  - случайная величина)")

    plt.subplot(2, 3, 4)
    nx.draw_circular(setProbabilityFullGraph, node_color='C4', node_size=150, with_labels=True)
    plt.axis('equal')
    plt.title("Вероятностный  граф \n(располож. ребер вероятностно)")
    plt.text(-0.8, 1.2, "(вершин =" + str(node_count) + "  ребер=" + str(edge_count) + " p=" + str(probability) + ")")

    plt.subplot(2, 3, 5)
    nx.draw_circular(circleRegularGraph, node_color='C5', node_size=150, with_labels=True)
    plt.axis('equal')
    plt.title("Регулярный  граф")
    plt.text(-0.8, 1.2, "(степень вершин=" + str(neighbour_count) + ")")

    plt.subplot(2, 3, 6)
    nx.draw_circular(circleWeaveGraph, node_color='C6', node_size=150, with_labels=True)
    plt.axis('equal')
    plt.title("Регулярный граф с вероятностным переплетением ребер")
    plt.text(-0.8, 1.2,
             "(степ. верш.(кол-во прямых контактов=" + str(neighbour_count) + " , p=" + str(probability) + ")")

    plt.show()


if __name__ == "__main__":
    main()
