from abc import ABCMeta, abstractmethod
import numpy as np

from kop2.Generators import rand_boolean


class GraphMutator():
    __metaclass__ = ABCMeta

    @abstractmethod
    def mutate_graph(self, graph: range):
        raise NotImplemented


class WeaveGraphMutator(GraphMutator):
    def __init__(self, probability: float):
        self.probability = probability

    def mutate_graph(self, graph: range):
        return переплетение(graph, self.probability)


def переплетение(граф, вероятность):  # Watts_Strogatz Graphs
    вершины = set(граф)
    for ev, v in граф.edges():
        if rand_boolean(вероятность):
            выбор = вершины - {ev} - set(граф[ev])
            нов_v = np.random.choice(list(выбор))
            граф.remove_edge(ev, v)
            граф.add_edge(ev, нов_v)
    return граф
