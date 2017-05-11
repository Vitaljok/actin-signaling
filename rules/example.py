import networkx as nx
from utils import get_edges, voting_rule

def build_rules():
    """ Example network rules for validation.
    """
    egf = "egf"
    nrg1 = "nrg1"
    erbb1 = "erbb1"
    erbb2 = "erbb2"
    erbb3 = "erbb3"
    erbb11 = "erbb11"
    erbb13 = "erbb13"
    erbb23 = "erbb23"
    grb2 = "grb2"
    gab1 = "gab1"
    pi3k = "pi3k"
    sos = "sos"
    ras = "ras"
    mek = "mek"
    erk = "erk"
    pip3 = "pip3"
    akt = "akt"

    G = nx.DiGraph()
    rules = ""

    G.add_weighted_edges_from(get_edges(erbb11, [egf, erbb1], []))
    rules += "1: erbb11* = egf and erbb1\n"

    G.add_weighted_edges_from(get_edges(erbb13, [egf, erbb1, erbb3, nrg1], [erbb2]))
    rules += "1: erbb13* = (egf and erbb1 and not erbb2 and erbb3) or (erbb1 and not erbb2 and erbb3 and nrg1) \n"

    G.add_weighted_edges_from(get_edges(erbb23, [erbb2, erbb3, nrg1], []))
    rules += "1: erbb23* = erbb2 and erbb3 and nrg1 \n"

    G.add_weighted_edges_from(get_edges(grb2, [erbb11, erbb13, erbb23], []))
    rules += "1: grb2* = erbb11 or erbb13 or erbb23\n"

    G.add_weighted_edges_from(get_edges(gab1, [grb2, pip3], []))
    rules += "1: gab1* = grb2 and pip3 \n"

    G.add_weighted_edges_from(get_edges(pi3k, [erbb13, erbb23, gab1, ras], []))
    rules += "1: pi3k* = erbb13 or erbb23 or gab1 or ras \n"

    G.add_weighted_edges_from(get_edges(sos, [grb2], [erk]))
    rules += "1: sos* = grb2 and not erk\n"

    G.add_weighted_edges_from(get_edges(ras, [sos], []))
    rules += "1: ras* = sos\n"

    G.add_weighted_edges_from(get_edges(mek, [ras], []))
    rules += "1: mek* = ras\n"

    G.add_weighted_edges_from(get_edges(erk, [mek], []))
    rules += "1: erk* = mek\n"

    G.add_weighted_edges_from(get_edges(pip3, [pi3k], []))
    rules += "1: pip3* = pi3k\n"

    G.add_weighted_edges_from(get_edges(akt, [pip3], []))
    rules += "1: akt* = pip3\n"

    return {"rules":rules, "graph":G}