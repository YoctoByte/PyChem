import parse_to_molecule as parse
from atoms import Atom

# todo: verify whether a molecule is valid or not; octet rule and stuff...
# todo: calculate resonance structures
# todo: predict stability of molecule
# todo: create molecule from IUPAC naming
# todo: lookup CAS number in some database


class Molecule:
    def __init__(self, formula=None, smiles=None, iupac=None, cas=None):
        """
        :param formula: examples for formula: 'Al2(SO4)3', 'CO2'
        :param smiles: example for smiles: [Al+3].[O-]S(=O)(=O)[O-]O-C-O
        :param iupac: examples for IUPAC: 'aluminium sulfate', 'carbon dioxide'
        :param cas: examples for CAS: '10043-01-3', '124-38-9'
        """
        if formula:
            self.structure = parse.formula(formula)
        elif smiles:
            self.structure = parse.smiles(smiles)
        elif iupac:
            self.structure = parse.iupac(iupac)
        elif cas:
            self.structure = parse.cas(cas)


Molecule(formula='NaCO3')
# 'CH3COOH'
