import random
from abc import ABCMeta, abstractmethod, abstractproperty
from itertools import combinations
import numpy as np


class EdgesGenerator():
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_edges(self, vertices: list):
        raise NotImplemented


class FullGraphGenerator(EdgesGenerator):
    def generate_edges(self, vertices: list):
        return all_pairs(vertices)


def all_pairs(vertices):
    return combinations(vertices, 2)


class ProbabilityGraphGenerator(EdgesGenerator):
    def __init__(self, probability: float):
        self.probability = probability

    def generate_edges(self, vertices: list):
        return random_edges(vertices, self.probability)


def random_edges(vertices: list, probability: float):
    for edge in all_pairs(vertices):
        if rand_boolean(probability):
            yield edge


def rand_boolean(p: float) -> bool:
    return np.random.random() < p


class ProbabilitySetNGraphGenerator(EdgesGenerator):
    def __init__(self, edges_count: int):
        self.edges_count = edges_count

    def generate_edges(self, vertices: list):
        return random_n_edges(vertices, self.edges_count)


def random_n_edges(vertices: list, number_of_edges: int):
    x = 1 / len(vertices)
    # вершины=[i for i in range(вершины)]
    # print(вершины)
    vertices = random.sample(vertices, len(vertices))
    # print(вершины)
    z = []
    while number_of_edges > len(z):
        v = int(np.random.random() // x)
        vv = int(np.random.random() // x)
        ребро = (vertices[v], vertices[vv])
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


class CircleGraphGenerator(EdgesGenerator):
    def __init__(self, neighbours_count: int):
        self.neighbours_count = neighbours_count

    def generate_edges(self, vertices: list):
        return локтевые_соседи(vertices, self.neighbours_count // 2)


def локтевые_соседи(вершины, k05):  # это все пары неориентированного графа или ориентированного непараллельного
    n = len(вершины)
    for i, ev in enumerate(вершины):
        for j in range(i + 1, i + k05 + 1):
            v = вершины[j % n]
            yield ev, v  # создаетcя кортеж из пары x-y: (x,y)
