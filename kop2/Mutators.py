from abc import ABCMeta, abstractmethod

import networkx as nx
import numpy as np

from kop2.Generators import rand_boolean


class GraphMutator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def mutate_graph(self, graph: nx.Graph):
        raise NotImplemented


class WeaveGraphMutator(GraphMutator):
    def __init__(self, probability: float):
        self.probability = probability

    def mutate_graph(self, graph: nx.Graph):
        return weave(graph, self.probability)


def weave(graph: nx.Graph, probability: float):  # Watts_Strogatz Graphs
    vertices = set(graph)
    for ev, v in graph.edges():
        if rand_boolean(probability):
            available_choices = vertices - {ev} - set(graph[ev])
            random_node = np.random.choice(list(available_choices))
            graph.remove_edge(ev, v)
            graph.add_edge(ev, random_node)
    return graph
