import itertools
import networkx as nx
from enzymes import *


class Rules:
    """ Original Actin network rules.
    """

    def __init__(self):
        G = nx.DiGraph()
        rules = ""

        G.add_weighted_edges_from(
            self.get_edges(WASP, [Rac1, Cdc42, PIP2, Cortactin, IRSp53], [Thymosin]))
        rules += "1: WASP* = not Thymosin and (Rac1 or Cdc42 or PIP2 or Cortactin or IRSp53) \n"

        G.add_weighted_edges_from(self.get_edges(WAVE, [Rac1], []))
        rules += "1: WAVE* = Rac1 \n"  # or IRSp53

        G.add_weighted_edges_from(
            self.get_edges(Arp2_3, [PAK, WASP, WAVE, Cortactin], [Profilin, Thymosin, Coronin]))
        rules += "1: Arp2_3* = PAK and (" + self.voting_rule([WASP, WAVE, Cortactin],
                                                             [Profilin, Thymosin, Coronin]) + ")\n"

        G.add_weighted_edges_from(self.get_edges(Rac1, [Arp2_3, Dia1, RhoA], [ROCK_]))
        rules += "1: Rac1* = not ROCK and (Arp2_3 or Dia1) \n"

        G.add_weighted_edges_from(self.get_edges(RhoA, [], [Rac1, PAK]))
        rules += "1: RhoA* = not Rac1 and not PAK \n"

        G.add_weighted_edges_from(self.get_edges(Thymosin, [], [WASP, Cofilin]))
        rules += "1: Thymosin* = not WASP and not Cofilin \n"

        G.add_weighted_edges_from(self.get_edges(Cortactin, [Rac1, PAK], [Coronin, PKD]))
        rules += "1: Cortactin* = (Rac1 and PAK) or ((Rac1 or PAK) and not (Coronin and PKD)) \n"  # voting

        G.add_weighted_edges_from(self.get_edges(IRSp53, [Cdc42, Rac1], []))
        rules += "1: IRSp53* = Cdc42 or Rac1 \n"

        G.add_weighted_edges_from(self.get_edges(PAK, [Rac1, Cdc42, PKD], []))
        rules += "1: PAK* = Rac1 or Cdc42 or PKD \n"

        G.add_weighted_edges_from(self.get_edges(Dia1, [RhoA], [CP]))
        rules += "1: Dia1* = RhoA and not CP \n"

        G.add_weighted_edges_from(self.get_edges(Dia2, [Rac1, RhoA], []))
        rules += "1: Dia2* = Rac1 or RhoA \n"

        G.add_weighted_edges_from(self.get_edges(Ena_Vasp, [IRSp53, WASP, PKD], []))
        rules += "1: Ena_Vasp* = IRSp53 or WASP or PKD \n"

        G.add_weighted_edges_from(self.get_edges(Profilin, [WASP, Dia1, WAVE], [Thymosin, PIP2]))
        rules += "1: Profilin* = " + self.voting_rule(["WASP", "Dia1", "WAVE"], ["Thymosin", "PIP2"]) + " \n"

        G.add_weighted_edges_from(self.get_edges(CP, [Arp2_3], [Ena_Vasp, PIP2]))
        rules += "1: CP* = (Arp2_3 and not Ena_Vasp) or not PIP2 \n"

        G.add_weighted_edges_from(self.get_edges(Coronin, [SSH], []))
        rules += "1: Coronin* = SSH \n"

        G.add_weighted_edges_from(self.get_edges(ROCK, [RhoA], [SSH, Coronin]))
        rules += "1: ROCK* = RhoA and not (SSH and Coronin) \n"

        G.add_weighted_edges_from(self.get_edges(PKD, [ROCK], []))
        rules += "1: PKD* = ROCK \n"

        G.add_weighted_edges_from(self.get_edges(LIMK, [ROCK, PAK], [SSH]))
        rules += "1: LIMK* = (ROCK or PAK) and not SSH \n"

        G.add_weighted_edges_from(self.get_edges(Cofilin, [SSH, Arp2_3], [PIP2, Thymosin, LIMK, Cortactin]))
        rules += "1: Cofilin* = " + self.voting_rule(["SSH", "Arp2_3"],
                                                     ["PIP2", "Thymosin", "LIMK", "Cortactin"]) + "\n"

        G.add_weighted_edges_from(self.get_edges(SSH, [Coronin, Rac1], [PKD]))
        rules += "1: SSH* = (Coronin or Rac1) and not PKD \n"

        G.add_weighted_edges_from(self.get_edges(Actin_BR, [Arp2_3], []))
        rules += "1: Actin_BR* = (Arp2_3) \n"  # or Cofilin) and not Thymosin

        G.add_weighted_edges_from(self.get_edges(Actin_ST, [Profilin, Dia1, Dia2, Ena_Vasp], [CP, Cofilin]))
        rules += "1: Actin_ST* = Profilin and (" + self.voting_rule(["Dia1", "Dia2", "Ena_Vasp"],
                                                                    ["CP", "Cofilin"]) + ")\n"

        self.boolean_rules = rules
        self.graph = G

    def voting_rule(self, act, inh):
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

    def get_edges(self, target, act, inh):
        res = []
        for a in act:
            res.append((a, target, 1))
        for i in inh:
            res.append((i, target, -1))

        return res
