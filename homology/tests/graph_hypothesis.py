""" Hypothesis strategies for generating graphs """

from hypothesis import strategies
from networkx import fast_gnp_random_graph
from functools import partial
from sage.graphs.graph import Graph

def random_graph(max_vertices=50, max_edges=100):
    r = lambda seed: Graph(fast_gnp_random_graph(max_vertices, max_edges, seed))
    return strategies.builds(r, strategies.integers())

# def random_graph(draw, max_vertices=50, max_edges=100):
#     draw_nat = lambda m: draw(strategies.integers(min_value=0, max_value=m))
#     n_vertices = draw_nat(max_vertices)
#     n_edges = draw_nat(max_edges)

#     lst = [[] for n in range(n_vertices)]
#     edges_added = 0
#     while edges_added < n_edges:
#         domain = draw_nat(n_vertices - 1)
#         codomain = draw_nat(n_vertices - 1)
#         lst[domain].append(codomain)
#         edges_added += 1

#     return digraph.DiGraph(data=lst, immutable=True).to_undirected()
