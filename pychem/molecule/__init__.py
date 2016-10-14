from . import molecule
from .parsers import smiles as smiles_parser
from .parsers import iupac as iupac_parser
from .parsers import formula as formula_parser


class Molecule(molecule.Molecule):
    def __init__(self, smiles=None, iupac=None, cas=None, formula=None):
        molecule.Molecule.__init__(self)

        if smiles:
            smiles_parser.parse(smiles, molecule=self)
