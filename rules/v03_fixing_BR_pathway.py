import networkx as nx
from utils import get_edges, voting_rule

def build_rules():
    """ Actin network rules.
        Changes from initial model:
            * direct activation link RhoA -> Rac1
            * ROCK inhibition delay: RhoA -> ROCK -> ROCK_ -| Rac1
            * weaker RhoA inhibition rule: not Rac1 or not PAK
        Changes from v1:
            * strong inhibitors for Arp2_3 (reworked voting rule)
            * reworked rule for Cortactin
        Changes from v2:
            * deleted PKD activates PAK
            * added link PKD activates LIMK
            * Option A: deleted PAK -> Cortactin link
            * deleted IRSp53 -> WAVE link
            * deleted Rac1 -> IRSp53 link            
    """
    
    Actin_BR = "Actin_BR"
    Actin_ST = "Actin_ST"
    Arp2_3 = "Arp2_3"
    CP = "CP"
    Cdc42 = "Cdc42"
    Cofilin = "Cofilin"
    Coronin = "Coronin"
    Cortactin = "Cortactin"
    Dia1 = "Dia1"
    Dia2 = "Dia2"
    Ena_Vasp = "Ena_Vasp"
    IRSp53 = "IRSp53"
    LIMK = "LIMK"
    PAK = "PAK"
    PIP2 = "PIP2"
    PKD = "PKD"
    Profilin = "Profilin"
    ROCK = "ROCK"
    ROCK_ = "ROCK_"
    Rac1 = "Rac1"
    RhoA = "RhoA"
    SSH = "SSH"
    Thymosin = "Thymosin"
    WASP = "WASP"
    WAVE = "WAVE"

    G = nx.DiGraph()
    rules = ""

    G.add_weighted_edges_from(get_edges(WASP, [Rac1, Cdc42, PIP2, Cortactin, IRSp53], [Thymosin]))
    rules += "1: WASP* = not Thymosin and (Rac1 or Cdc42 or PIP2 or Cortactin or IRSp53) \n"

    G.add_weighted_edges_from(get_edges(WAVE, [Rac1], []))
    rules += "1: WAVE* = Rac1 \n" 

    G.add_weighted_edges_from(get_edges(Arp2_3, [PAK, WASP, WAVE, Cortactin], [Profilin, Thymosin, Coronin]))
    rules += "1: Arp2_3* = PAK and (" + voting_rule([WASP, WAVE, Cortactin],
                                                    [Profilin, Thymosin, Coronin]) + ")\n"

    G.add_weighted_edges_from(get_edges(Rac1, [Arp2_3, Dia1, RhoA], [ROCK_]))
    # rules += "1: Rac1* = not ROCK_ and (Arp2_3 or Dia1 or RhoA) \n"  # intermediate ROCK_ node + activation from RhoA
    rules += "1: Rac1* = not ROCK_ and (Arp2_3 or Dia1) \n" 

    G.add_weighted_edges_from(get_edges(RhoA, [], [Rac1, PAK]))
    rules += "1: RhoA* = not (Rac1 or PAK) \n"

    G.add_weighted_edges_from(get_edges(Thymosin, [], [WASP, Cofilin]))
    rules += "1: Thymosin* = not WASP and not Cofilin \n"

    G.add_weighted_edges_from(get_edges(Cortactin, [Rac1], [Coronin, PKD]))
    rules += "1: Cortactin* = "+ voting_rule([Rac1], [Coronin, PKD]) +" \n"

    G.add_weighted_edges_from(get_edges(IRSp53, [Cdc42], []))
    rules += "1: IRSp53* = Cdc42 \n"
    
    G.add_weighted_edges_from(get_edges(PAK, [Rac1, Cdc42], []))
    rules += "1: PAK* = Rac1 or Cdc42 \n"

    G.add_weighted_edges_from(get_edges(Dia1, [RhoA], [CP]))
    rules += "1: Dia1* = RhoA and not CP \n"

    G.add_weighted_edges_from(get_edges(Dia2, [Rac1, RhoA], []))
    rules += "1: Dia2* = Rac1 or RhoA \n"

    G.add_weighted_edges_from(get_edges(Ena_Vasp, [IRSp53, WASP, PKD], []))
    rules += "1: Ena_Vasp* = IRSp53 or WASP or PKD \n"  

    G.add_weighted_edges_from(get_edges(Profilin, [WASP, Dia1, WAVE], [Thymosin, PIP2]))
    rules += "1: Profilin* = " + voting_rule(["WASP", "Dia1", "WAVE"], ["Thymosin", "PIP2"]) + " \n"

    G.add_weighted_edges_from(get_edges(CP, [Arp2_3], [Ena_Vasp, PIP2]))
    rules += "1: CP* = (Arp2_3 and not Ena_Vasp) or not PIP2 \n"

    G.add_weighted_edges_from(get_edges(Coronin, [SSH], []))
    rules += "1: Coronin* = SSH \n"

    G.add_weighted_edges_from(get_edges(ROCK, [RhoA], [SSH, Coronin]))
    rules += "1: ROCK* = RhoA and not (SSH and Coronin) \n"

    G.add_weighted_edges_from(get_edges(ROCK_, [ROCK], []))
    rules += "1: ROCK_* = ROCK \n"

    G.add_weighted_edges_from(get_edges(PKD, [ROCK], []))
    rules += "1: PKD* = ROCK \n"

    G.add_weighted_edges_from(get_edges(LIMK, [ROCK, PAK, PKD], [SSH]))
    rules += "1: LIMK* = (ROCK or PAK or PKD) and not SSH \n"

    G.add_weighted_edges_from(get_edges(Cofilin, [SSH, Arp2_3], [PIP2, Thymosin, LIMK, Cortactin]))
    rules += "1: Cofilin* = " + voting_rule(["SSH", "Arp2_3"],
                                            ["PIP2", "Thymosin", "LIMK", "Cortactin"]) + "\n"

    G.add_weighted_edges_from(get_edges(SSH, [Coronin, Rac1], [PKD]))
    rules += "1: SSH* = (Coronin or Rac1) and not PKD \n"

    G.add_weighted_edges_from(get_edges(Actin_BR, [Arp2_3], []))
    rules += "1: Actin_BR* = (Arp2_3) \n"  # or Cofilin) and not Thymosin

    G.add_weighted_edges_from(get_edges(Actin_ST, [Profilin, Dia1, Dia2, Ena_Vasp], [CP, Cofilin]))
    rules += "1: Actin_ST* = Profilin and (" + voting_rule(["Dia1", "Dia2", "Ena_Vasp"],
                                                           ["CP", "Cofilin"]) + ")\n"

    return {"rules":rules, "graph":G}
