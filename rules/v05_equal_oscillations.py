import networkx as nx
from rules.enzymes_v04 import *
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
        Changes from v3:
            * separate IRSp53 variants Cdc42 and Rac1 activations
        Changes from v4:
            * Cdc42 -> Dia2 instead of Rac1 -> Dia2
            * CP strong inhibitor for Actin_ST
    """
    
    UPSTREAM = "UPSTREAM"

    G = nx.DiGraph()
    rules = ""    
    
    rules += "1: UPSTREAM* = not UPSTREAM \n"

    G.add_weighted_edges_from(get_edges(WASP, [Rac1, Cdc42, PIP2, Cortactin, IRSp53_Cdc42], [Thymosin]))
    rules += "1: WASP* = not Thymosin and (Rac1 or Cdc42 or PIP2 or Cortactin or IRSp53_Cdc42) \n"
    
    G.add_weighted_edges_from(get_edges(WAVE, [Rac1, IRSp53_Rac1], []))
    rules += "1: WAVE* = Rac1 or IRSp53_Rac1 \n" 

    G.add_weighted_edges_from(get_edges(Arp2_3, [PAK, WASP, WAVE, Cortactin], [Profilin, Thymosin, Coronin]))
    rules += "1: Arp2_3* = PAK and (" + voting_rule([WASP, WAVE, Cortactin], [Profilin, Thymosin, Coronin]) + ")\n"
    
    G.add_weighted_edges_from(get_edges(Rac1, [UPSTREAM], []))
    rules += "1: Rac1* = UPSTREAM \n" 
        
    G.add_weighted_edges_from(get_edges(RhoA, [], [UPSTREAM]))
    rules += "1: RhoA* = not UPSTREAM \n"
    
    G.add_weighted_edges_from(get_edges(Thymosin, [], [WASP, Cofilin]))
    rules += "1: Thymosin* = (not WASP and not Cofilin) \n" 

    G.add_weighted_edges_from(get_edges(Cortactin, [Rac1], [Coronin, PKD]))
    rules += "1: Cortactin* = "+ voting_rule([Rac1], [Coronin, PKD]) +" \n"

    G.add_weighted_edges_from(get_edges(IRSp53_Cdc42, [Cdc42], []))
    rules += "1: IRSp53_Cdc42* = Cdc42 \n"
    
    G.add_weighted_edges_from(get_edges(IRSp53_Rac1, [Rac1], []))
    rules += "1: IRSp53_Rac1* = Rac1 \n"
    
    G.add_weighted_edges_from(get_edges(PAK, [Rac1, Cdc42], []))
    rules += "1: PAK* = Rac1 or Cdc42 \n"

    G.add_weighted_edges_from(get_edges(Dia1, [RhoA], [CP]))
    rules += "1: Dia1* = RhoA and not CP \n"

    G.add_weighted_edges_from(get_edges(Dia2, [Rac1, RhoA], []))
    rules += "1: Dia2* = Cdc42 or RhoA \n"

    G.add_weighted_edges_from(get_edges(Ena_Vasp, [IRSp53_Cdc42, WASP, PKD], []))
    rules += "1: Ena_Vasp* = IRSp53_Cdc42 or WASP or PKD \n"  

    G.add_weighted_edges_from(get_edges(Profilin, [WASP, Dia1, WAVE], [Thymosin, PIP2]))
    rules += "1: Profilin* = " + voting_rule(["WASP", "Dia1", "WAVE"], ["Thymosin", "PIP2"]) + " \n"

    G.add_weighted_edges_from(get_edges(CP, [Arp2_3], [Ena_Vasp, PIP2]))
    rules += "1: CP* = (Arp2_3 and not Ena_Vasp) or not PIP2 \n"

    G.add_weighted_edges_from(get_edges(Coronin, [SSH], []))
    rules += "1: Coronin* = SSH \n"

    G.add_weighted_edges_from(get_edges(ROCK, [RhoA], [SSH, Coronin]))
    rules += "1: ROCK* = RhoA and not (SSH and Coronin) \n"

    G.add_weighted_edges_from(get_edges(PKD, [ROCK], []))
    rules += "1: PKD* = ROCK \n"

    G.add_weighted_edges_from(get_edges(LIMK, [ROCK, PAK, PKD], [SSH]))
    rules += "1: LIMK* = (ROCK or PAK or PKD) and not SSH \n"

    G.add_weighted_edges_from(get_edges(Cofilin, [SSH, Arp2_3], [PIP2, Thymosin, LIMK, Cortactin]))
    rules += "1: Cofilin* = " + voting_rule(["SSH", "Arp2_3"], ["PIP2", "Thymosin", "LIMK", "Cortactin"]) + "\n"

    G.add_weighted_edges_from(get_edges(SSH, [Coronin, Rac1], [PKD]))
    rules += "1: SSH* = (Coronin or Rac1) and not PKD \n"

    G.add_weighted_edges_from(get_edges(Actin_BR, [Arp2_3], []))
    rules += "1: Actin_BR* = Arp2_3 \n" 

    G.add_weighted_edges_from(get_edges(Actin_ST, [Profilin, Dia1, Dia2, Ena_Vasp], [CP, Cofilin]))
    rules += "1: Actin_ST* = Profilin and not CP and (" + voting_rule(["Dia1", "Dia2", "Ena_Vasp"],
                                                           ["Cofilin"]) + ")\n"

    return {"rules":rules, "graph":G}
