import networkx as nx

from kop2.Generators import EdgesGenerator
from kop2.Mutators import GraphMutator


class GraphBuilder:
    def __init__(self, vertices_count):
        self.vertices_count = vertices_count
        self.generator = None
        self.mutator = None
        self.name = None

    def set_name(self, name: str):
        self.name = name
        return self

    def set_edges_generator(self, generator: EdgesGenerator):
        self.generator = generator
        return self

    def set_graph_mutator(self, mutator: GraphMutator):
        self.mutator = mutator
        return self

    def generate_graph(self):
        graph = nx.Graph()
        if self.name is not None:
            graph.name = self.name
        graph.add_nodes_from(range(self.vertices_count))
        graph.add_edges_from(self.generator.generate_edges(list(graph.nodes)))
        if self.mutator is not None:
            graph = self.mutator.mutate_graph(graph)
        return graph
