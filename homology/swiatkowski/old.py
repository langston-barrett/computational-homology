
def _zero_cells_with_duplicates(n, G, logger=None):
    """ A generator of configurations of n points on G

    The implementation causes duplicates, see ``zero_cells`` for a version
    without duplicates, and for more documentation.

    Implementation: the graph is subdivided Abrams-style, so that each edge has
    n additional labels on it. We loop through the permutations of n points on
    these n+(n*E) labels.

     * If the label represents a vertex, that vertex is renamed as a tuple
       (original_label, point_on_this_vertex).
     * If the label represents a vertex, we append a pair (point, label) to the
       list of points on that edge. We record the label so that they can be
       sorted on that edge later.
    """
    logger.debug("n: {}".format(n))

    G = subdivide(n, G)
    logger.debug("Graph: {}".format(G))

    # Look up which edge a label lies on. Construction is O(n*E).
    lookup = _label_lookup_table(G)
    logger.debug("Lookup: {}".format(lookup))

    # A list of every available label on this graph. Construction is O(n*E).
    labels = itertools.chain((n for n in xrange(G.order())), *G.edge_labels())
    labels = list(labels)
    logger.debug("Labels: {}".format(labels))

    # We'll yield a copy of G with the appropriate labels
    H_ = sage.all.copy(G)

    perms = itertools.permutations(labels, n)
    perms = list(perms)
    logger.debug("Permutations: {}".format(list(perms)))
    # Loop through all n-tuples of point positions
    for perm in perms:
        H = sage.all.copy(H_)

        # Zero out labels
        H, _ = edge_label_fold(lambda label, acc: ([], None), None, H)

        # For each point, record its location on the graph
        relabeling = {n: (n, None) for n in xrange(H.order())}
        logger.debug("Relabeling: {}".format(relabeling))
        for point, location in enumerate(perm):
            # If it's on a vertex, relabel the vertex
            if location < H.order():
                relabeling[location] = (location, point)
            # Otherwise, look up the appropriate edge and append it
            else:
                u, v = lookup[location]
                try:
                    current_label = H.edge_label(u, v)
                    # TODO: replace with a binary heap
                    H.set_edge_label(u, v, current_label + [(point, location)])
                except LookupError:
                    logger.error("lookup: {}".format(lookup))
                    logger.error("location: {}".format(location))
                    logger.error("u, v: {}, {}".format(u, v))
                    logger.error("vertices: {}".format(H.vertices()))
                    raise

        logger.debug("Sorting edges: {}".format(H.edges(labels=True)))
        fst = lambda tup: tup[0]
        sort_then_fst = lambda label: map(fst, sorted(label, key=lambda tup: tup[1]))
        H = edge_label_map(sort_then_fst, H)
        logger.debug("Edges: {}".format(H.edges(labels=True)))

        logger.debug("Relabeling: {}".format(relabeling))
        H.relabel(relabeling)
        yield H.copy(immutable=True)
