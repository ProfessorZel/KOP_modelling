import random
from abc import ABCMeta, abstractmethod
from itertools import combinations

import numpy as np


class EdgesGenerator:
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
        edge = (vertices[v], vertices[vv])
        # print(len(z), edge, edge[::-1])
        if v == vv:
            # print("петля!")
            # raise SystemExit("loop")
            continue
        if edge in z or edge[::-1] in z:
            # print("повторение!")
            # raise SystemExit("repeat!")
            continue
        # print("новое edge","z=", len(z), edge)
        z.append(edge)
        yield edge  # print(z)


class CircleGraphGenerator(EdgesGenerator):
    def __init__(self, neighbours_count: int):
        self.neighbours_count = neighbours_count

    def generate_edges(self, vertices: list):
        return closest_neighbours(vertices, self.neighbours_count // 2)


def closest_neighbours(vertices: list,
                       k05):  # это все пары неориентированного графа или ориентированного непараллельного
    n = len(vertices)
    for i, ev in enumerate(vertices):
        for j in range(i + 1, i + k05 + 1):  # TODO this works with numbers not with list
            v = vertices[j % n]
            yield ev, v  # создается кортеж из пары x-y: (x,y)


class AdvancedCircleGraphGenerator(EdgesGenerator):
    def __init__(self, neighbours_count: int):
        self.neighbours_count = neighbours_count

    def generate_edges(self, vertices: list):
        return advanced_closest_neighbours(vertices, self.neighbours_count)


def advanced_closest_neighbours(vertices: list, k):
    n = len(vertices)
    if n % 2 == 0:
        for i, ev in enumerate(vertices):
            for j in range(1, k // 2 + 1):
                v = vertices[(i + j) % n]
                yield ev, v
    else:
        for i, ev in enumerate(vertices[:-1]):
            for j in range(1, k // 2 + 1):
                v = vertices[(i + j) % n]
                yield ev, v
        yield vertices[0], vertices[-1]