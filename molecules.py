import parse_to_molecule as parse
from atoms import Atom

# todo: verify whether a molecule is valid or not; octet rule and stuff...
# todo: calculate resonance structures
# todo: predict stability of molecule
# todo: create molecule from IUPAC naming
# todo: lookup CAS number in some database


class Molecule:
    def __init__(self, formula=None, IUPAC=None, CAS=None):
        # examples for formula: 'Al2(SO4)3', 'CO2'
        # examples for IUPAC: 'aluminium sulfate', 'carbon dioxide'
        # examples for CAS: '10043-01-3', '124-38-9'
        if formula:
            parse.formula(formula)
        elif IUPAC:
            parse.IUPAC(IUPAC)
        elif CAS:
            parse.CAS(CAS)

    def _add_atom(self, atom):
        if not atom:
            return
        print(atom)


Molecule(formula='NaCO3')
