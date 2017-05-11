import matplotlib.pylab as pl
import numpy as np


def plot_model(data, title=""):
    x = []
    lab = []
    for key, value in sorted(data.iteritems()):
        lab.append(key)
        x.append(value)

    pl.title(title.replace("\n", "; "))
    pl.imshow(x, interpolation='none');
    pl.yticks(np.arange(len(lab)), lab);
    pl.grid()


def plot_plde(data, title=""):
    for col in data:
        pl.plot(data[col], label=col)
    pl.ylim((-0.1, 1.1))
    pl.legend(loc="center left", bbox_to_anchor=(1, 0.5));
    pl.title(title.replace("\n", "; "))


def get_edges(target, act, inh):
    """
    Builds list of edges for networkx.DiGraph.add_weighted_edges_from()
    """
    res = []
    for a in act:
        res.append((a, target, 1))
    for i in inh:
        res.append((i, target, -1))

    return res


def voting_rule(act, inh):
    import itertools
    """
    Returns "voting" boolean logic expression for given list of activators and inhibitors. 
    """
    actLen = len(act)
    inhLen = len(inh)

    rules = []

    for case in itertools.product([0, 1], repeat=actLen + inhLen):
        actLevel = sum(case[0:actLen])
        inhLevel = sum(case[actLen:])
        if actLevel > 0 and actLevel >= inhLevel:
            rules.append(case)

    res = ""

    for rule in rules:
        line = ""

        for idx, val in enumerate(act + inh):
            if line != "":
                line += " and "

            if rule[idx] == 0:
                line += "not " + val
            else:
                line += "" + val

        if res != "":
            res += " or "

        res += line

    return res
