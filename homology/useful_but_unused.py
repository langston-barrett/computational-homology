# -*- coding: utf-8 -*-
def is_proper_face(cube1, cube2):
    """ Is the first cube a proper face of the second?

    Example 2.8 from Kaczynki, Mischaikow, and Mrozek:

        >>> from homology.cubical_complex import Cube
        >>> Q = Cube([[1,2], [1]])     # [1,2] x [1,1]
        >>> P = Cube([[1,2], [1, 2]])  # [1,2] x [1,2]
        >>> is_proper_face(Q, P)
        True

        >>> is_proper_face(Q, Q)
        False

    Reference: Definition 2.7 from Kaczynki, Mischaikow, and Mrozek
    """
    return cube1.is_face(cube2) and not cube1 == cube2

def all_faces(cube):
    """ Get all the faces of a cube, not just the primary faces

    Runtime:
      O(2^m): A cube of dimension m has 2^m vertices.
      https://en.wikipedia.org/wiki/Hypercube

     * The empty cube has no faces:

        >>> from homology.cubical_complex import Cube
        >>> all_faces(Cube([]))
        set([])

     * A line has two faces, its endpoints:

        >>> all_faces(Cube([[0, 0], [0, 1]]))  # [0, 0] x [0, 1]
        set([[0,0] x [0,0], [0,0] x [1,1]])

     * A square has 8 faces: 4 edges + 4 vertices:

        >>> len(all_faces(Cube([[0, 1], [0, 1]])))  # I^2
        8

     * A cube has 26 faces: 6 sides + 12 edges + 8 vertices:

        >>> len(all_faces(Cube([[0, 1], [0, 1], [0, 1]])))  # I^3
        26
    """
    to_return = set()
    to_return.update(cube.faces())
    for face in cube.faces():
        to_return.update(all_faces(face))
    return to_return

# This test helped debug an error in collapse_all, and revealed the necessity
# of collapsing maximal cubes first.
'''
@hypothesis.given(
    random_complex(
        max_embed=5, max_cubes=15, maximality_check=True))
def test_collapse_single(cubical_complex):
    """ For debugging: keep collapsing, asserting each time that the homology
    doesn't change """
    face_set = set(cubical_complex.maximal_cells())
    face_d = face_dict(face_set)
    free = get_free_face(face_d)
    while free is not None:
        face_d = collapse(face_d, free, logger=logger)
        complex_ = face_dict_to_complex(face_d)

        logger.debug(">>> Comparing homology...")
        logger.debug(">>> Complex 1: {}".format(cubical_complex.maximal_cells()))
        logger.debug(">>> Complex 2: {}".format(complex_.maximal_cells()))
        compare_homology(cubical_complex.homology(), complex_.homology())
        free = get_free_face(face_d)
'''


def orient(G):
    """\
    Give an orientation to (undirected) G such that there is a single free
    vertex with an out degree of 1, and all edges point "outwards" from this
    vertex.

    Example:
     * The graph  *---*------*   might get assigned   *→ →* → → →*
                      |      |                            ↓      ↓
                      |      |                            ↓      ↓
                      *---*  *                            * → *  *
    """
    assert G.is_undirected()
    assert G.is_tree()

    # Find a free vertex
    free = None
    for vertex, degree in enumerate(G.degree_iterator()):
        if degree == 0:
            free = vertex
            break

    # All trees must have at least one free vertex
    assert free is not None

    # Construct a new digraph where all nodes are "downstream" from the free
    # vertex
    new_digraph = dict()
    to_visit = [free]
    while to_visit != []:
        visiting = to_visit.pop()
        new_neighbors = [n for n in visiting.neighbors_iterator()
                         if n not in new_digraph]

        new_digraph[visiting] = new_neighbors
        to_visit.append(new_neighbors)

    to_return = digraph.DiGraph(data=new_digraph, format="dict_of_lists",
                                immutable=True)

    assert to_return.order() == G.order()
    assert to_return.size() == G.size()
    assert len(filter(lambda deg: deg == 1, G.out_degree())) == 1

    return to_return


def _permutation_to_configuration(permutation, G, edge_lookup):
    """ Given a permutation, give back a relabeling of vertices and edges

    Returns: 2-tuple of (vertex relabeling dictionary, edge relabeling dictionary)

    Runtime: O(V+E+n)

    Examples:
        >>> from sage.graphs.graph import Graph
        >>> _permutation_to_configuration((0, 1), Graph([(0, 1)]), {})
        ({0: (0, 0), 1: (1, 1)}, {(0, 1): []})

        >>> _permutation_to_configuration((0, 2), Graph([(0, 1)]), {2: (0, 1)})
        ({0: (0, 0), 1: (1, None)}, {(0, 1): [(1, 2)]})
    """
    vertex_relabeling = {v: (v, None) for v in G.vertices()}
    edge_relabeling = {e: [] for e in G.edges(labels=False)}

    for point, position in enumerate(permutation):
        if position < G.order():  # point is on a vertex
            vertex_relabeling[position] = (position, point)

        else:
            try:
                edge_relabeling[edge_lookup[position]].append((point, position))
            except KeyError:
                logger.error("lookup: {}".format(lookup))
                logger.error("position: {}".format(position))
                logger.error("u, v: {}, {}".format(u, v))
                logger.error("vertices: {}".format(H.vertices()))
                raise

    return (vertex_relabeling, edge_relabeling)


# class HashableGraph(Graph):
#     """ A subclass of Sage's Graph which includes labels in its hash

#      * Sage default behavior:

#         >>> IGraph = lambda *args: Graph(*args, immutable=True)
#         >>> hash(IGraph([(0, 1)])) == hash(IGraph([(0, 1)]))
#         True
#         >>> hash(IGraph([(0, 1, "x")])) == hash(IGraph([(0, 1, "y")]))
#         True

#      * HashableGraph:

#         >>> hash(HashableGraph([(0, 1)])) == hash(HashableGraph([(0, 1)]))
#         True
#         >>> hash(HashableGraph([(0, 1, "x")])) == hash(HashableGraph([(0, 1, "y")]))
#         False
#     """

#     def __hash__(self):
#         try:
#             return hash(frozenset(self.vertices() + self.edges(labels=True)))

#         # If the labels were unhashable (probably lists), make them frozensets
#         except TypeError as e:
#             edges = map(lambda t: (t[0], t[1], frozenset(t[2])),
#                         self.edges(labels=True))
#             return hash(frozenset(self.vertices() + edges))
