# -*- coding: utf-8 -*-
"""\
Swiatkowski describes a deformation retraction of UConf_n(Γ) which has
dimension min(b(Γ), n) (where b(Γ) is the number of branched vertices of Γ,
i.e. those of valence three or greater). Daniel Lütgehetmann extends this to a
deformation retraction of Conf_n(Γ) in their master's thesis.
"""

import logging

# Logging configuration: by default, produce no output
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def swiatkowski_model(n, G):
    """ Returns the Swiatkowski model of the Conf_n(G) """
    assert G.is_undirected()
    assert all(map(lambda d: d != 2, G.degree()))  # no inessential vertices
